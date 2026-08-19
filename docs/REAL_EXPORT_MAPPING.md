# Real export mapping used by the importer

The importer was validated against the real exports available in the project Library.

## OSCAR Sessions

Example: `OSCAR_Amit Granot_Sessions_2026-08-15_2026-08-16.csv`

Key fields include `Date`, `Session`, `Start`, `End`, `Total Time`, `AHI`, `CA Count`, `OA Count`, `H Count`, `UA Count`, `RE Count`, `VS Count`, and median/95th/max pressure fields.

The file can contain **multiple sessions on the same therapy date**. The database therefore uses the session identifier and source file in the uniqueness rule rather than treating date alone as unique.

## OSCAR Details

Example: `OSCAR_Amit Granot_Details_2026-08-15_2026-08-16.csv`

Columns: `DateTime`, `Session`, `Event`, `Data/Duration`.

The current importer stores timestamped event rows. Event types observed in the supplied export include IPAP, EPAP, Hypopnea, VSnore, Obstructive, RERA and Apnea.

## PrismaTS TherapyStatistics

Example: `2026-08-17_LMT_30031465_prisma30ST_TherapyStatistics.csv`

This export is semicolon-separated and contains a `Value` row followed by a `Unit` row. The importer keeps the `Value` row.

The current mapping includes:

- AHI, oAHI, cAHI, HI
- leakage P50/P95 and high-leak duration
- EPAP min/max
- IPAP min/max and P95
- breathing frequency P50
- tidal volume P50
- minute ventilation P50
- minimum/P50/P95 SpO2 where available
- heart-rate P50 where available
- usage duration

`--` is treated as unavailable rather than zero.
