"""Generates work/<slug>/index.html from the case-study entries below (one shared template).
Run: python3 tools/build_case_studies.py"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]

NAV = """<header class="nav" id="nav">
  <div class="nav-in">
    <a class="brand" href="/" aria-label="Bingcheng Liu home">BL<span>.</span></a>
    <nav class="nav-links" aria-label="Main navigation">
      <a href="/#work">Work</a>
      <a href="/#approach" class="hide-s">Approach</a>
      <a href="/#more">Projects</a>
      <a href="/#about" class="hide-s">About</a>
      <a href="https://github.com/bensonliu-sudo">GitHub ↗</a>
    </nav>
  </div>
</header>"""


def frame(cs):
    if cs["frame"] == "win":
        bar = f'<div class="frame-bar" aria-hidden="true"><span>{cs["frame_label"]}</span><em>– □ ×</em></div>'
        cls = "frame win rv"
    else:
        bar = f'<div class="frame-bar" aria-hidden="true"><i></i><i></i><i></i><span>{cs["frame_label"]}</span></div>'
        cls = "frame rv"
    return (f'<div class="{cls}">{bar}<video data-auto src="{cs["video"]}" poster="{cs["poster"]}" muted loop playsinline '
            f'preload="metadata" controls aria-label="{escape(cs["video_label"])}"></video></div>')


def page(cs, nxt):
    meta = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in cs["meta"])
    blocks = []
    for i, b in enumerate(cs["blocks"]):
        items = "".join(f"<li>{x}</li>" for x in b.get("points", []))
        blocks.append(f'''        <div class="block{' flip' if i % 2 else ''}">
          <figure class="shot rv"><a href="{b["img"]}"><img src="{b["img"]}" alt="{escape(b["alt"])}" loading="lazy"></a></figure>
          <div class="rv d1"><div class="k">{b["k"]}</div><h3>{b["h"]}</h3><p>{b["p"]}</p>{f"<ul>{items}</ul>" if items else ""}</div>
        </div>''')
    stats = "".join(f'<div class="stat rv{" d%d" % i if i else ""}"><b>{v}</b><span>{t}</span></div>' for i, (v, t) in enumerate(cs["stats"]))
    stats2 = "".join(f'<div class="stat rv{" d%d" % i if i else ""}"><b>{v}</b><span>{t}</span></div>' for i, (v, t) in enumerate(cs.get("stats2", [])))
    note = f'<p class="stats-note rv">{cs["stats_note"]}</p>' if cs.get("stats_note") else ""
    note2 = f'<p class="stats-note rv">{cs["stats2_note"]}</p>' if cs.get("stats2_note") else ""
    lessons = "".join(f'<div class="lesson rv{" d1" if i % 2 else ""}"><b>{h}</b><p>{t}</p></div>' for i, (h, t) in enumerate(cs["lessons"]))
    limits = "".join(f"<li>{x}</li>" for x in cs["limits"])
    problem = "".join(f"<p>{x}</p>" for x in cs["problem"])
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cs["title_plain"]} — Bingcheng Liu</title>
<meta name="description" content="{escape(cs["summary"])}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#050b1a">
<meta property="og:title" content="{cs["title_plain"]} — Bingcheng Liu">
<meta property="og:description" content="{escape(cs["summary"])}">
<meta property="og:image" content="{cs["poster"]}">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{NAV}

<main id="main">
  <section class="cs-hero">
    <div class="wrap">
      <a class="back" href="/#work"><span aria-hidden="true">←</span> All work</a>
      <div class="eyebrow">{cs["eyebrow"]}</div>
      <h1>{cs["title_html"]}</h1>
      <p class="lede">{cs["summary"]}</p>
      <dl class="cs-meta">{meta}</dl>
    </div>
  </section>

  <section class="cs-video"><div class="wrap">{frame(cs)}</div></section>

  <section class="cs-sec">
    <div class="wrap cs-two">
      <div class="rv"><div class="eyebrow">The problem</div><h2>{cs["problem_h"]}</h2></div>
      <div class="prose rv d1">{problem}</div>
    </div>
  </section>

  <section class="cs-sec">
    <div class="wrap">
      <div class="rv"><div class="eyebrow">What I built</div><h2>{cs["built_h"]}</h2></div>
      <div class="blocks">
{chr(10).join(blocks)}
      </div>
    </div>
  </section>

  <section class="cs-sec">
    <div class="wrap">
      <div class="rv"><div class="eyebrow">By the numbers</div></div>
      <div class="stats" style="margin-top:30px">{stats}</div>{note}
      {f'<div class="stats" style="margin-top:40px">{stats2}</div>{note2}' if stats2 else ""}
    </div>
  </section>

  <section class="cs-sec">
    <div class="wrap">
      <div class="rv"><div class="eyebrow">How it was built</div><h2>{cs["lessons_h"]}</h2></div>
      <div class="lessons">{lessons}</div>
      <div class="limits rv"><div class="eyebrow" style="margin-bottom:14px">Scope and limits</div><ul>{limits}</ul></div>
    </div>
  </section>

  <a class="next wrap" href="/work/{nxt["slug"]}"><div class="eyebrow">Next case study</div><b>{nxt["title_plain"]} <i aria-hidden="true">→</i></b></a>
</main>

<footer><div class="foot"><span>© 2026 Bingcheng Liu</span><span>Full-stack · AI agents · Finance</span></div></footer>
<script src="/assets/site.js"></script>
</body>
</html>
'''


MF = "/assets/multifactor"
YRD = "/assets/yrd"
FR = "/assets/fris"
CASES = [
    dict(
        slug="fris", eyebrow="Case study · 01 · Risk intelligence platform",
        title_plain="FRIS", title_html="FRIS <em>risk intelligence</em>",
        summary="A risk-intelligence platform that monitors around 220 asset managers. It gathers news, filings and regulators' releases through seven collectors, has an LLM classify every development into 13 risk categories on a 20-point scale, and turns them into a deterministic, explainable risk score for each entity.",
        meta=[("Role", "Sole developer, built for an employer: data, AI pipeline, backend, frontend, deployment"), ("Timeline", "February to October 2026"),
              ("Stack", "Python · FastAPI · PostgreSQL · LLM classification · Next.js · Recharts · Azure"), ("Status", "Deployed to the cloud with sign-in; private repository")],
        frame="browser", frame_label="fris · risk dashboard", video=f"{FR}/demo.mp4", poster=f"{FR}/poster.jpg",
        video_label="71-second screen recording of FRIS running on fictional entities and synthetic data",
        problem_h="Early warning, buried<br><em>in thousands of articles.</em>",
        problem=["Analysts who oversee fund managers on behalf of clients need to know early when a manager runs into trouble: redemptions gated, an investor class action, a regulator's probe. The signals are spread across <b>thousands of articles a week</b>, in many sources and several languages.",
                 "Most of it is noise. The same story is syndicated a dozen times, law-firm press releases make routine investigations sound alarming, and news about a parent company is not always news about its local subsidiary. A keyword alert drowns; a person cannot read it all.",
                 "FRIS turns that stream into <b>one number per entity that an analyst can defend</b>: where it came from, which development set it, and what would bring it down."],
        built_h="From raw news to a score<br><em>you can defend.</em>",
        blocks=[
            dict(img=f"{FR}/dashboard.jpg", alt="FRIS dashboard with AI briefing and latest risk events", k="01 · INGESTION AND DEDUPLICATION", h="Eight sources, one clean event stream",
                 p="Seven collectors pull from Google News, Yahoo Finance, SEC EDGAR and four regulators (ASIC, FCA, ESMA, SFC). Full text is extracted where it can be, and duplicates are removed before anything is scored.",
                 points=["Deduplication by URL, title similarity and content hash, then 7-day semantic clustering into incidents", "A representative article per incident, chosen by content and source authority", "Parent-to-subsidiary propagation that judges whether a parent's news really applies"]),
            dict(img=f"{FR}/waterline.jpg", alt="Risk Score Waterline chart", k="02 · AI JUDGES, ARITHMETIC SCORES", h="The LLM classifies; it never sets the score",
                 p="Each development is classified by an LLM into one of 13 categories on a 20-point scale, under explicit consistency rules. The entity's score is then pure arithmetic: the highest category, with cooling over time and credit for mitigations.",
                 points=["Law-firm solicitation releases capped, a 33-firm blacklist, repeat alerts merged", "Category scores cool after 60 days, or 180 while a legal matter is pending", "The waterline shows every move, with one marker per assessed development"]),
            dict(img=f"{FR}/analysis.jpg", alt="Radar of category scores and written risk analysis", k="03 · EXPLAINABLE BY CONSTRUCTION", h="Every rating explains itself",
                 p="The category radar shows what is driving the score today. The written analysis is generated from the scorer's own record, not free-form text, so every sentence traces back to a scored development.",
                 points=["Rating, risk profile, trajectory, last 90 days, mitigation, open matters", "The same text goes into the PDF report for clients"]),
            dict(img=f"{FR}/rankings.jpg", alt="Entity risk rankings table", k="04 · BUILT FOR CLIENT WORK", h="Rankings, watchlists, reports",
                 p="A multi-layer ranking across all entities, client watchlists, regional and asset-class filters, a top-movers view, PDF export, and sign-in so clients see only their own watchlist."),
        ],
        stats=[("288,534", "articles collected since launch"), ("114,810", "events classified by the LLM after deduplication"),
               ("9,485", "incidents clustered from those events"), ("220", "asset managers and entities monitored")],
        stats_note="Cumulative, as of the weekly run of 18 October 2026.",
        stats2=[("~1,960", "new articles in a typical week, from 7 collectors"), ("1.5<small>%</small>", "of them are genuine risk developments; 88% are irrelevant"),
                ("2<small>h</small> 46<small>m</small>", "for the whole weekly pipeline, collection to scoring"), ("100<small>%</small>", "of events classified successfully that week")],
        stats2_note="A typical week: 12 to 18 October 2026.",
        lessons_h="Most of the work is<br><em>removing noise.</em>",
        lessons=[("Keep AI out of the arithmetic", "The model classifies and explains; the score is a deterministic function of the classified record. That makes every rating reproducible and every change attributable."),
                 ("Calibrate the judge against a gold set", "A hand-labelled gold standard and regression runs check the classifier after every prompt or taxonomy change, so improvements are measured rather than assumed."),
                 ("Design for the noise you actually see", "Syndication, law-firm solicitations, parent and subsidiary confusion and multi-language duplicates each got a specific, tested rule."),
                 ("Make it operable", "One command runs the weekly update end to end in under three hours, backs up the database and writes the change log, so the system does not depend on its author being there.")],
        limits=["A monitoring signal for analysts, not investment advice or a credit rating.",
                "Coverage depends on what sources publish; paywalls limit full text for some articles.",
                "The recording runs the real frontend against a demo backend: every manager, client, headline and figure in it is fictional, and the employer's name is removed."],
    ),
    dict(
        slug="multifactor-scoring", eyebrow="Case study · 02 · Equity research tooling",
        title_plain="Multi-factor stock scoring", title_html="Multi-factor<br><em>stock scoring</em>",
        summary="A full-stack tool for equity research teams: researchers set the factors, directions and weights, and the tool turns them into exact, reproducible scores, rankings and an auditable stock pool, explaining every result factor by factor.",
        meta=[("Role", "Sole developer: design, backend, frontend, tests"), ("Year", "2026"), ("Stack", "Python · FastAPI · NumPy · SQLite · vanilla JS"), ("Status", "Working tool; private repository, source on request")],
        frame="browser", frame_label="multi-factor-scoring · live walkthrough", video=f"{MF}/demo.mp4", poster=f"{MF}/poster.jpg",
        video_label="37-second screen recording of the multi-factor scoring tool on synthetic data",
        problem_h="Pools built by hand,<br><em>hard to explain.</em>",
        problem=["Research teams often build their candidate pools in spreadsheets: standardise a handful of factors, weight them, sort, take the top N. It works until someone asks <b>why a stock is in the pool</b>, or what changed since last week.",
                 "A changed weight leaves no trace, rounding differs between sheets, and outliers quietly dominate a score. The scoring itself is simple; making it <b>exact, explainable and reproducible</b> is the real work.",
                 "This tool takes the factor choices as given and does that part properly. Choosing factors, optimising weights and backtesting are deliberately out of scope."],
        built_h="A scoring layer that<br><em>shows its working.</em>",
        blocks=[
            dict(img=f"{MF}/overview.jpg", alt="Stock pool overview", k="01 · SCORING ENGINE", h="Exact, deterministic scores",
                 p="Every factor is winsorised at k standard deviations, standardised, signed by its direction and weighted. The same data and configuration always produce the same pool, down to the last digit.",
                 points=["Optional industry-neutral standardisation", "Missing values handled explicitly, never silently dropped", "Bit-exact regression against an independent reference"]),
            dict(img=f"{MF}/sandbox.jpg", alt="Weight sandbox showing rank changes", k="02 · WEIGHT SANDBOX", h="Change a weight, see the consequences",
                 p="Drag any weight and the pool re-scores instantly. The table shows which stocks entered or left the pool and how far each one moved, against the last official run.",
                 points=["Sandbox runs never overwrite the official result", "Filter to entered, exited, up or down", "One click to save a sandbox as the new official run"]),
            dict(img=f"{MF}/detail.jpg", alt="Factor-level score breakdown", k="03 · CUTOFF EXPLANATION", h="Why this stock is in, or out",
                 p="For any stock, a factor-by-factor breakdown: raw and clipped values, standardised score, weight and contribution, plus the distance to the rank-N cutoff and the factor that drives it."),
            dict(img=f"{MF}/history.jpg", alt="Run history", k="04 · AUDIT TRAIL", h="Every run can be reproduced",
                 p="Each run is stored with a snapshot of its configuration and a fingerprint of its input data, so any past pool can be traced and rebuilt. Results export to CSV."),
        ],
        stats=[('5,000', "stocks × 10 factors scored per request in the stress test"), ('&lt; 0.6<small>s</small>', "slowest full HTTP request, scoring and persistence included"),
               ('166', "automated tests, including bit-exact regression against a reference"), ('15', "documented AI errors caught by independent review and fixed")],
        lessons_h="Built with AI,<br><em>verified</em> like production.",
        lessons=[("Pin down the spec first", "Every ambiguous rule (rounding, ties, missing values, clipping order) was written down and checked against an independent reference implementation before features were built on it."),
                 ("Ship in gated packages", "Engine, service, frontend and performance were separate packages. Each was frozen, hashed and reviewed before the next one started."),
                 ("Independent adversarial review", "A second AI re-computed results, injected faults and replayed real usage. Fifteen genuine errors were found this way; each one is documented with its fix."),
                 ("Measure, don't assume", "Performance claims come from a stress test at 5,000 stocks and 10 factors, timed end to end through the HTTP API.")],
        limits=["Scores one cross-section at a time; multi-period data and incremental updates are future work.",
                "No factor research, weight optimisation or backtesting, by design.",
                "Demo data is synthetic: 200 sample companies across 10 industries."],
    ),
    dict(
        slug="yrd-assistant", eyebrow="Case study · 03 · Workflow automation",
        title_plain="YRD Assistant", title_html="YRD <em>Assistant</em>",
        summary="A desktop assistant that runs a financial publisher's daily report workflow: it finds the morning market commentary in Outlook, writes each section into the right WordPress draft, and drafts the confirmation email, while a person stays in charge of publishing.",
        meta=[("Role", "Sole developer, built for an employer"), ("Timeline", "March to May 2026"), ("Stack", "Node.js · Electron · Python · Outlook COM · WordPress REST API"), ("Status", "Delivered; private repository")],
        frame="win", frame_label="YRD Assistant · desktop app", video=f"{YRD}/demo.mp4", poster=f"{YRD}/poster.jpg",
        video_label="46-second screen recording of YRD Assistant running on synthetic content",
        problem_h="A daily copy-paste job<br><em>that had to be perfect.</em>",
        problem=["Every business day the publisher releases a bonds report and an equities report. The market commentary arrives by email in the morning, and someone has to copy <b>four sections into two WordPress drafts</b>, each under exactly the right heading, without disturbing the charts, tables and ads around them.",
                 "Then they confirm by email. It is repetitive, time-boxed, and the emails are messier than they look: reply threads carry yesterday's commentary, section order changes, headings run into the first sentence.",
                 "The goal was to automate the tedious part <b>without taking the human out of the loop</b>: nothing is ever published automatically."],
        built_h="Three layers, one<br><em>guided workflow.</em>",
        blocks=[
            dict(img=f"{YRD}/dryrun.jpg", alt="Dry run result with matched drafts", k="01 · MAIL INTAKE", h="Find the right email, read it robustly",
                 p="A Python intake step scans today's Outlook inbox newest first and recognises the commentary by its four section headings rather than a fixed intro sentence.",
                 points=["Ignores quoted reply threads, so old commentary never overrides today's", "Works with any section order, inline headings and divider lines", "Extracts the business date and retries while the mailbox is still starting up"]),
            dict(img=f"{YRD}/draft.jpg", alt="WordPress draft with inserted sections highlighted", k="02 · DRAFT UPDATER", h="Write into WordPress, never publish",
                 p="A Node service finds the latest bonds and equities drafts through the WordPress REST API, matches each section heading in the post HTML and inserts the text beneath it.",
                 points=["Dry run first: validates every match before anything is written", "Cleans empty filler markup so spacing matches the house style", "Charts, tables and ad tags are left exactly as they were; posts stay in Draft"]),
            dict(img=f"{YRD}/done.jpg", alt="Completed workflow with confirmation draft ready", k="03 · DESKTOP ASSISTANT", h="One screen, five steps, a human in charge",
                 p="An Electron app wraps the scripts in a guided flow: scan, review the dry run, generate drafts, publish manually in WordPress, then create the confirmation email as a reply-all draft for review.",
                 points=["Auto-scans during the morning window and retries every five minutes", "Resettable run state, so a new operator can test without restarting anything", "Browser fallback when the desktop shell is unavailable"]),
        ],
        stats=[("4", "commentary sections placed into 2 reports every business day"), ("5", "guided steps from inbox to confirmation email"),
               ("11", "real production issues logged, root-caused and fixed"), ("0", "automatic publishes: a person always signs off")],
        lessons_h="Real inputs are<br><em>messier than the spec.</em>",
        lessons=[("Match on meaning, not on literals", "Early versions keyed on a fixed intro sentence and exact heading names. Real emails broke both, so recognition moved to normalised section keys that tolerate variants and reordering."),
                 ("Verify against real content", "Spacing bugs only showed up in the live drafts' raw HTML, not in local templates. Fixes were checked against the real post content before release."),
                 ("Keep a maintenance log", "Every fault gets a symptom, root cause, fix and status. Eleven entries in three months show where the fragile edges are."),
                 ("Automate the work, not the judgement", "The tool prepares everything up to the publish button and drafts the follow-up email; deciding to publish and send stays with a person.")],
        limits=["Windows only: mail intake depends on the Outlook desktop client through COM.",
                "An internal tool for one publishing workflow, not a general product.",
                "The recording runs the real interface against a demo backend with synthetic commentary; publisher names and addresses are removed."],
    ),
]

for i, cs in enumerate(CASES):
    out = ROOT / "work" / cs["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(cs, CASES[(i + 1) % len(CASES)]))
    print("wrote", out.relative_to(ROOT))
