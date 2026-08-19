from pathlib import Path
import tempfile

from app.core import config
import app.core.db as dbmod
from app.core.db import connect
from app.ingest.csv_importer import import_csv

DATA = Path(__file__).parent.parent / 'testdata'


def _redirect_db(monkeypatch, td):
    data = Path(td)
    monkeypatch.setattr(config, 'DATA', data)
    monkeypatch.setattr(config, 'DB_PATH', data / 'osa.db')
    monkeypatch.setattr(dbmod, 'DATA', data)
    monkeypatch.setattr(dbmod, 'DB_PATH', data / 'osa.db')


def test_oscar_sessions_import(monkeypatch):
    with tempfile.TemporaryDirectory() as td:
        _redirect_db(monkeypatch, td)
        result = import_csv(DATA / 'oscar_sessions_sample.csv')
        assert result['inserted'] == 1
        db = connect()
        row = db.execute("SELECT ahi,oa,hi,usage_hours FROM sleep_sessions WHERE source='oscar_sessions' AND session_id='21'").fetchone()
        assert round(row['ahi'], 3) == 17.814
        assert row['oa'] == 28
        assert row['hi'] == 87
        assert round(row['usage_hours'], 4) > 6.6


def test_prisma_import(monkeypatch):
    with tempfile.TemporaryDirectory() as td:
        _redirect_db(monkeypatch, td)
        result = import_csv(DATA / 'prismats_therapystatistics_sample.csv')
        assert result['inserted'] == 1
        db = connect()
        row = db.execute("SELECT ahi,oa,ca,hi,ipap_max,ipap_p95,epap_max FROM daily_metrics WHERE source='prismats'").fetchone()
        assert row['ahi'] == 11
        assert row['oa'] == 11
        assert row['ca'] == 0
        assert row['hi'] == 12
        assert row['ipap_max'] == 10
        assert row['epap_max'] == 5
