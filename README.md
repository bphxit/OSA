# OSA Therapy System

Windows 11 local-first OSA/BiPAP therapy analysis platform based on the supplied OSA Definition specification.

## Goals
- Import OSCAR and PrismaTS CSV exports.
- Preserve a longitudinal local database.
- Calculate deterministic PAP metrics and trends.
- Expose local OSA data through MCP to Claude Desktop/Claude Code — **no Claude API is required**.
- Automate Windows ingestion and deployment.
- Keep clinical recommendations advisory; PAP setting changes require clinician review.

## Windows 11 install
Double-click `installer\\install.cmd`, or run `installer\\install.ps1` from PowerShell.

See `docs/WINDOWS11.md` and `docs/DEPLOYMENT.md`.

## Safety
This is a personal clinical decision-support prototype, not an autonomous prescriber or medical device. It does not control a PAP device.
