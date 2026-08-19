from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from app.ingest.csv_importer import import_csv

incoming=ROOT/'data'/'incoming'
processed=ROOT/'data'/'processed'
archive=ROOT/'data'/'archive'
results=[]
for f in sorted(incoming.glob('*.csv')):
    try:
        result=import_csv(f); results.append(result)
        f.rename(processed/f.name)
    except Exception as e:
        results.append({'file':f.name,'error':str(e)})
        f.rename(archive/f.name)
print(json.dumps(results, indent=2))
