from pathlib import Path
from app.ingest.csv_importer import import_csv
from app.core.db import connect
BASE=Path(__file__).resolve().parents[1]; incoming=BASE/'data'/'incoming'; processed=BASE/'data'/'processed'; connect().close()
for p in incoming.glob('*.csv'):
 try: print(import_csv(p)); p.rename(processed/p.name)
 except Exception as e: print(f'ERROR {p.name}: {e}')
