# Editorial guide for the AI Briefing site

Every scheduled run that writes a briefing or a research radar follows this
guide. The site is
public, so the rules on copyright and privacy below are not optional.

## Publishing schedule

- **Briefings:** Sunday, Tuesday and Thursday mornings (Asia/Riyadh). Each
  issue covers every newsletter received since the previous issue, so a
  Tuesday issue covers Saturday to Monday, and so on. The file is named by
  the publication date and carries a `covers` range. Days before 24 November
  2026 were published one file per day without `covers`; leave them as they
  are.
- **Research radar:** every Saturday, covering the previous 7 days of
  research alerts. See "Research radar" below.

## Briefing sources

All in Fatima's Gmail. Ignore welcome, sign-up, account and "confirm your
email" messages, and anything that is only an advert.

- AlphaSignal: `news@alphasignal.ai`
- Forward Future: `astro@forwardfuture.ai`
- One Useful Thing (Ethan Mollick): `oneusefulthing@substack.com`
- Import AI (Jack Clark): `importai@substack.com`
- SemiAnalysis: `semianalysis@substack.com` (often partly paywalled: use
  only what the email itself contains)
- The Neuron: sender domain `theneurondaily.com`
- Arabian Business (Gulf Insight newsletter): search Gmail for
  `"Arabian Business" OR arabianbusiness` and use the sender you find.
  Use it mainly for the Saudi and region lens.

Gmail query for a briefing (adjust the date window):
`(from:news@alphasignal.ai OR from:astro@forwardfuture.ai OR from:oneusefulthing@substack.com OR from:importai@substack.com OR from:semianalysis@substack.com OR from:theneurondaily.com OR "Arabian Business" OR from:arabianbusiness.com) after:YYYY/MM/DD`

- Skip every sponsored block ("Presented by", "Sponsored by", "In partnership
  with", "Powered by", ads, discount codes, event promotions).
- When several newsletters cover the same story, write it once and list all
  of them in `sources`.

## Writing rules

- Write everything in your own words. Never copy sentences from the
  newsletters. No quotes longer than a few words, and at most one per day.
- Plain English, short sentences. Never use em-dashes (the build script
  rejects them). Use colons, commas or full stops instead.
- Keep each issue to roughly 500 words of visible text.
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
  "date": "2026-11-24",
  "covers": {"from": "2026-11-21", "to": "2026-11-23"},
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
  "idea_kids": {
    "title": "Something to create for children",
    "pitch": "One or two sentences: a game, book, activity kit, workshop or simple app made for children, inspired by the day's theme.",
    "age": "8 to 12",
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

- `idea_kids`: an idea for something to create for children aged 15 and
  under (a game, picture book, card set, classroom kit, workshop or simple
  app), inspired by the same day's theme. Hands-on and offline-friendly where
  possible; never something that collects children's personal data or asks
  them to share it with an AI tool. Culturally appropriate for Saudi Arabia.
  `age` is a range within 4 to 15. Plain language, like the other fields.
- `covers`: required for every issue from 24 November 2026 onwards. `from`
  is the day after the previous issue's `covers.to` (or the previous issue's
  date for older daily files); `to` is the day before publication.
- `top_stories`: 4 or 5 per issue (fewer only if the period is thin). Pick
  the most important stories across all sources and days, not one per
  newsletter. The page must still read as one page of roughly 500 words.
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


## Research radar (`data/research/YYYY-MM-DD.json`)

Published every Saturday, named by the Saturday's date, covering the 7 days
before it.

Sources (Fatima's Gmail):

- arXiv daily listings from `cs@arxiv.org` / `no-reply@arxiv.org` for
  Human-Computer Interaction and Computers and Society. Each listing holds
  dozens of abstracts: scan titles and abstracts, do not summarise them all.
- Journal alerts from Springer Nature (`nature.com`, `springernature.com`),
  currently Nature Human Behaviour and Humanities and Social Sciences
  Communications. Add NEJM AI (`nejm.org`) if alerts start arriving.
- Ignore account, registration and welcome emails.

Gmail query: `(from:arxiv.org OR from:nature.com OR from:springernature.com OR from:nejm.org) after:YYYY/MM/DD -subject:(welcome OR registration OR subscribe OR "Important Information")`

Selection: pick 5 to 8 papers most relevant to behavioural science, human
trust and decisions with AI, health, public policy, education, work, culture,
and Saudi Arabia or the Gulf. Prefer empirical studies (experiments, RCTs,
field studies, large surveys) over opinion pieces. Prefer peer-reviewed
journal articles when two papers are equally relevant, and label preprints
clearly as not yet peer-reviewed.

```json
{
  "date": "2026-11-28",
  "covers": {"from": "2026-11-21", "to": "2026-11-27"},
  "question": "Plain question that opens the radar?",
  "reflection": "One original, plain sentence on how this research could help people and societies.",
  "one_line": "The single most useful takeaway from this week's research.",
  "papers": [
    {
      "title": "The paper's real title, exactly as published",
      "authors": "First author et al.",
      "venue": "Nature Human Behaviour | arXiv cs.HC | ...",
      "kind": "Journal article | Preprint (not peer-reviewed)",
      "study_type": "Randomised experiment | Field study | Survey | Review | Modelling | ...",
      "summary": "What they did and found, 1 to 2 plain sentences in your own words.",
      "why": "Why it matters for a behavioural-science and research consultancy in Saudi Arabia, 1 sentence.",
      "audience": ["lay", "builder", "decision"],
      "tags": ["trust", "health"],
      "link": "https://arxiv.org/abs/... or https://doi.org/... (the paper's public page)"
    }
  ],
  "themes": ["2 to 4 short patterns across this week's papers."]
}
```

Rules: never copy abstract sentences; the paper title is the only text
reproduced verbatim. Links must be the paper's public page (arXiv abs page or
DOI link), never a tracking link from the email. Same plain-language,
no-em-dash and no-client-names rules as the briefings.

After writing, run `python3 scripts/build.py` (it also rebuilds
`data/research_index.json`), commit and push as for briefings.
