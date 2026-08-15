# 30-Day Growth Plan — Road Accident Insight Explorer

A realistic roadmap taking the v1.0.0 MVP toward a significantly more complete
product. One milestone per day, each building on the previous. Built around
the actual stack: Streamlit, pandas, Plotly, Parquet, Streamlit Community
Cloud, GitHub.

## Week 1 — Harden what exists

- **Day 1:** Add a `requirements.txt` version pin audit — confirm `streamlit`,
  `plotly`, and `pyarrow` versions are pinned, not just `pandas`. Re-deploy and
  confirm the app still builds clean.
- **Day 2:** Add basic input validation / empty-state handling — confirm the
  app doesn't break if a filter combination returns zero rows.
- **Day 3:** Mobile layout pass on the filter sidebar and charts.
- **Day 4:** Add GitHub repo topics, a repo description, and a social preview
  image.
- **Day 5:** Write a non-technical summary paragraph at the top of the README
  (what it does, who it's for) before the technical details.
- **Day 6:** Add a "Data last updated" note and a link back to the DfT source
  page directly in the app UI, not just the README.
- **Day 7:** Review week 1 — confirm the app still deploys cleanly end to end.

## Week 2 — Extend the data layer

- **Day 8:** Investigate whether DfT STATS19 has additional years available;
  document what a multi-year merge would require.
- **Day 9:** Extend `etl.py` to accept a year parameter instead of a hardcoded
  filename.
- **Day 10:** Add a second year of data and confirm the pipeline output is
  still 99%+ retention like the original.
- **Day 11:** Add a year filter to the Streamlit UI.
- **Day 12:** Update trend charts to optionally compare year-over-year.
- **Day 13:** Add tests for `generate_insights()` covering the Day 5 edge case
  (filtered-to-100%-severe) so it can't regress silently.
- **Day 14:** Review week 2 — confirm multi-year data doesn't break map/chart
  performance.

## Week 3 — Insight and UX depth

- **Day 15:** Add a "compare two selections" view (e.g. two regions or two
  years side by side).
- **Day 16:** Add a downloadable filtered-data export (CSV) for users who want
  the underlying rows.
- **Day 17:** Add a short in-app methodology note explaining what counts as
  "Fatal/Serious/Slight" per STATS19 definitions.
- **Day 18:** Polish the hotspot map further — evaluate cluster labels or
  zoom-dependent detail.
- **Day 19:** Add loading-state indicators for slower filter combinations.
- **Day 20:** Accessibility pass — color contrast on the severity chart,
  alt text where relevant.
- **Day 21:** Review week 3 — get outside feedback (a non-technical friend
  or colleague) and log what confused them.

## Week 4 — Toward the predictive layer and wrap-up

- **Day 22:** Research a simple baseline model for accident-risk scoring by
  location/time/weather (no deployment yet — research and design only).
- **Day 23:** Build the baseline model offline against the cleaned parquet
  data; evaluate honestly, including where it's unreliable.
- **Day 24:** Decide, with the same discipline as Day 1 of the original
  build: is this model good enough to ship, or does it need another cycle?
  Document the decision either way.
- **Day 25:** If shipping: add the risk layer as an optional, clearly-labeled
  map overlay (not a replacement for the descriptive hotspot map).
- **Day 26:** If not shipping: document findings in an updated
  `future-scope.md` and move on — don't let it block the rest of the plan.
- **Day 27:** Update the README and screenshots to reflect the 30-day
  changes.
- **Day 28:** Tag and release v1.1.0 with a changelog summarizing what
  changed since v1.0.0.
- **Day 29:** Write a short retrospective post on what the 30 extra days
  added, in the same style as the original 60-day challenge posts.
- **Day 30:** Final review — confirm the deployed app, the repo, and the
  documentation are all consistent with each other.
