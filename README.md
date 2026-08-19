# OSA Therapy System — Windows 11 MVP

Local-first OSA/BiPAP therapy analysis system designed to work with an existing Claude subscription and **without the Anthropic Claude API**.

## Real export formats validated
The importer has been tested against the real project Library schemas:

- OSCAR `Sessions` CSV — fields include Date, Session, Start, End, Total Time, AHI, CA Count, OA Count, H Count, and pressure statistics.
- OSCAR `Details` CSV — 4-column high-volume event stream: DateTime, Session, Event, Data/Duration. The sample contains events such as IPAP, EPAP, Hypopnea, Obstructive, RERA, Apnea and VSnore.
- Loewenstein PrismaTS `TherapyStatistics` CSV — semicolon-delimited Value/Unit export with AHI, OA/CA/HI, leak, EPAP/IPAP, SpO2, heart-rate and ventilation statistics.

Your personal exports are **not stored in this public repository**. Only synthetic test fixtures are included.

## Architecture
- Python + SQLite local database
- Deterministic ingestion and analytics
- OSCAR raw event storage in `pap_events`
- PrismaTS daily statistics in `daily_metrics`
- Local MCP server for Claude Desktop/Claude Code
- Windows PowerShell automation
- No API key or per-token Anthropic API billing

## Install on Windows 11
Run `installer\\install.cmd`.

The installer creates `.venv`, installs dependencies, initializes the database, creates data folders and installs the optional Windows scheduled ingestion task.

## Data flow
Copy exports into `data\\incoming`:

```text
OSCAR Sessions.csv ─┐
OSCAR Details.csv  ─┼─► importer ─► SQLite local DB ─► MCP ─► Claude Desktop / Code
PrismaTS TherapyStatistics.csv ─┘
```

## Duplicate-date behavior
The ingestion layer follows the project specification: when an imported therapy date already exists for the same source, that date is skipped rather than creating a second copy. New dates in the same multi-day export are still imported.

## Testing
Run:

```powershell
python -m pytest -q
```

## Safety
This is a personal clinical decision-support prototype. It does not control a PAP device and does not replace qualified clinical care. Potential therapy changes require clinician review.
