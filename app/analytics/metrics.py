from app.core.db import connect


def _avg(rows, key):
    vals=[r[key] for r in rows if r[key] is not None]
    return round(sum(vals)/len(vals),3) if vals else None


def summary(days=30):
    db=connect()
    sessions=[dict(r) for r in db.execute('SELECT * FROM sleep_sessions ORDER BY therapy_date DESC, start_time DESC').fetchall()]
    daily=[dict(r) for r in db.execute('SELECT * FROM daily_metrics ORDER BY therapy_date DESC').fetchall()]
    db.close()
    if not sessions and not daily: return {'days':0,'message':'No PAP exports imported'}
    return {'session_count':len(sessions),'prismats_daily_count':len(daily),'latest_session':sessions[0] if sessions else None,'latest_prismats_day':daily[0] if daily else None,'oscar_averages':{k:_avg(sessions[:days],k) for k in ['ahi','oa','ca','hi','rera','usage_hours','median_pressure','median_ipap','median_epap','p95_ipap','p95_epap']},'prismats_latest':daily[0] if daily else None}


def trend(days=30):
    db=connect()
    rows=[dict(r) for r in db.execute('''SELECT therapy_date,source,usage_hours,ahi,oa,ca,hi,rera,leak_p50,leak_p95,epap_min,epap_max,ipap_min,ipap_max,ipap_p95,spo2_min,spo2_p50,spo2_p95,hr_p50 FROM daily_metrics ORDER BY therapy_date DESC LIMIT ?''',(days,)).fetchall()]
    if not rows:
        rows=[dict(r) for r in db.execute('''SELECT therapy_date,source,usage_hours,ahi,oa,ca,hi,rera,median_ipap,median_epap,p95_ipap,p95_epap FROM sleep_sessions ORDER BY therapy_date DESC,start_time DESC LIMIT ?''',(days,)).fetchall()]
    db.close(); return rows
