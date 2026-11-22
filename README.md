# AI Briefing

AI news and research, read through a Saudi and behavioural-science lens.

**Live site:** https://xfsala.github.io/ai-briefing/

## Tabs

- **Briefings:** a one-page briefing three times a week, with a searchable
  archive grouped by month.
- **Research:** a weekly radar of new studies on AI and people, with links to
  each paper.
- **What this means:** a guide to reading the site.
- **Who & What:** a glossary, plus every company, person and organisation
  mentioned, with official links.
- **Mindmap:** industries, concepts and organisations, filterable by audience
  (lay users, builders, decision-makers).

## How it updates

Scheduled Claude tasks write the content, following
[`EDITORIAL_GUIDE.md`](EDITORIAL_GUIDE.md):

| When (Riyadh time) | What | File |
|---|---|---|
| Sunday, Tuesday, Thursday, before 7:30 am | Briefing covering the days since the last one | `data/days/YYYY-MM-DD.json` |
| Saturday, about 8 am | Research radar covering the past 7 days | `data/research/YYYY-MM-DD.json` |

Each run then executes `python3 scripts/build.py` to rebuild the indexes,
glossary, entity list and mindmap, and pushes. GitHub Pages publishes the
change within a minute or two.

## Sources

- **Briefings:** AlphaSignal, Forward Future, One Useful Thing, Import AI,
  SemiAnalysis, The Neuron, AI Made Simple and Arabian Business.
- **Research:** arXiv (cs.HC and cs.CY) and Springer Nature journal alerts.

Summaries are original. The newsletters and papers remain the property of
their publishers.
