# Windows 11 Deployment

1. Install Python 3.11+.
2. Download/clone the repository.
3. Open PowerShell in the OSA folder.
4. Run `Set-ExecutionPolicy -Scope Process Bypass`.
5. Run `installer\\install.cmd` or `installer\\install.ps1`.
6. The installer creates `.venv`, installs dependencies, initializes SQLite, creates data folders and registers `OSA Therapy Data Watcher` at logon.
7. Put OSCAR/PrismaTS CSV exports into `data\\incoming`.
8. The watcher imports them automatically and moves processed source files to `data\\processed`.
9. Start the local API with `scripts\\start-osa.ps1`.
10. Configure Claude Desktop with the example MCP configuration, replacing the example path with the actual installation path.

No Anthropic API key is used by this project.

## Current automation boundary
The importer and analytics are automated. Claude reasoning is exposed through local MCP. Fully autonomous clinical decisions and PAP device setting changes are intentionally not implemented.
