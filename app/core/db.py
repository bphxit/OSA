import sqlite3
from .config import DB_PATH, DATA

SCHEMA = '''
CREATE TABLE IF NOT EXISTS sleep_sessions (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 patient_id TEXT NOT NULL DEFAULT 'default',
 therapy_date TEXT NOT NULL,
 session_id TEXT,
 start_time TEXT,
 end_time TEXT,
 source TEXT NOT NULL,
 source_file TEXT NOT NULL,
 duration_seconds REAL,
 usage_hours REAL,
 ahi REAL, oa REAL, ca REAL, hi REAL, ua REAL, rera REAL,
 snoring_index REAL,
 median_pressure REAL, median_ipap REAL, median_epap REAL,
 p95_pressure REAL, p95_ipap REAL, p95_epap REAL,
 max_pressure REAL, max_ipap REAL, max_epap REAL,
 raw_json TEXT,
 created_at TEXT DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(patient_id, therapy_date, source, session_id, source_file)
);
CREATE TABLE IF NOT EXISTS daily_metrics (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 patient_id TEXT NOT NULL DEFAULT 'default',
 therapy_date TEXT NOT NULL,
 source TEXT NOT NULL,
 source_file TEXT NOT NULL,
 usage_hours REAL,
 ahi REAL, oa REAL, ca REAL, hi REAL, rera REAL,
 leak_p50 REAL, leak_p95 REAL, duration_leak_high REAL,
 epap_min REAL, epap_max REAL, ipap_min REAL, ipap_max REAL, ipap_p95 REAL,
 spo2_min REAL, spo2_p50 REAL, spo2_p95 REAL,
 hr_p50 REAL,
 breathing_frequency_p50 REAL,
 tidal_volume_p50 REAL,
 minute_ventilation_p50 REAL,
 raw_json TEXT,
 created_at TEXT DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(patient_id, therapy_date, source)
);
CREATE TABLE IF NOT EXISTS pap_events (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 patient_id TEXT NOT NULL DEFAULT 'default',
 therapy_date TEXT NOT NULL,
 session_id TEXT,
 event_time TEXT,
 event_type TEXT NOT NULL,
 value REAL,
 source_file TEXT NOT NULL,
 UNIQUE(therapy_date, session_id, event_time, event_type, value, source_file)
);
CREATE INDEX IF NOT EXISTS idx_pap_events_date ON pap_events(therapy_date);
CREATE TABLE IF NOT EXISTS medical_facts (
 id INTEGER PRIMARY KEY AUTOINCREMENT, fact_type TEXT, fact TEXT, event_date TEXT,
 source_document TEXT, status TEXT DEFAULT 'pending', created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS therapy_changes (
 id INTEGER PRIMARY KEY AUTOINCREMENT, change_date TEXT, device TEXT, mode TEXT,
 settings_json TEXT, mask TEXT, reason TEXT, outcome TEXT
);
CREATE TABLE IF NOT EXISTS assessments (
 id INTEGER PRIMARY KEY AUTOINCREMENT, assessment_date TEXT, report TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS data_quality_issues (
 id INTEGER PRIMARY KEY AUTOINCREMENT, therapy_date TEXT, source TEXT, severity TEXT, issue TEXT,
 created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
'''

def connect():
    DATA.mkdir(parents=True, exist_ok=True)
    c=sqlite3.connect(DB_PATH)
    c.row_factory=sqlite3.Row
    c.executescript(SCHEMA)
    return c
