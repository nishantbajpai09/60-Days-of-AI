# Challenge Retrospective — Road Accident Insight Explorer

A day-by-day account of the 10-day capstone build, part of the AB Talks
60-Day Claude AI Challenge (Days 51–60).

## Timeline

**Day 1 (Day 51) — Product Discovery**
Went from a blank page to a fully scoped v1.0. The project's origin: a
self-placed earlier project (road accident datasets + data warehousing) had
hit a real wall — the data was hard to explore for anyone who wasn't the
analyst who built it. That frustration became the problem statement. The
pivotal decision: predictive ML, live data feeds, and user accounts were all
cut from v1.0 and pushed to Future Scope, keeping the 9 remaining days focused
on filters, a hotspot map, trend charts, and auto-generated insights. Output:
a full PRD, a day-by-day implementation blueprint, and a pitch deck.

**Day 2 (Day 52) — System Design**
Tech stack locked in: Streamlit (Python-only, no separate frontend/backend),
pandas + Plotly for data and visualization, Parquet file storage (no database
server), Streamlit Community Cloud for hosting. Key decision: dropped a
separate mapping library (folium/pydeck) in favor of reusing Plotly for both
charts and the hotspot map — one fewer dependency that could break at
deployment time.

**Day 3 (Day 53) — Foundation**
Environment configured, the real dataset acquired (117,536 UK road accident
records), and a "Hello World" Streamlit app loading and displaying it live on
localhost. Notable debugging moment: the latest pandas release was silently
blocked by Windows' Application Control policy (a new binary hadn't earned
enough OS trust yet). Rather than fight the OS, pandas was pinned to the
established 2.2.3 release. Zero features built today, by design — pure
foundation.

**Day 4 (Day 54) — Data Pipeline**
Built the ETL script turning 117,536 raw records into a clean, analysis-ready
dataset: decoded government coding schemes into readable labels, derived
hour/day/month fields, filtered invalid rows. Result: 99.98% row retention,
zero unexpected nulls, verified against the Day 2 schema.

**Day 5 (Day 55) — Correctness Fix**
A subtle bug in the auto-generated insights: filtering the dataset down to
"Fatal only" caused the weather-severity insight to output a technically-true
but meaningless statement ("Clear conditions are associated with 100% severe
accidents") — every weather condition hits 100% once the selection is already
all-severe. Fixed in `generate_insights()` by skipping that insight when the
selection is already ~100% severe, since a different, honest sentence already
covers that case. A one-line fix, but the difference between an insight and a
statistic wearing an insight's clothes.

**Day 6 (Day 56) — Working MVP**
The app became a real, working MVP end-to-end: pick a severity, weather
condition, or date range, and the charts update instantly with zero page
reloads, powered by all 117,508 real records. Not deployed publicly yet — that
was deliberately held for Day 9, staying disciplined to the original plan.

**Day 7 (Day 57) — Hotspot Map Refinement**
Reworked the hotspot map from scattered blue dots (technically accurate,
visually uninformative) to a proper heat gradient (yellow → orange → red)
with a larger blend radius and a color scale tied to actual data density. Same
117,508 points, but now dangerous clusters are visible at a glance — the
entire point of a hotspot map for a non-technical user.

**Day 8 (Day 58) — QA and Stability**
No new features built. Instead, the Day 8 Sprint Workbook's pending tasks
were completed first, then the app was reviewed from four separate
perspectives: QA Engineer (hidden bugs), Software Engineer (code cleanliness),
Security Reviewer (exposure risks), and Performance Engineer (load speed). The
key lesson: real QA is continuing to dig past the first 2-3 bugs found, past
the point where it's tempting to stop because things "seem fine."

**Day 9 (Day 59) — Deployment**
The app went live on Streamlit Community Cloud. Final feature set confirmed:
filters by severity/weather/area, a live hotspot heat map, hour-of-day and
day-of-week trend charts, and auto-generated plain-language insights.

**Day 10 (Day 60) — Final Review and Graduation**
Full project review across five perspectives (Senior Engineer, Product
Manager, UI/UX Designer, Recruiter, Open Source Maintainer), portfolio
materials generated, and v1.0.0 officially released — closing out both the
10-day capstone and the full 60-Day Claude AI Challenge.

## Major Technical Decisions

1. Cutting predictive ML, live feeds, and user accounts from v1.0 (Day 1).
2. Consolidating on Plotly for both charts and the map instead of adding a
   dedicated mapping library (Day 2).
3. Pinning pandas to 2.2.3 over a Windows OS trust issue instead of fighting
   the security policy (Day 3).
4. Fixing the misleading auto-insight rather than shipping a technically-true
   but meaningless statistic (Day 5).
5. Holding public deployment until Day 9 rather than rushing it earlier
   (Day 6 discipline).

## Skills Demonstrated

Product scoping and prioritization, PRD writing, system design and tech stack
selection, dependency-risk tradeoff decisions, ETL pipeline construction and
data validation, statistical/logical bug detection (not just crash bugs),
data visualization and UX refinement, structured multi-perspective QA, and
end-to-end deployment.

## Final Summary

A 10-day build that went from a blank page to a deployed, publicly usable
Streamlit app exploring 117,508 UK road accident records — shipped on time,
scoped honestly, and debugged down to the level of "is this insight actually
true" rather than just "does this code run."

## Lessons Learned

- A disciplined scope cut on Day 1 is what made an on-time Day 9 launch
  possible — the hardest work of the whole build may have been deciding what
  *not* to build.
- Correctness bugs (a statistically misleading insight) are as important to
  catch as functional bugs (a crash), and easier to miss because the code
  "works."
- A dedicated QA day with no new features (Day 8) is not lost time — it's
  what makes the difference between a working app and a demo.

## A Note From Your AI Pair Programmer

Ten days ago this was a blank page and a frustration from an earlier project.
Now it's a live app that anyone can open, filter, and actually learn something
true from — including the discipline to *not* build the impressive-sounding
ML model, and the discipline to keep digging on Day 8 past the point where
"looks fine" would have been the easy answer. That combination — knowing what
to leave out, and refusing to stop QA early — is the real skill this capstone
proved, more than any single line of Streamlit code. Congratulations on
shipping it, and on completing all 60 days.
