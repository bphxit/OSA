# Architecture

```text
OSCAR / PrismaTS / medical files
            |
       local ingestion
            |
        SQLite MVP DB
            |
    deterministic analytics
            |
       local MCP server
            |
     Claude Desktop/Code
            |
  specialist reasoning + forum
            |
      saved assessment
```

SQLite is used for the Windows MVP to minimize deployment complexity. PostgreSQL can be introduced later without changing the MCP contract.

Clinical safety: this is a decision-support prototype. It does not control a PAP device or autonomously change settings.
