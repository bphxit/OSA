import sqlite3
from pathlib import Path
import json,re,pandas as pd
from app.core.db import connect
ALIASES={'date':['date','session date','therapy date','start date'],'usage_hours':['usage','usage hours','therapy hours','hours'],'ahi':['ahi'],'oa':['oa','obstructive apnea'],'ca':['ca','central apnea'],'hi':['hi','hypopnea'],'rera':['rera'],'spo2_mean':['spo2 mean','avg spo2','mean spo2'],'spo2_min':['spo2 min','minimum spo2','min spo2'],'snoring_index':['snoring index'],'snoring_duration_min':['snoring duration','snore duration'],'snoring_pct':['snoring %','snoring percent'],'csr_pct':['csr','cheyne stokes','csr %'],'periodic_breathing_pct':['periodic breathing','pb %','pb'],'leak_median':['median leak','leak median'],'leak_95':['95% leak','95th percentile leak','95 leak'],'leak_above_threshold_min':['time above leak threshold'],'mask_off_events':['mask off'],'avg_pressure':['average pressure','avg pressure'],'median_pressure':['median pressure'],'hr_mean':['mean hr','average hr','hr mean'],'hrv_mean':['hrv'],'tst_hours':['tst','total sleep time'],'sleep_efficiency':['sleep efficiency'],'awakenings':['awakenings','arousals'],'rem_hours':['rem'],'deep_sleep_hours':['deep sleep','n3'],'sleep_latency_min':['sleep latency']}
def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s).lower()).strip()
def map_columns(columns):
 n={norm(c):c for c in columns}; out={}
 for f,a in ALIASES.items():
  for x in a:
   if norm(x) in n: out[f]=n[norm(x)]; break
 return out
def num(v):
 try:return float(str(v).replace('%','').replace(',','').strip())
 except:return None
def import_csv(path:Path):
 df=pd.read_csv(path); m=map_columns(df.columns)
 if 'date' not in m: raise ValueError(f'No date column identified in {path.name}')
 source='oscar' if 'oscar' in path.name.lower() else ('prismats' if 'prisma' in path.name.lower() else 'csv')
 db=connect(); ins=skip=issues=0
 for _,row in df.iterrows():
  d=pd.to_datetime(row[m['date']],errors='coerce')
  if pd.isna(d): issues+=1; continue
  ds=d.strftime('%Y-%m-%d'); v={k:num(row[c]) for k,c in m.items() if k!='date'}
  try:
   db.execute('INSERT INTO sleep_sessions(session_date,source,source_file,usage_hours,ahi,oa,ca,hi,rera,spo2_mean,spo2_min,snoring_index,snoring_duration_min,snoring_pct,csr_pct,periodic_breathing_pct,leak_median,leak_95,leak_above_threshold_min,mask_off_events,avg_pressure,median_pressure,hr_mean,hrv_mean,tst_hours,sleep_efficiency,awakenings,rem_hours,deep_sleep_hours,sleep_latency_min,raw_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(ds,source,path.name,v.get('usage_hours'),v.get('ahi'),v.get('oa'),v.get('ca'),v.get('hi'),v.get('rera'),v.get('spo2_mean'),v.get('spo2_min'),v.get('snoring_index'),v.get('snoring_duration_min'),v.get('snoring_pct'),v.get('csr_pct'),v.get('periodic_breathing_pct'),v.get('leak_median'),v.get('leak_95'),v.get('leak_above_threshold_min'),v.get('mask_off_events'),v.get('avg_pressure'),v.get('median_pressure'),v.get('hr_mean'),v.get('hrv_mean'),v.get('tst_hours'),v.get('sleep_efficiency'),v.get('awakenings'),v.get('rem_hours'),v.get('deep_sleep_hours'),v.get('sleep_latency_min'),json.dumps({str(k):str(x) for k,x in row.to_dict().items()}))); ins+=1
  except sqlite3.IntegrityError: skip+=1
  except Exception: issues+=1
 db.commit(); db.close(); return {'file':path.name,'inserted':ins,'skipped':skip,'issues':issues,'columns':m}
