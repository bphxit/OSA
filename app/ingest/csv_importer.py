from pathlib import Path
import csv
import json
import pandas as pd
from app.core.db import connect


def _clean_number(v):
    if v is None or (isinstance(v, float) and pd.isna(v)): return None
    s=str(v).strip().replace('%','').replace(',','')
    if not s or s in {'--','-','nan','NaN'}: return None
    try: return float(s)
    except (ValueError, TypeError): return None


def _read_csv(path: Path):
    first = path.read_text(encoding='utf-8-sig', errors='replace').splitlines()[0]
    sep = ';' if first.count(';') > first.count(',') else ','
    return pd.read_csv(path, sep=sep, encoding='utf-8-sig'), sep


def _json_row(row):
    return json.dumps({str(k): (None if pd.isna(v) else str(v)) for k,v in row.items()}, ensure_ascii=False)


def _duration_to_hours(v):
    if v is None or pd.isna(v): return None
    s=str(v).strip()
    if ':' in s:
        try: return pd.to_timedelta(s).total_seconds()/3600
        except Exception: return None
    return _clean_number(v)


def import_oscar_sessions(path: Path):
    df,_ = _read_csv(path)
    required={'Date','Session','Start','End','Total Time','AHI','CA Count','OA Count','H Count'}
    missing=required-set(df.columns)
    if missing: raise ValueError(f'OSCAR Sessions missing columns: {sorted(missing)}')
    inserted=skipped=0; db=connect()
    existing_dates={x[0] for x in db.execute("SELECT DISTINCT therapy_date FROM sleep_sessions WHERE source='oscar_sessions'").fetchall()}
    for _,r in df.iterrows():
        d=pd.to_datetime(r['Date'], errors='coerce')
        if pd.isna(d): continue
        therapy_date=d.strftime('%Y-%m-%d')
        if therapy_date in existing_dates:
            skipped += 1; continue
        sid=str(r['Session'])
        duration=pd.to_timedelta(r['Total Time'], errors='coerce').total_seconds() if pd.notna(r['Total Time']) else None
        vals=(therapy_date,sid,str(r['Start']),str(r['End']),'oscar_sessions',path.name,duration,duration/3600 if duration else None,
              _clean_number(r['AHI']),_clean_number(r['OA Count']),_clean_number(r['CA Count']),_clean_number(r['H Count']),_clean_number(r.get('UA Count')),
              _clean_number(r.get('RE Count')),_clean_number(r.get('VS Count')),_clean_number(r.get('Median Pressure')),_clean_number(r.get('Median IPAP')),
              _clean_number(r.get('Median EPAP')),_clean_number(r.get('95% Pressure')),_clean_number(r.get('95% IPAP')),_clean_number(r.get('95% EPAP')),
              _clean_number(r.get('Max Pressure')),_clean_number(r.get('Max IPAP')),_clean_number(r.get('Max EPAP')),_json_row(r))
        cur=db.execute('''INSERT OR IGNORE INTO sleep_sessions
          (therapy_date,session_id,start_time,end_time,source,source_file,duration_seconds,usage_hours,ahi,oa,ca,hi,ua,rera,snoring_index,median_pressure,median_ipap,median_epap,p95_pressure,p95_ipap,p95_epap,max_pressure,max_ipap,max_epap,raw_json)
          VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', vals)
        inserted += 1 if cur.rowcount else 0
        skipped += 0 if cur.rowcount else 1
    db.commit(); db.close(); return {'file':path.name,'type':'oscar_sessions','inserted':inserted,'skipped':skipped}


def import_oscar_details(path: Path):
    db=connect(); inserted=skipped=0; batch=[]
    existing_dates={x[0] for x in db.execute('SELECT DISTINCT therapy_date FROM pap_events').fetchall()}
    skipped_dates=set()
    with path.open('r',encoding='utf-8-sig',newline='') as fh:
        reader=csv.DictReader(fh); required={'DateTime','Session','Event','Data/Duration'}
        missing=required-set(reader.fieldnames or [])
        if missing: raise ValueError(f'OSCAR Details missing columns: {sorted(missing)}')
        for r in reader:
            dt=pd.to_datetime(r.get('DateTime'), errors='coerce')
            if pd.isna(dt): continue
            therapy_date=dt.strftime('%Y-%m-%d')
            if therapy_date in existing_dates or therapy_date in skipped_dates:
                skipped_dates.add(therapy_date); continue
            batch.append((therapy_date,str(r.get('Session','')),dt.isoformat(),str(r.get('Event','')),_clean_number(r.get('Data/Duration')),path.name))
            if len(batch)>=10000:
                cur=db.executemany('INSERT OR IGNORE INTO pap_events(therapy_date,session_id,event_time,event_type,value,source_file) VALUES(?,?,?,?,?,?)',batch)
                n=max(cur.rowcount,0); inserted+=n; skipped+=len(batch)-n; db.commit(); batch.clear()
    if batch:
        cur=db.executemany('INSERT OR IGNORE INTO pap_events(therapy_date,session_id,event_time,event_type,value,source_file) VALUES(?,?,?,?,?,?)',batch)
        n=max(cur.rowcount,0); inserted+=n; skipped+=len(batch)-n
    db.commit(); db.close(); return {'file':path.name,'type':'oscar_details','inserted':inserted,'skipped':skipped}


def import_prismats(path: Path):
    df,_ = _read_csv(path)
    if 'Filter_From' not in df.columns or 'Filter_To' not in df.columns: raise ValueError('PrismaTS TherapyStatistics requires Filter_From and Filter_To')
    value_rows=df[df['Id'].astype(str).str.lower().eq('value')].copy() if 'Id' in df.columns else df.iloc[:1]
    inserted=skipped=0; db=connect()
    existing_dates={x[0] for x in db.execute("SELECT DISTINCT therapy_date FROM daily_metrics WHERE source='prismats'").fetchall()}
    for _,r in value_rows.iterrows():
        d=pd.to_datetime(str(r['Filter_From']).strip(), dayfirst=True, errors='coerce')
        if pd.isna(d): continue
        therapy_date=d.strftime('%Y-%m-%d')
        if therapy_date in existing_dates:
            skipped+=1; continue
        def n(name): return _clean_number(r.get(name))
        row=(therapy_date,'prismats',path.name,_duration_to_hours(r.get('AvgUsage')),n('AHI'),n('oAHI'),n('cAHI'),n('HI'),
             n('Percentile_Leakage_P50'),n('Percentile_Leakage_P95'),n('Percentile_DurationLeakageHigh_P95'),n('PressureEpapMin'),n('PressureEpapMax'),
             n('PressureIpapMin'),n('PressureIpapMax'),n('Percentile_Ipap_P95'),n('Min_SpO2'),n('Percentile_SpO2_P50'),n('Percentile_SpO2_P95'),
             n('Percentile_HeartRate_P50'),n('Percentile_BreathingFrequency_P50'),n('Percentile_Vt_P50'),n('Percentile_Amv_P50'),_json_row(r))
        cur=db.execute('''INSERT OR IGNORE INTO daily_metrics
            (therapy_date,source,source_file,usage_hours,ahi,oa,ca,hi,leak_p50,leak_p95,duration_leak_high,epap_min,epap_max,ipap_min,ipap_max,ipap_p95,spo2_min,spo2_p50,spo2_p95,hr_p50,breathing_frequency_p50,tidal_volume_p50,minute_ventilation_p50,raw_json)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',row)
        inserted+=1 if cur.rowcount else 0; skipped+=0 if cur.rowcount else 1
    db.commit(); db.close(); return {'file':path.name,'type':'prismats_therapy_statistics','inserted':inserted,'skipped':skipped}


def import_csv(path: Path):
    name=path.name.lower()
    if 'oscar' in name and 'details' in name: return import_oscar_details(path)
    if 'oscar' in name and 'sessions' in name: return import_oscar_sessions(path)
    if 'prism' in name and 'therapystatistics' in name: return import_prismats(path)
    raise ValueError(f'Unsupported OSA export: {path.name}')
