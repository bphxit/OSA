from mcp.server.fastmcp import FastMCP
from app.analytics.metrics import summary,trend
from app.core.db import connect
mcp=FastMCP('OSA Therapy System')
@mcp.tool()
def get_sleep_summary(days:int=30)->dict: return summary(days)
@mcp.tool()
def get_sleep_trend(days:int=30)->list: return trend(days)
@mcp.tool()
def get_patient_profile()->dict: return {'patient_id':'default','source':'local OSA database'}
@mcp.tool()
def get_medical_history()->list:
 db=connect(); r=[dict(x) for x in db.execute('SELECT * FROM medical_facts ORDER BY event_date DESC').fetchall()]; db.close(); return r
@mcp.tool()
def get_therapy_changes()->list:
 db=connect(); r=[dict(x) for x in db.execute('SELECT * FROM therapy_changes ORDER BY change_date DESC').fetchall()]; db.close(); return r
@mcp.tool()
def save_assessment(assessment_date:str,report:str)->dict:
 db=connect(); db.execute('INSERT INTO assessments(assessment_date,report) VALUES(?,?)',(assessment_date,report)); db.commit(); db.close(); return {'saved':True,'date':assessment_date}
if __name__=='__main__': mcp.run()
