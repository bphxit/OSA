from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from app.ingest.csv_importer import import_csv
p=Path(sys.argv[1]).expanduser().resolve()
print(json.dumps(import_csv(p), indent=2))
