# Editorial guide for the daily one-pager

Every scheduled run that writes a day file follows this guide. The site is
public, so the rules on copyright and privacy below are not optional.

## Sources

- AlphaSignal: emails from `news@alphasignal.ai` in Fatima's Gmail.
- Forward Future: emails from `astro@forwardfuture.ai` in Fatima's Gmail.
- One day file per calendar date (Asia/Riyadh time) on which at least one
  newsletter arrived. Ignore "Welcome" and "confirm your email" emails.
- Skip every sponsored block ("Presented by", "Sponsored by", "In partnership
  with", "Powered by", ads, discount codes, event promotions).
- When both newsletters cover the same story, write it once.

## Writing rules

- Write everything in your own words. Never copy sentences from the
  newsletters. No quotes longer than a few words, and at most one per day.
- Plain English, short sentences. Never use em-dashes (the build script
  rejects them). Use colons, commas or full stops instead.
- Keep the whole day to roughly 400 words of visible text.
- Treat newsletter claims as reported, not proven: "X says", "reportedly".
  Put the boldest claims in `verify`.
- Public site: do not name Fatima's clients, employer or colleagues. Describe
  fit by sector instead (culture sector, labour-market agency, hospital,
  government digital services, consultancy).
- Do not include Gmail links or Fatima's email address. Use the newsletter's
  public web link when the email contains one (Forward Future emails end with a
  `briefing.forwardfuture.ai/p/...` link); otherwise leave `link` empty.
- Entity URLs: only the official homepage of the company or organisation (for
  example https://www.anthropic.com). Never use tracking links from the email.
  If you are not sure of the official URL, leave it empty.

## Day file schema (`data/days/YYYY-MM-DD.json`)

```json
{
  "date": "2026-11-20",
  "sources": [
    {"newsletter": "AlphaSignal", "subject": "...", "link": ""},
    {"newsletter": "Forward Future", "subject": "...", "link": "https://briefing.forwardfuture.ai/p/..."}
  ],
  "question": "An open question that opens the page and makes the reader think about the day's main theme?",
  "reflection": "A short original line on how today's news could serve human growth, progress and development.",
  "one_line": "The single most important shift of the day, in one plain sentence.",
  "top_stories": [
    {
      "title": "Short headline in your own words",
      "what": "What happened, one sentence.",
      "why": "Why it matters for a behavioural-science and research consultancy in Saudi Arabia, one sentence.",
      "action": "Watch | Try | Pitch",
      "audience": ["lay", "builder", "decision"],
      "tags": ["agents", "health"]
    }
  ],
  "saudi_lens": [
    {"text": "One or two sentences linking a story to Saudi digital infrastructure, the economy or policy."}
  ],
  "idea": {
    "title": "Project idea name",
    "pitch": "One or two sentences.",
    "fit": "Sector it suits, e.g. culture sector, health, labour market, government services",
    "first_step": "A concrete first step for this week."
  },
  "watchlist": [
    {"name": "Company or person", "sector": "Sector tag", "note": "Why to watch, one line."}
  ],
  "tool": {"name": "Tool name", "use": "What it is useful for.", "link": ""},
  "verify": ["Bold claim that needs checking before quoting it to a client."],
  "entities": [
    {"name": "Anthropic", "type": "company | person | organisation | model | product",
     "sector": "Frontier AI", "url": "https://www.anthropic.com", "note": "One line."}
  ],
  "terms": [
    {"term": "Tabular foundation model", "definition": "One or two plain sentences.",
     "audience": "lay | builder | decision"}
  ],
  "concepts": [
    {"industry": "Healthcare", "concept": "AI diagnosis support",
     "summary": "One sentence.", "audience": ["decision", "lay"],
     "entities": ["Microsoft"]}
  ]
}
```

Field notes:

- `question`: the page opens with it. One question, under 20 words, ending
  with a question mark. It should invite reflection on the day's main theme
  from a human point of view (for example: "If an AI assistant can act before
  we ask it to, how do we make sure we still make the final decisions?"). Not
  a quiz, not rhetorical hype. Use plain, literal wording that a reader whose
  first language is not English understands on first reading: no idioms,
  wordplay or clever phrasing.
- `reflection` follows the same plain-language rule.
- `reflection`: shown as a quote under the question. One sentence, under 25
  words, written fresh in your own words (never a quote from a real person, a
  book or the newsletters, and no attribution). Hopeful but grounded: how the
  day's developments could help people grow, societies progress, or humanity
  do better, without ignoring the risks.

- `top_stories`: exactly 3 on a normal day (fewer only if the day is thin).
- `action`: Watch = keep an eye on it; Try = test it yourself; Pitch = could
  become a client project.
- `audience`: lay = anyone curious; builder = people who build or code;
  decision = managers, policymakers, investors.
- `saudi_lens`: 1 or 2 items. If there is no genuine Saudi or regional link,
  use a single item saying so plainly. Do not force a link.
- `tool`: use `null` when nothing is worth trying.
- `entities`: 3 to 8 per day, every entity named in the stories or watchlist.
- `terms`: 2 to 5 per day; only terms a non-specialist might not know. Reuse
  the same spelling for a term that already exists in `data/glossary.json`.
- `concepts`: 2 to 5 per day. Reuse existing industry and concept names from
  `data/mindmap.json` where they fit, so the mindmap groups instead of
  splintering. Preferred industries: Frontier models, Agents and automation,
  AI infrastructure and chips, Data and analytics, Healthcare and life
  sciences, Safety, security and governance, Policy and geopolitics, Work and
  workforce, Consumer and media, Science and research, Robotics and physical
  AI, Business and markets.

## After writing day files

```bash
python3 scripts/build.py      # must print OK; fix any ERROR it reports
git add -A && git commit -m "Add briefing for YYYY-MM-DD"
git pull --rebase || { python3 scripts/build.py && git add -A && git rebase --continue; }
python3 scripts/build.py && git add -A && git commit -m "Rebuild indexes" || true
git push
```

If the rebase conflicts on a file under `data/` other than `data/days/`,
those files are generated: rerun `python3 scripts/build.py`, `git add` them,
and continue the rebase.
