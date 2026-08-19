from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

# This test expects representative real exports to be copied to a local test-data directory.
# It is intentionally opt-in so personal medical data is never committed to the repository.

def test_modules_import():
    from app.ingest.csv_importer import import_csv
    from app.analytics.daily import build_daily_snapshot
    from app.analytics.metrics import summary, trend
    assert callable(import_csv)
    assert callable(build_daily_snapshot)
    assert callable(summary)
    assert callable(trend)
