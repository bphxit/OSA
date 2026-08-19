# OSA Therapy System — Windows 11 MVP

Local-first OSA/BiPAP therapy analysis system designed to work with an existing Claude subscription and **without the Anthropic Claude API**.

## Real export formats supported
This version is aligned to the real exports in the project Library:

- OSCAR `Sessions` CSV: one or more therapy sessions per therapy date.
- OSCAR `Details` CSV: timestamped PAP events such as IPAP, EPAP, Hypopnea, Obstructive, RERA and VSnore.
- Loewenstein PrismaTS `TherapyStatistics` CSV: semicolon-separated `Value` / `Unit` export with AHI, OA/CA/HI, leak, EPAP/IPAP, SpO₂, heart-rate and ventilation statistics.

## Architecture
- Python + SQLite local database
- Deterministic ingestion and analytics
- Local MCP server for Claude Desktop/Claude Code
- Windows PowerShell automation
- No API key or per-token Anthropic API billing

## Install on Windows 11
Run `installer\\install.cmd`.

The installer creates `.venv`, installs dependencies, initializes the database, creates data folders and installs the optional Windows scheduled ingestion task.

## Data flow
Copy exports into `data\\incoming`:

```text
OSCAR Sessions.csv
OSCAR Details.csv
PrismaTS TherapyStatistics.csv
          ↓
      importer
          ↓
   SQLite local DB
          ↓
      MCP tools
          ↓
 Claude Desktop / Code
```

## Safety
This is a personal clinical decision-support prototype. It does not control a PAP device and does not replace qualified clinical care. Potential therapy changes require clinician review.
