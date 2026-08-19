import sqlite3
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data'
DB_PATH=Path(os.getenv('OSA_DB_PATH', DATA/'osa.db'))
SCHEMA='''
CREATE TABLE IF NOT EXISTS sleep_sessions (
 id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT NOT NULL DEFAULT 'default', session_date TEXT NOT NULL, source TEXT NOT NULL, source_file TEXT NOT NULL,
 usage_hours REAL, ahi REAL, oa REAL, ca REAL, hi REAL, rera REAL, spo2_mean REAL, spo2_min REAL,
 snoring_index REAL, snoring_duration_min REAL, snoring_pct REAL, csr_pct REAL, periodic_breathing_pct REAL,
 leak_median REAL, leak_95 REAL, leak_above_threshold_min REAL, mask_off_events INTEGER, avg_pressure REAL, median_pressure REAL,
 hr_mean REAL, hrv_mean REAL, tst_hours REAL, sleep_efficiency REAL, awakenings INTEGER, rem_hours REAL, deep_sleep_hours REAL, sleep_latency_min REAL,
 raw_json TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, UNIQUE(patient_id,session_date,source));
CREATE TABLE IF NOT EXISTS medical_facts (id INTEGER PRIMARY KEY AUTOINCREMENT,fact_type TEXT,fact TEXT,event_date TEXT,source_document TEXT,status TEXT DEFAULT 'pending',created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS therapy_changes (id INTEGER PRIMARY KEY AUTOINCREMENT,change_date TEXT,device TEXT,mode TEXT,settings_json TEXT,mask TEXT,reason TEXT,outcome TEXT);
CREATE TABLE IF NOT EXISTS assessments (id INTEGER PRIMARY KEY AUTOINCREMENT,assessment_date TEXT,report TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS data_quality_issues (id INTEGER PRIMARY KEY AUTOINCREMENT,session_date TEXT,source TEXT,severity TEXT,issue TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
'''
def connect():
 DATA.mkdir(parents=True,exist_ok=True); c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; c.executescript(SCHEMA); return c
