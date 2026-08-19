from app.core.db import connect

def summary(days=30):
 db=connect(); rows=db.execute('SELECT * FROM sleep_sessions ORDER BY session_date DESC LIMIT ?', (days,)).fetchall(); db.close()
 if not rows: return {'days':0,'message':'No PAP sessions imported'}
 def avg(k):
  v=[r[k] for r in rows if r[k] is not None]; return round(sum(v)/len(v),2) if v else None
 return {'days':len(rows),'latest':dict(rows[0]),'averages':{k:avg(k) for k in ['ahi','oa','ca','hi','rera','usage_hours','spo2_mean','spo2_min','leak_median','leak_95','csr_pct','periodic_breathing_pct','hr_mean','hrv_mean']}}

def trend(days=30):
 db=connect(); rows=[dict(r) for r in db.execute('SELECT session_date,ahi,oa,ca,hi,usage_hours,spo2_min,leak_95,csr_pct,periodic_breathing_pct FROM sleep_sessions ORDER BY session_date DESC LIMIT ?', (days,)).fetchall()]; db.close(); return rows
