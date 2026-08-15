# Future Scope — Road Accident Insight Explorer

This document captures what was deliberately cut from v1.0 (per the Day 1 scoping
decision) and how the project could grow if development continued.

## Why these were cut from v1.0

On Day 1, predictive risk modeling, live data feeds, and user accounts were pushed
out of scope. With 9 build days remaining, the choice was between a polished,
reliable v1.0 with a narrower feature set, or an ambitious build that risked
shipping broken or unfinished. The narrower scope won, and the project shipped
on time (Day 9) as a result.

## 3-Month Horizon

- **Predictive hotspot modeling** — a basic classification model (e.g. logistic
  regression or gradient boosting) predicting relative accident risk by location,
  time, and weather, surfaced as an additional map layer rather than replacing
  the descriptive hotspot map.
- **Multi-year data** — extend beyond the single 2023 STATS19 dataset to allow
  year-over-year trend comparison.
- **Mobile layout pass** — audit and fix the sidebar/filter experience on small
  screens (Streamlit's default layout needs explicit handling here).
- **Automated data refresh** — a scheduled job (e.g. GitHub Actions) that pulls
  the latest DfT STATS19 release and re-runs `etl.py` on a cadence, instead of
  requiring a manual re-download.

## 6-Month Horizon

- **User accounts and saved views** — let a user save a specific filter
  combination (e.g. "Fatal accidents, Fog, Fridays") and return to it, which was
  explicitly deferred from v1.0.
- **Live/near-live data feed** — if a suitable near-real-time UK collision feed
  exists, move off the static annual CSV/parquet pipeline.
- **Comparative view** — side-by-side comparison of two filter selections (e.g.
  two different regions or two different years) rather than one filtered view
  at a time.
- **API layer** — expose the cleaned dataset and aggregate insights via a small
  API so the underlying data/insights can be consumed outside the Streamlit UI.

## 12-Month Horizon

- **Full predictive risk system** — the "high-risk zone forecasting" idea that
  was explicitly deferred on Day 1, now built on a full year (or more) of
  historical data, with proper train/test validation and documented model
  limitations (an accident-risk model has real stakes if misused — this needs
  care, not just accuracy).
- **Multi-country / multi-source support** — generalize the ETL pipeline beyond
  the UK's STATS19 schema so the same app could load comparable open datasets
  from other countries.
- **Public-facing insight reports** — auto-generated periodic (e.g. monthly)
  summary reports rather than only on-demand filtered exploration.

## Explicitly Not Planned

Anything requiring PII, real-time personal location tracking, or law-enforcement
integration is out of scope for this project's lifetime — it is a public-data
exploration tool, not a surveillance or enforcement product.
