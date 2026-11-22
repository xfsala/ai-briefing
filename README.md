# AI Briefing

A daily one-page briefing on AI, built from the AlphaSignal and Forward Future
newsletters and read through a Saudi and behavioural-science lens.

**Live site:** https://xfsala.github.io/ai-briefing/

## Tabs

- **Daily:** today's one-pager and a searchable archive of every past day.
- **What this means:** a guide to reading the briefing.
- **Who & What:** a glossary, plus every company, person and organisation
  mentioned, with official links and the days they appeared.
- **Mindmap:** industries, concepts and organisations, filterable by audience
  (lay users, builders, decision-makers).

## How it updates

A scheduled Claude task runs every morning at 7:30 Riyadh time. It reads the
previous day's newsletters, writes `data/days/YYYY-MM-DD.json` following
[`EDITORIAL_GUIDE.md`](EDITORIAL_GUIDE.md), runs `python3 scripts/build.py` to
rebuild the glossary, entity list and mindmap, and pushes. GitHub Pages
publishes the change within a minute or two.

## Content

Summaries are original. The newsletters remain the property of their
publishers: subscribe at [alphasignal.ai](https://alphasignal.ai) and
[forwardfuture.ai](https://www.forwardfuture.ai).
