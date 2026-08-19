from fastapi import FastAPI
from app.analytics.metrics import summary,trend
app=FastAPI(title='OSA Therapy System',version='0.1.0')
@app.get('/')
def root(): return {'name':'OSA Therapy System','version':'0.1.0','claude_api':False}
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/api/metrics')
def metrics(days:int=30): return summary(days)
@app.get('/api/sessions')
def sessions(limit:int=30): return trend(limit)
