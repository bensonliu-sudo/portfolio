"""Generates work/<slug>/index.html from the case-study entries below (one shared template).
Run: python3 tools/build_case_studies.py"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]

NAV = """<header class="nav theme-dark" id="nav">
  <div class="nav-in">
    <a class="brand" href="/" aria-label="Bingcheng Liu home">BL<span>.</span></a>
    <nav class="nav-links" aria-label="Main navigation">
      <a href="/#work">Work</a>
      <a href="/#approach" class="hide-s">Approach</a>
      <a href="/#more">Projects</a>
      <a href="/#about" class="hide-s">About</a>
      <a href="/#contact">Contact</a>
      <a href="https://github.com/bensonliu-sudo" class="hide-s">GitHub ↗</a>
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
    nxt_link = (f'<a class="next wrap" href="/work/{nxt["slug"]}"><div class="eyebrow">Next case study</div><b>{nxt["title_plain"]} <i aria-hidden="true">→</i></b></a>'
                if nxt else '<a class="next wrap" href="/#work" data-home><div class="eyebrow">That was the last one</div><b>Back to all work <i aria-hidden="true">↩</i></b></a>')
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
    stats3 = "".join(f'<div class="stat rv{" d%d" % i if i else ""}"><b>{v}</b><span>{t}</span></div>' for i, (v, t) in enumerate(cs.get("stats3", [])))
    note3 = f'<p class="stats-note rv">{cs["stats3_note"]}</p>' if cs.get("stats3_note") else ""
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
<link rel="stylesheet" href="/assets/site.css?v=20261026a">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{NAV}

<main id="main">
  <section class="cs-hero theme-dark">
    <div class="wrap">
      <a class="back" href="/#work" data-home><span aria-hidden="true">←</span> All work</a>
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
      {f'<div class="stats" style="margin-top:40px">{stats3}</div>{note3}' if stats3 else ""}
    </div>
  </section>

  <section class="cs-sec">
    <div class="wrap">
      <div class="rv"><div class="eyebrow">How it was built</div><h2>{cs["lessons_h"]}</h2></div>
      <div class="lessons">{lessons}</div>
      <div class="limits rv"><div class="eyebrow" style="margin-bottom:14px">Scope and limits</div><ul>{limits}</ul></div>
    </div>
  </section>

  {nxt_link}
</main>

<footer class="theme-dark"><div class="foot"><span>© 2026 Bingcheng Liu</span><span>Full-stack · AI agents · Data</span></div></footer>
<script src="/assets/site.js?v=20261026a"></script>
</body>
</html>
'''


MF = "/assets/multifactor"
YRD = "/assets/yrd"
FR = "/assets/fris"
WD = "/assets/wald"
CASES = [
    dict(
        slug="fris", eyebrow="Case study · 01 · Reputational and governance risk monitoring",
        title_plain="FRIS", title_html="FRIS <em>fund manager risk monitoring</em>",
        summary="FRIS is an enterprise platform that monitors reputational and governance risk at 220 fund managers for due-diligence and investment teams. Every week it reads the news and regulatory releases about each manager, scores every development on a 20-point scale, and shows who is getting riskier, and why. An LLM judges each article, a multi-agent quality layer checks those judgements stage by stage, and deterministic rules turn them into a score an analyst can defend.",
        meta=[("Role", "Sole developer, built for an employer: data, AI pipeline, agents, backend, frontend, deployment"), ("Timeline", "February to October 2026"),
              ("Stack", "Python · LangGraph · FastAPI · PostgreSQL · Next.js · Azure"), ("Status", "Deployed to the cloud with sign-in; private repository")],
        frame="browser", frame_label="fris · risk dashboard", video=f"{FR}/demo.mp4?v=3", poster=f"{FR}/poster.jpg?v=2",
        video_label="71-second screen recording of FRIS running on fictional entities and synthetic data",
        problem_h="Early warning, buried<br><em>in thousands of articles.</em>",
        problem=["Analysts who oversee fund managers on behalf of clients need to know early when a manager runs into trouble: redemptions gated, an investor class action, a regulator's probe. The signals are spread across <b>thousands of articles a week</b>, in many sources and several languages, and most of them are noise.",
                 "A language model can read that stream, but <b>its judgements go wrong in patterns</b>: a law-firm press release read as a lawsuit, a parent company's news pinned on its subsidiary, a reopening read as a resolution. Someone has to catch those errors every week, before clients see the result.",
                 "FRIS does that with agents instead of people, and still produces <b>one number per entity that an analyst can defend</b>: where it came from, which development set it, and what would bring it down."],
        built_h="Code sets the flow, models judge,<br><em>agents guard, rules score.</em>",
        blocks=[
            dict(img=f"{FR}/dashboard.jpg", alt="FRIS dashboard with AI briefing and latest risk events", k="01 · DETERMINISTIC WORKFLOW", h="One command, eight stages, no model in charge",
                 p="Collection, deduplication, clustering windows, scoring formulas and cooling rules are all code. The weekly run starts with one command, checks its own window and model access, and every stage exits with a status code.",
                 points=["Seven collectors: Google News, Yahoo Finance, SEC EDGAR, ASIC, FCA, ESMA, SFC", "Cross-source deduplication, then 7-day semantic clustering into incidents", "Parent-to-subsidiary propagation with rules for when a parent's news really applies"]),
            dict(img=f"{FR}/agents.svg", alt="Diagram of the deterministic workflow with quality agents at each gate", k="02 · MULTI-AGENT QUALITY LAYER", h="Agents that supervise the model",
                 p="Built on LangGraph and organised like supervision on a construction site: the pipeline is the contractor, the agents are the inspectors. Each agent owns one stage and checks it before the next stage reads the results, when a correction still affects nothing downstream.",
                 points=["An inspector reads alongside the classifier in real time and can pause it when disagreement turns systematic", "Classification, clustering, mitigation and scoring agents each own one gate; one field has exactly one writer", "Agents coordinate through work items that must be closed within the run, not free-form chat"]),
            dict(img=f"{FR}/waterline.jpg", alt="Risk Score Waterline chart", k="03 · CONSENSUS AND GUARDRAILS", h="The model proposes; code decides",
                 p="A disputed verdict goes to three models from three different vendors: the producer explains its reasoning, an inspector reads the source blind, and a final reviewer rules. The ruling only lands if code-enforced guardrails pass.",
                 points=["Quotes must appear verbatim in the source or rulebook; headline-only articles are never escalated", "Minimal moves only; each change is one transaction with a before-image and can be reverted", "Scores stay pure arithmetic: highest category, cooling over time, credit for mitigations"]),
            dict(img=f"{FR}/analysis.jpg", alt="Radar of category scores and written risk analysis", k="04 · EXPLAINABLE BY CONSTRUCTION", h="Every rating explains itself",
                 p="The category radar shows what is driving the score today, and the written analysis is generated from the scorer's own record, so every sentence traces back to a scored development. The same text goes into the PDF report for clients."),
            dict(img=f"{FR}/rankings.jpg", alt="Entity risk rankings table", k="05 · BUILT FOR CLIENT WORK", h="Rankings, watchlists, reports",
                 p="A multi-layer ranking across all entities, client watchlists, regional and asset-class filters, a top-movers view, PDF export, and sign-in so clients see only their own watchlist. A separate operations panel shows every run, every agent decision and its cost."),
        ],
        stats=[("288,534", "articles collected since launch"), ("114,810", "events classified by the LLM after deduplication"),
               ("9,485", "incidents clustered from those events"), ("220", "asset managers and entities monitored")],
        stats_note="Cumulative, as of the weekly run of 18 October 2026.",
        stats2=[("~1,960", "new articles in the week of 12–18 October 2026, from 7 collectors"), ("1.5<small>%</small>", "of them classified as risk-relevant by the model; 88% as irrelevant"),
                ("2<small>h</small> 46<small>m</small>", "for the whole weekly pipeline, collection to scoring"), ("100<small>%</small>", "of events classified successfully that week")],
        stats2_note="One week: 12 to 18 October 2026.",
        stats3=[("6", "quality agents, each owning one stage of the pipeline"), ("3", "models from three vendors on every disputed verdict"),
                ("87<small>%</small>", "of agent corrections upheld by independent adjudication"), ("97.9<small>%</small>", "verdict stability: 1,036 articles judged twice")],
        stats3_note="Quality layer, first production run on 12 October 2026.",
        lessons_h="An agent is only useful<br><em>if it can be held to account.</em>",
        lessons=[("Code sets the flow, models judge", "The model never outputs a final score or decides what runs next. Every score change traces back to a specific event or a specific rule."),
                 ("Every alert needs a recipient", "Agents don't raise warnings nobody reads. They issue work items to the agent downstream, which must accept or reject them, with a reason, in the same run."),
                 ("One field, one writer", "Each field has exactly one agent allowed to change it. Agents run in pipeline order and downstream agents never overturn upstream ones."),
                 ("The model proposes; code decides", "A ruling lands only if its quotes are found verbatim, the change is minimal and the score stays inside the category's range."),
                 ("Agents earn their permissions", "Every agent change is adjudicated independently. Accuracy over recent runs sets next week's edit budget, down to observe-only below 50%."),
                 ("Never block production", "The quality layer can fail without failing the weekly run: hard timeouts, a backup reviewer, and anything unfinished is dropped and logged.")],
        limits=["A monitoring signal for analysts, not investment advice or a credit rating.",
                "Independent adjudication of agent changes is still confirmed by a person; the scoring agent only observes for now.",
                "The recording runs the real frontend against a demo backend: every manager, client, headline and figure in it is fictional, and the employer's name is removed."],
    ),
    dict(
        slug="wald", eyebrow="Case study · 02 · Data terminal and trading system",
        title_plain="WALD", title_html="WALD <em>data &amp; trading</em>",
        summary="WALD is my own platform for US equities: a data terminal and a trading system on one shared data layer, with its always-on services running 24/7 on Azure. The terminal turns market, filing, news and industry data into point-in-time datasets behind one read-only API and a terminal-style workspace, with industry-chain analysis at its core. The trading system uses an LLM as its analyst and code for forecasting, sizing, independent risk and execution.",
        meta=[("Role", "Sole architect and developer: data pipelines, database, APIs, agents, both frontends, cloud operations"), ("Year", "2026"),
              ("Stack", "Python · PostgreSQL · Parquet · vanilla JS · Azure · systemd · LLM APIs"), ("Status", "Running 24/7 on Azure since October 2026; private repository")],
        frame="browser", frame_label="wald · data terminal → trading desk", video=f"{WD}/demo.mp4?v=3", poster=f"{WD}/poster.jpg?v=2",
        video_label="97-second screen recording of the WALD data terminal and trading desk",
        problem_h="What was known, when,<br><em>and who it reaches.</em>",
        problem=["Trading on events means answering three questions fast: <b>what just happened, what was already known, and which companies it reaches</b>. The answers sit in a dozen sources with different clocks: exchange data, SEC filings, news wires, macro releases, foreign disclosures.",
                 "Most of the errors are quiet. A restated quarter or a renamed ticker leaks <b>information from the future</b> into a backtest; a filing time recorded in the wrong time zone shifts a whole replay by hours.",
                 "And the most valuable signal is often one step removed: a supplier's contract, a memory price, a capacity commitment. Seeing it needs <b>a supply chain mapped from primary evidence</b>, not a list of tickers."],
        built_h="One data layer,<br><em>two products, always on.</em>",
        blocks=[
            dict(img=f"{WD}/cockpit.jpg", alt="Cockpit heat map of the AI supply chain", k="01 · INDUSTRY-CHAIN ANALYSIS", h="The AI supply chain, live",
                 p="The terminal opens on a heat map of the AI supply chain, grouped by stage. Sector and theme heat maps and an infrastructure map from hyperscalers down to chips, packaging, power and cooling are one click away, and every company opens onto its own supply chain.",
                 points=["Any company's suppliers and customers, five tiers up and down", "Peers, orders, partnerships and investments as separate relation types", "Every link marked as filed, registered or inferred"]),
            dict(img=f"{WD}/hbm_dash.jpg", alt="HBM workbench dashboard", k="02 · ONE CHAIN IN DEPTH", h="Built from primary sources",
                 p="The HBM workbench follows the memory chain end to end: supply, demand, pricing, capacity, qualification and product roadmaps per supplier. Relationships come from filings, such as supply contracts disclosed to the Korean regulator, with their correction history kept.",
                 points=["201 Korean supply-contract disclosures parsed, with 168 correction links", "Capacity commitments and product roadmaps tracked per company", "A research trail runs event → product → evidence → impact"]),
            dict(img=f"{WD}/asof.jpg", alt="Company financials replayed as of a past date", k="03 · POINT-IN-TIME DATA", h="Every row knows when it became known",
                 p="Raw files land in an append-only lake, become fixed-version products, then a PostgreSQL database where every row carries the time it became available. Any page, API call or script can be replayed as of a past date and sees only what was known then.",
                 points=["Row-level security enforces the cutoff in the database, not in the page", "Restatements kept as versions; ticker, CIK and FIGI resolved by date", "Strict mode refuses a historical request it cannot honour instead of silently degrading"]),
            dict(img=f"{WD}/desk.jpg", alt="Trading desk overview", k="04 · TRADING SYSTEM", h="The model analyses; code decides",
                 p="An LLM reads the filings and news and writes a research file with scenario prices by horizon. Code turns that into candidates, a manager sizes them, an independent risk station can veto, and a trader places limit orders. Every station leaves a versioned, hashed receipt.",
                 points=["Inputs unlock at the time they were received, and model inputs are scanned for leaks", "Daily model budget enforced across all runs, with circuit breakers", "Research memory: dated facts, live theses and expectation cards frozen before earnings"]),
            dict(img=f"{WD}/cloud.svg", alt="Cloud deployment diagram", k="05 · CLOUD OPERATIONS", h="Always on, on Azure",
                 p="The platform's always-on layer runs on an Azure VM: 24 systemd services ingest SEC filings every minute with their acceptance times, read news wires and regulator releases, record quotes and order-flow tapes, freeze and score shadow forecasts, and keep a headless broker gateway connected to a paper account on a private network, its API bound to loopback.",
                 points=["Hash-locked deployer: verifies hashes, checks for zero open positions and orders, drains running jobs and writes a receipt", "Every deploy approved by an independent reviewer first; six in one day, including during market hours", "Watchdog checks every service every 10 minutes and alerts on change; daily briefing, backup and cold copy with restore checks", "Model spend reserved and settled per call under daily caps; ledger, logs and broker reconciled"]),
        ],
        stats=[("1,050", "data sources verified working, from 1,500 probed"), ("20,291", "US securities in the versioned security master"),
               ("16.5M", "rows in the point-in-time database, across 189 tables"), ("577K", "news documents from 15 sources")],
        stats_note="Data terminal, as of 26 October 2026.",
        stats2=[("851K", "issuer-month fundamentals rows, 7,697 issuers, 2009 to 2026"), ("4,900", "US stocks × 12 factors in the multi-factor panel"),
                ("3.8M", "daily price bars, raw and adjusted"), ("2.06M", "segment-revenue rows taken from filings")],
        stats2_note="Depth of the data.",
        stats3=[("24<small>/7</small>", "on Azure since 10 October 2026, 24 systemd services"), ("48,953", "SEC filing files ingested into the cloud lake"),
                ("162", "synthetic scenarios and 157 unit tests on the decision chain"), ("3,215", "historical cases for calibration and replay")],
        stats3_note="Trading system and cloud operations.",
        lessons_h="Run like production,<br><em>from day one.</em>",
        lessons=[("Builder and reviewer, separated", "Every work package is self-checked against the reviewer's likely attacks, then accepted by an independent AI reviewer before it is committed."),
                 ("Known when, not just known", "Every row carries when it became available and how that time was established. The database enforces the cutoff, so a replay cannot see the future."),
                 ("Every link needs a source", "A supply-chain relation is filed, registered or inferred, and says so. Inferred links never pass as disclosed ones."),
                 ("The model analyses; code decides", "The LLM writes research and scenarios. Sizing, risk limits, stops and orders are code, and the risk station ignores the model's opinion."),
                 ("Deploys are approved and reversible", "No file reaches the cloud without a recorded approval, a hash check before and after, and a receipt."),
                 ("Fail safe, not silent", "When a budget runs out, new paid work stops but risk checks, protective orders and checkpoints keep running.")],
        limits=["Orders go to a paper account; live accounts are never connected.",
                "Some industry dashboards appear in their labelled sample mode, and the interface is in Chinese."],
    ),
    dict(
        slug="multifactor-scoring", eyebrow="Case study · 03 · Equity research tooling",
        title_plain="Multi-factor stock scoring", title_html="Multi-factor<br><em>stock scoring</em>",
        summary="A full-stack tool for equity research teams: researchers set the factors, directions and weights, and the tool turns them into exact, reproducible scores, rankings and an auditable stock pool, explaining every result factor by factor.",
        meta=[("Role", "Sole developer: design, backend, frontend, tests"), ("Year", "2026"), ("Stack", "Python · FastAPI · NumPy · SQLite · vanilla JS"), ("Status", "Runs on ~2,300 US equities on my own platform; private repository, source on request")],
        frame="browser", frame_label="multi-factor-scoring · live walkthrough", video=f"{MF}/demo.mp4?v=3", poster=f"{MF}/poster.jpg?v=2",
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
                "The recording uses synthetic data (200 sample companies across 10 industries). The same tool runs unchanged on ~2,300 US equities and 12 fundamental and momentum factors on my own platform; those data and results are not shown here."],
    ),
    dict(
        slug="yrd-assistant", eyebrow="Case study · 04 · Workflow automation",
        title_plain="YRD Assistant", title_html="YRD <em>Assistant</em>",
        summary="A desktop assistant that runs a financial publisher's daily report workflow: it finds the morning market commentary in Outlook, writes each section into the right WordPress draft, and drafts the confirmation email, while a person stays in charge of publishing.",
        meta=[("Role", "Sole developer, built for an employer"), ("Timeline", "March to May 2026"), ("Stack", "Node.js · Electron · Python · Outlook COM · WordPress REST API"), ("Status", "Delivered; private repository")],
        frame="win", frame_label="YRD Assistant · desktop app", video=f"{YRD}/demo.mp4?v=3", poster=f"{YRD}/poster.jpg?v=2",
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
    out.write_text(page(cs, CASES[i + 1] if i + 1 < len(CASES) else None))
    print("wrote", out.relative_to(ROOT))
