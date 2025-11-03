# Birds Biodiversity Dataset Overview

This note helps you quickly understand the contents of `data/raw/Observations 2012-2025.xlsx`, the canonical dataset for the final project.

## Source & Scope
- **Program**: Martinique breeding bird monitoring initiative (Applied Statistics final project).
- **Years covered**: 2012–2025 (inclusive) with one row per observation record in the observation sheet.
- **Geography**: Island-wide transects; each observation references a monitoring point.

## Workbook structure
The Excel workbook ships with three tabs you will use together:

| Sheet name | Purpose |
|------------|---------|
| `ESPECES` | Bird taxonomy helper (scientific / French names, migration status, endemic vs. introduced). |
| `GPS-MILIEU` | Site catalogue with one row per observation point (transect ID, point ID, habitat type, GPS labels). |
| `NOM FRANÇAIS` | Observation log – the main fact table with one row per point visit including counts and detection metadata. |

Always keep the mapping sheets (`ESPECES`, `GPS-MILIEU`) alongside the observations so you can enrich the fact table with species and habitat context during your analysis.

## How observations are gathered
1. **Transects as sites** – each transect corresponds to a monitoring site. Every site contains **10 fixed observation points** laid out along the transect.
2. **Visit protocol** – to run a survey, an observer travels to the site, starts at point 1, records birds for **5 minutes**, then walks to the next point and repeats until all 10 points are completed.
3. **Observer frequency** – an observer visits a given site **at most twice** (the protocol does not specify whether this limit applies per season, per year, or over the entire project).
4. **Detection type** – every entry classifies detections as **visual**, **audio**, or **both**, making it possible to analyse modality-specific detection rates.

## What each row represents
- A single visit to an observation point on a given date.
- Consolidates species detected, the number of individuals, detection modality, and effort metadata for that point visit.

## Key columns (high level)
- **`observation_id`** – unique identifier for the record.
- **`transect_id` / `point_id`** – location metadata; `point_id` runs from 1–10 within each transect.
- **`date` / `year`** – visit timestamp; `year` is handy for trend analyses.
- **`observer_id`** – anonymous identifier for the person conducting the transect visit.
- **`species_code` / `species_name`** – species observed.
- **`individual_count`** – number of individuals detected during the 5-minute window.
- **`detection_type`** – categorical field indicating visual, audio, or both.
- **Effort metrics** (e.g., `visit_duration_minutes`, `points_completed`) – important when normalising counts or imputing effort-adjusted indices.

> Additional columns (e.g., weather, notes) may appear. Inspect the header row after loading to confirm availability.

## Recommended first steps
1. **Load** the data with pandas:
   ```python
   import pandas as pd
   df = pd.read_excel("projects/birds-biodiversity/data/raw/Observations 2012-2025.xlsx")
   ```
2. **Check schema consistency** with `df.info()` and `df.head()`.
3. **Validate effort assumptions** – confirm each transect has 10 points, look for sites with fewer than 10 completed visits, and note detection modality distributions.
4. **Create orientation summaries** – species richness by site, observer workload, yearly totals, detection modality shares.

## Usage expectations
- Treat the workbook as read-only; derive new tables/notebooks elsewhere.
- Cite as "Martinique Breeding Bird Monitoring, 2012–2025" in your report.
- When sharing subsets, export copies rather than modifying the raw extract.

Good luck, and remember to tie your EDA back to the project brief! ⚡️
