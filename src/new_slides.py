# New slides written in the same inline-style idiom as the Nudge / AI Commons talks.
# Only words the user gave, or words from the source material. No extra captions.

BG = ("box-sizing:border-box;padding:84px 120px 90px;display:flex;flex-direction:column;gap:56px;"
      "background-color:#f6f3ea;background-image:linear-gradient(rgba(27,26,23,.07) 2px,transparent 2px),"
      "linear-gradient(90deg,rgba(27,26,23,.07) 2px,transparent 2px);background-size:60px 60px;"
      "color:#1b1a17;font-family:'Bricolage Grotesque',sans-serif;")
BLUE = ("box-sizing:border-box;padding:96px 120px;display:flex;flex-direction:column;justify-content:center;gap:48px;"
        "background:#1f5fd1;color:#fff;font-family:'Bricolage Grotesque',sans-serif;")
H = "flex:none;font:800 96px/1.02 'Bricolage Grotesque',sans-serif;letter-spacing:-3px;"
CARD = "background:#fff;border:3px solid #1b1a17;border-radius:24px;box-shadow:10px 10px 0 {c};padding:44px 48px;display:flex;flex-direction:column;gap:24px;"


def sec(label, notes, style, body):
    return f'<section data-label="{label}" data-speaker-notes="{notes}" style="{style}">\n{body}\n</section>'


def title(logos):
    speakers = [("Aimee Barnes", "J-PAL"), ("Olivia Bryan", "J-PAL"), ("Agnes Kiragga", "APHRC"),
                ("Miranda Barasa", "APHRC"), ("Aman Dalmia", "The Agency Fund"),
                ("Anneka Wickramanayake", "Jacaranda Health"), ("Joseph Ross", "Ariadne Labs")]
    sp = "".join(
        f'<div style="display:flex;flex-direction:column;gap:6px;"><div style="font:700 36px/1.1 \'Bricolage Grotesque\',sans-serif;">{n}</div>'
        f'<div style="font:500 28px/1.2 \'Bricolage Grotesque\',sans-serif;color:#4a4740;">{o}</div></div>' for n, o in speakers)
    lg = "".join(f'<img src="{u}" alt="{a}" style="height:{h}px;">' for u, a, h in logos)
    style = BG.replace("gap:56px;", "gap:0;justify-content:space-between;").replace("padding:84px 120px 90px", "padding:110px 120px 90px")
    body = f'''  <div style="display:grid;grid-template-columns:1fr 520px;gap:80px;align-items:start;">
    <div style="display:flex;flex-direction:column;gap:56px;">
      <div style="font:800 128px/1.02 'Bricolage Grotesque',sans-serif;letter-spacing:-5px;">Navigating Challenges in Evaluating Health AI for Impact</div>
      <div style="display:flex;flex-direction:column;gap:12px;">
        <div style="font:700 52px/1.1 'Bricolage Grotesque',sans-serif;">Global Digital Health Forum</div>
        <div style="font:500 40px/1.2 'IBM Plex Mono',monospace;color:#4a4740;">Bangkok, December 2026</div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:26px;border-left:3px solid #1b1a17;padding-left:44px;margin-top:12px;">{sp}</div>
  </div>
  <div style="display:flex;gap:72px;align-items:center;border-top:3px solid #1b1a17;padding-top:40px;">{lg}</div>'''
    return sec("00 Title", "Title. No member intros.", style, body)


def _cols(title, notes, label, cols, size):
    out = []
    for c, L, name, items in cols:
        it = "".join(f'<div style="font:500 {size}px/1.3 \'Bricolage Grotesque\',sans-serif;">{t}</div>' for t in items)
        out.append(f'''    <div style="{CARD.format(c=c)}border-top:14px solid {c};">
      <div style="font:600 30px/1 'IBM Plex Mono',monospace;color:{c};">{L}</div>
      <div style="font:800 56px/1 'Bricolage Grotesque',sans-serif;letter-spacing:-2px;">{name}</div>
      <div style="display:flex;flex-direction:column;gap:22px;">{it}</div>
    </div>''')
    body = f'''  <div style="{H}">{title}</div>
  <div style="flex:1;min-height:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:40px;align-content:center;">
{chr(10).join(out)}
  </div>'''
    return sec(label, notes, BG, body)


def mve():
    cols = [
        ("#1f5fd1", "L1", "Model", ["Build a Golden Dataset of at least 30-50 items covering key, diverse user interactions",
                                    "Define 2-3 rubrics for model success, including at least one robust safety/guardrail metric"]),
        ("#6d4fd1", "L2", "Product", ["Instrument the product to capture events automatically",
                                      "Compute two metrics from event data: activation (used once) and retention (used repeatedly)"]),
        ("#b44a06", "L3", "User", ["Define 1-2 outcome metrics tied to your theory of change",
                                   "Include at least one early-warning indicator of harm, such as over-reliance or disengagement"]),
        ("#1a7f37", "L4", "Impact", ["Conduct an impact evaluation with a counterfactual and a sample size large enough to measure key outcomes",
                                     "Use strong version control: either a frozen version or a limited number of product versions to be tested"]),
    ]
    return _cols("Minimum viable evaluation", "From eval.playbook.org.ai, Minimum Viable Evaluations.", "MVE", cols, 32)


def noora():
    # same UI as the 4-level framework slide, filled with Noora's metrics
    cols = [("#1f2b4a", "#c49a3c", "L1", "Model<br>Evaluation", [("Medical accuracy", "Is the advice medically correct?"), ("Missed escalations", "Emergencies the AI failed to flag to the medical team"), ("Context awareness", "Does the reply use what the caregiver already shared, like the baby’s age?")]),
            ("#233a2d", "#5fae7e", "L2", "Product<br>Evaluation", [("Scale", "Number of caregiver messages the copilot handles every day, across India, Bangladesh, Indonesia and Nepal"), ("Draft acceptance", "% of queries where the medical team sends the AI draft without any edits")]),
            ("#361d3a", "#b07cc6", "L3", "User<br>Evaluation", [("Queries per caregiver", "Are caregivers asking more medical questions after using the service, a sign they trust it?"), ("Uptake of advice", "% of caregivers who actually follow the advice at home, e.g. skin-to-skin care for newborns")]),
            ("#3a1f14", "#d97a4a", "L4", "Impact<br>Evaluation", [("Severe complications and deaths", "Does the copilot reduce severe complications and deaths among high-risk mothers and newborns? Planned neonatal RCT with Stanford Impact Labs")])]
    serif = "Gelasio,Georgia,serif"
    cards = []
    for bg, ac, L, n, ms in cols:
        mets = "".join(f'''<div style="display:flex;flex-direction:column;gap:6px;"><div style="font:700 32px/1.2 {serif};color:#ffffff;">{a}</div><div style="font:400 27px/1.3 {serif};color:#e9e4d8;">{b}</div></div>''' for a, b in ms)
        cards.append(f'''<div style="background:{bg};border-top:14px solid {ac};padding:40px 40px 44px;display:flex;flex-direction:column;color:#f3efe6;">
      <div style="font:700 30px/1 'IBM Plex Sans',sans-serif;color:{ac};">{L}</div>
      <div style="font:700 48px/1.1 {serif};margin-top:24px;color:#ffffff;">{n}</div>
      <div style="height:5px;background:{ac};opacity:.6;margin:24px -12px 0;"></div>
      <div style="display:flex;flex-direction:column;gap:20px;margin-top:24px;">{mets}</div></div>''')
    body = f'''  <div style="{H}">Noora Health</div>
  <div style="flex:1;min-height:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:40px;">{"".join(cards)}</div>'''
    notes = "Same four levels, filled in with what Noora measures. Optional numbers to say aloud (Q1 2026 audit): missed escalations 10%, 10K+ messages a day, draft acceptance 71% Indonesia / 8% Bangladesh, queries per caregiver +33% Bangladesh. Neonatal RCT planned with Stanford Impact Labs."
    return sec("Noora", notes, BG.replace("gap:56px;", "gap:44px;"), body)


def divider(label, big, small, notes):
    body = f'''  <div style="font:800 140px/1.0 'Bricolage Grotesque',sans-serif;letter-spacing:-5px;">{big}</div>
  <div style="align-self:flex-start;background:#ffd84d;color:#1b1a17;border-radius:24px;padding:24px 40px;font:800 60px/1.1 'Bricolage Grotesque',sans-serif;letter-spacing:-2px;">{small}</div>'''
    return sec(label, notes, BLUE, body)


def lantern():
    body = f'''  <div style="{H}">Lantern</div>
  <div style="flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:40px;">
    <div style="{CARD.format(c='#1f5fd1')}">
      <div style="font:600 30px/1 'IBM Plex Mono',monospace;color:#4a4740;">Try it</div>
      <div style="font:800 72px/1 'IBM Plex Mono',monospace;color:#1f5fd1;">tinyurl.com/lantern-chatbot</div>
    </div>
  </div>'''
    return sec("Lantern", "Introduce Lantern in one line. INPUT NEEDED from Aman: what Lantern does and its rubric.", BG, body)


def demo():
    steps = [("A", "I ask Lantern queries", "Do I agree? What should the right answer be?"),
             ("B", "Your queries", "Call them out. I'll run them."),
             ("C", "Add them to Calibrate", "Reproduce the mistakes"),
             ("D", "Fix the knowledge base", "Re-run. Tests pass again.")]
    rows = "".join(f'''<div style="background:#fff;border:3px solid #1b1a17;border-radius:24px;box-shadow:10px 10px 0 #1f5fd1;padding:30px 44px;display:grid;grid-template-columns:90px 1fr;gap:30px;align-items:center;">
      <div style="font:800 80px/1 'Bricolage Grotesque',sans-serif;color:#1f5fd1;">{a}</div>
      <div style="display:flex;flex-direction:column;gap:8px;"><div style="font:700 50px/1.1 'Bricolage Grotesque',sans-serif;">{b}</div><div style="font:500 34px/1.2 'Bricolage Grotesque',sans-serif;color:#4a4740;">{c}</div></div></div>''' for a, b, c in steps)
    body = f'''  <div style="{H}">Live demo</div>
  <div style="flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:28px;">{rows}</div>'''
    notes = ("A: ask queries live, including one known failure; say whether you agree and what the right answer should be. "
             "B: take 2-3 queries from the room; you keep control of the screen. "
             "C: add them as tests in Calibrate and show the mistakes reproduce. "
             "D: fix the knowledge base Lantern uses, re-run, tests pass. "
             "Check first: can Calibrate run Lantern with its knowledge base?")
    return sec("Demo steps", notes, BG, body)


def master_placeholder(n, what):
    body = f'''  <div style="flex:1;display:flex;align-items:center;justify-content:center;border:6px dashed #c79a00;border-radius:24px;background:#fff6cc;">
    <div style="font:700 56px/1.3 'IBM Plex Mono',monospace;text-align:center;">Master deck slide {n}<br>{what}</div>
  </div>'''
    return sec(f"Master {n}", f"Placeholder: replace with master deck slide {n} ({what}) once the .pptx is shared.", BG, body)


MVE = {
    1: ("#1f5fd1", "Model evaluation", [
        "Define 2-3 rubrics for model success, including at least one robust safety/guardrail metric computed on your Golden Dataset",
        "With product and business owners, set a success criterion or threshold for each rubric/metric that must be passed before deployment",
        "Build a Golden Dataset of at least 30-50 items covering key, diverse user interactions",
        "Establish a process for expert review of system responses to Golden Dataset inputs as you iterate on system configuration"]),
    2: ("#6d4fd1", "Product evaluation", [
        "Instrument the product to capture events automatically",
        "Compute two metrics from event data: activation (used once) and retention (used repeatedly)",
        "Look for patterns in the data and talk to users to find improvement opportunities",
        "Test improvement ideas against these metrics with an A/B test"]),
    3: ("#b44a06", "User evaluation", [
        "Define 1-2 outcome metrics tied to your theory of change, focusing on the most decision-relevant cognitive or behavioral outcomes",
        "Include at least one early-warning indicator of harm, such as over-reliance or disengagement",
        "Pair at least one behavioral/trace metric with a brief, contextualized self-report measure of no more than 3 items",
        "Include a minimal external check, such as a focused group discussion, offline data, or stakeholder validation, to confirm on-platform measures reflect real-world outcomes"]),
    4: ("#1a7f37", "Impact evaluation", [
        "Conduct an impact evaluation with a counterfactual and a sample size large enough to measure key outcomes, including sub-populations of interest (e.g., by gender or geography)",
        "Use strong version control: either a frozen version or a limited number of product versions to be tested",
        "Cost the data collection"]),
}


def mve_level(n):
    c, name, items = MVE[n]
    rows = "".join(
        f'<div style="background:#fff;border:3px solid #1b1a17;border-radius:20px;box-shadow:8px 8px 0 {c};padding:24px 32px;display:grid;grid-template-columns:64px 1fr;gap:20px;align-items:baseline;">'
        f'<div style="font:600 30px/1 \'IBM Plex Mono\',monospace;color:{c};">0{i+1}</div>'
        f'<div style="font:600 36px/1.3 \'Bricolage Grotesque\',sans-serif;text-wrap:pretty;">{t}</div></div>' for i, t in enumerate(items))
    body = f'''  <div style="font:800 96px/1.02 'Bricolage Grotesque',sans-serif;letter-spacing:-3px;">Minimum viable evaluation</div>
  <div style="font:700 52px/1.1 'Bricolage Grotesque',sans-serif;color:{c};margin-top:-24px;">Level {n}: {name}</div>
  <div style="flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:24px;">{rows}</div>'''
    return sec(f"MVE L{n}", f"Minimum viable evaluation for Level {n}, from eval.playbook.org.ai.", BG.replace("gap:56px;", "gap:40px;"), body)


def _hl(t, kind="b"):
    return f'<span data-hl="{kind}" style="background:#ffd84d;padding:0 6px;border-radius:6px;">{t}</span>'


def why_fail():
    items = [
        f"{_hl('Biased')} training data, {_hl('misinformation')}, and {_hl('unverified claims')} baked into the model",
        f"Poor performance in {_hl('low-resource languages')}: your users may be underrepresented in training data",
        f"{_hl('Knowledge cut-off')}: the model doesn't know what happened after its training ended",
        f"No access to {_hl('local context')}: norms, policies, real-time conditions on the ground",
        f"{_hl('Inconsistent instruction-following')}: complex or ambiguous prompts often produce the wrong output",
        f"{_hl('Wrong tool')} for the task: AI may confidently give wrong answers for a complex multiplication that any calculator can easily do",
    ]
    rows = "".join(
        f'<div style="background:#fff;border:3px solid #1b1a17;border-radius:20px;box-shadow:8px 8px 0 #1b1a17;padding:18px 32px;font:500 38px/1.3 \'Bricolage Grotesque\',sans-serif;text-wrap:pretty;">{t}</div>'
        for t in items)
    body = f'''  <div style="{H}">Why AI can {_hl('fail your users', 'h')}</div>
  <div style="flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:16px;">{rows}</div>'''
    return sec("Why AI can fail your users", "Walk the six, one concrete example each.", BG.replace("gap:56px;", "gap:36px;"), body)


def framework():
    # master-deck design (dark columns, serif), rebuilt as crisp HTML
    cols = [("#1f2b4a", "#c49a3c", "L1", "Model<br>Evaluation", "Does the AI system perform as intended?", "AI Engineers<br>Domain Experts"),
            ("#233a2d", "#5fae7e", "L2", "Product<br>Evaluation", "Does the overall product engage and retain users?", "Product Managers<br>Data Scientists"),
            ("#361d3a", "#b07cc6", "L3", "User<br>Evaluation", "Does product usage change how users are thinking, feeling, and behaving?", "Behavioural Scientists<br>UX Researchers"),
            ("#3a1f14", "#d97a4a", "L4", "Impact<br>Evaluation", "Does product usage improve development outcomes?", "Economists<br>Impact Researchers")]
    serif = "Gelasio,Georgia,serif"
    cards = []
    for k, (bg, ac, L, n, q, o) in enumerate(cols):
        cards.append(f'''<div style="background:{bg};border-top:14px solid {ac};padding:44px 44px 48px;display:flex;flex-direction:column;color:#f3efe6;">
      <div style="font:700 30px/1 'IBM Plex Sans',sans-serif;color:{ac};">{L}</div>
      <div style="font:700 60px/1.12 {serif};margin-top:70px;">{n}</div>
      <div style="height:5px;background:{ac};opacity:.6;margin:56px -12px 0;"></div>
      <div style="font:400 36px/1.3 {serif};margin-top:64px;color:#f3efe6;">{q}</div>
      <div style="margin-top:auto;font:400 30px/1.35 {serif};color:{ac};">{o}</div></div>''')
    body = f'''  <div style="{H}">The 4-Level Evaluation Framework</div>
  <div style="flex:1;min-height:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:40px;">{"".join(cards)}</div>'''
    return sec("The 4-Level Evaluation Framework", "One line per level. Different levels, different disciplines.", BG.replace("gap:56px;", "gap:44px;"), body)


def dev_outcomes():
    body = f'''  <div style="font:600 32px/1 'IBM Plex Mono',monospace;letter-spacing:2px;color:#ffd84d;">DEVELOPMENT OUTCOMES</div>
  <div style="font:700 88px/1.3 'Bricolage Grotesque',sans-serif;max-width:1550px;">If the <span data-hl="b" style="background:#ffd84d;color:#1b1a17;padding:0 14px;border-radius:12px;">AI system is not performing well (L1)</span> or if <span data-hl="b" style="background:#ffd84d;color:#1b1a17;padding:0 14px;border-radius:12px;">no one is using the product as intended (L2/L3)</span>, then it is unlikely that there will be any impact (L4)</div>
  <div style="width:1000px;height:6px;background:#c49a3c;"></div>'''
    return sec("Development outcomes", "Level 4 depends on Levels 1, 2 and 3.", BLUE, body)


def feedback():
    lv = [("L1", "Model", "Does the AI system perform as intended?", "#1f2b4a", "#c49a3c"),
          ("L2", "Product", "Does the overall product engage and retain users?", "#233a2d", "#5fae7e"),
          ("L3", "User", "Does product usage change how users are thinking, feeling, and behaving?", "#361d3a", "#b07cc6"),
          ("L4", "Impact", "Does product usage improve development outcomes?", "#3a1f14", "#d97a4a")]
    W, CW, GAP, TOP, CH = 1680, 390, 40, 90, 300
    cx = [CW / 2 + i * (CW + GAP) for i in range(4)]
    bottom = TOP + CH
    cards = ""
    for i, (L, n, q, bg, ac) in enumerate(lv):
        x = i * (CW + GAP)
        cards += (f'<div style="position:absolute;left:{x}px;top:{TOP}px;width:{CW}px;height:{CH}px;box-sizing:border-box;background:{bg};border-top:12px solid {ac};border-radius:18px;padding:28px 30px;display:flex;flex-direction:column;gap:22px;color:#f3efe6;">'
                  f'<div style="display:flex;align-items:center;gap:20px;"><span style="background:{ac};color:{bg};border-radius:8px;padding:6px 14px;font:700 26px/1 \'IBM Plex Mono\',monospace;">{L}</span>'
                  f'<span style="font:700 40px/1 \'Bricolage Grotesque\',sans-serif;color:#ffffff;">{n}</span></div>'
                  f'<div style="font:500 30px/1.35 \'Bricolage Grotesque\',sans-serif;color:#e9e4d8;">{q}</div></div>')
    svg = [f'<svg width="{W}" height="520" viewBox="0 0 {W} 520" style="position:absolute;left:0;top:0;overflow:visible;" xmlns="http://www.w3.org/2000/svg"><defs>']
    for i, (_, _, _, _, ac) in enumerate(lv):
        svg.append(f'<marker id="fb{i}" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,0 L10,0 L5,10 z" fill="{ac}"/></marker>')
    svg.append('<marker id="fbu" viewBox="0 0 10 10" refX="5" refY="2" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,10 L10,10 L5,0 z" fill="#8a7a6a"/></marker></defs>')
    # self loops above each card
    for i, (_, _, _, _, ac) in enumerate(lv):
        c = cx[i]
        svg.append(f'<path d="M{c+40},{TOP} C{c+40},{TOP-90} {c-40},{TOP-90} {c-40},{TOP-6}" fill="none" stroke="{ac}" stroke-width="4" marker-end="url(#fb{i})"/>')
    # feedback arcs below: each level back to every lower level
    for s in range(1, 4):
        for d in range(s - 1, -1, -1):
            span = s - d
            ac = lv[s][4]
            op = {1: .9, 2: .55, 3: .35}[span]
            depth = 70 + span * 55
            svg.append(f'<path d="M{cx[s]},{bottom+4} C{cx[s]},{bottom+depth} {cx[d]},{bottom+depth} {cx[d]},{bottom+8}" fill="none" stroke="{ac}" stroke-opacity="{op}" stroke-width="4" marker-end="url(#fbu)"/>')
    svg.append('</svg>')
    rows = ""
    for k, (a, b, c, col) in enumerate([("Greater marginal ", "Cost", "", "#2f4a2a"), ("Slower ", "Speed", " of iteration", "#1f2b4a"), ("Increased ", "Risk", " to user or org", "#7a1f1f")]):
        y = 540 + k * 78
        rows += (f'<div style="position:absolute;left:300px;top:{y}px;width:1080px;height:64px;display:flex;align-items:center;">'
                 f'<div style="flex:1;height:52px;background:linear-gradient(90deg,#f5f3ee,#f29a90);display:flex;align-items:center;justify-content:center;font:500 34px/1 \'Bricolage Grotesque\',sans-serif;color:{col};">{a}<b style="margin:0 .25em;">{b}</b>{c}</div>'
                 f'<div style="width:0;height:0;border-top:46px solid transparent;border-bottom:46px solid transparent;border-left:56px solid #f29a90;"></div></div>')
    body = f'''  <div style="font:800 96px/1.02 'Bricolage Grotesque',sans-serif;letter-spacing:-3px;">Learnings feed back to lower levels</div>
  <div style="position:relative;flex:1;min-height:0;">{"".join(svg)}{cards}{rows}</div>'''
    notes = "The levels are not one-way. Each level feeds back into the ones below it. Higher levels cost more, take longer to learn from, and carry more risk to users."
    return sec("Learnings feed back to lower levels", notes, BG.replace("gap:56px;", "gap:20px;"), body)



def level1_divider():
    # framework UI again, with Level 1 lit up and the rest faded: this is the level we go deep on
    cols = [("#1f2b4a", "#c49a3c", "L1", "Model<br>Evaluation", "Does the AI system perform as intended?", 1),
            ("#233a2d", "#5fae7e", "L2", "Product<br>Evaluation", "Does the overall product engage and retain users?", .25),
            ("#361d3a", "#b07cc6", "L3", "User<br>Evaluation", "Does product usage change how users are thinking, feeling, and behaving?", .25),
            ("#3a1f14", "#d97a4a", "L4", "Impact<br>Evaluation", "Does product usage improve development outcomes?", .25)]
    serif = "Gelasio,Georgia,serif"
    cards = []
    for bg, ac, L, n, q, op in cols:
        ring = "outline:6px solid #c49a3c;outline-offset:8px;" if op == 1 else ""
        cards.append(f'''<div style="opacity:{op};{ring}background:{bg};border-top:14px solid {ac};padding:40px 40px 44px;display:flex;flex-direction:column;color:#f3efe6;">
      <div style="font:700 30px/1 'IBM Plex Sans',sans-serif;color:{ac};">{L}</div>
      <div style="font:700 54px/1.12 {serif};margin-top:36px;color:#ffffff;">{n}</div>
      <div style="height:5px;background:{ac};opacity:.6;margin:32px -12px 0;"></div>
      <div style="font:400 34px/1.3 {serif};margin-top:36px;color:#f3efe6;">{q}</div></div>''')
    body = f'''  <div style="{H}">Evaluating AI is hard</div>
  <div style="flex:1;min-height:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:48px;padding:8px;">{"".join(cards)}</div>'''
    return sec("Level 1 deep dive", "Transition: of the four levels, Level 1 is where teams are most unsure today. The rest of this section goes deep on it.", BG.replace("gap:56px;", "gap:44px;"), body)


def why_hard():
    items = [("01", "Teams don’t know what good looks like", "What a correct, safe reply looks like is hard to define and hard to agree on"),
             ("02", "Manual verification does not scale", "Someone verifies a few responses before deploying changes. That barely works for a pilot, but does not create a reliable product for real users as new changes cause unexpected errors."),
             ("03", "Evaluation falls on engineers who do not know your domain", "Engineers cannot evaluate response quality whereas the domain experts are either left out of the work or experience friction in collaboration."),
             ("04", "Teams don’t know how to build evaluation datasets", "Test sets miss the edge cases that real users bring"),
             ("05", "Users find the failures first", "Mistakes surface only after they reach real people")]
    cards = "".join(f'''<div style="background:#fff;border:3px solid #1b1a17;border-radius:20px;box-shadow:8px 8px 0 #1b1a17;padding:22px 34px;display:grid;grid-template-columns:60px 560px 1fr;gap:28px;align-items:center;">
      <div style="font:600 30px/1 'IBM Plex Mono',monospace;color:#b44a06;">{n}</div>
      <div style="font:800 36px/1.15 'Bricolage Grotesque',sans-serif;letter-spacing:-1px;">{a}</div>
      <div style="font:500 27px/1.35 'Bricolage Grotesque',sans-serif;color:#4a4740;">{b}</div></div>''' for n, a, b in items)
    body = f'''  <div style="{H}">Why Level 1 is hard for teams</div>
  <div style="flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:22px;">{cards}</div>'''
    return sec("Why Level 1 is hard", "Four problems we see in every team. The rest of this section shows how to fix each one.", BG, body)


def demo_title():
    style = ("box-sizing:border-box;padding:0 160px;display:flex;flex-direction:column;justify-content:center;"
             "background:#1f2a4d;color:#ffffff;font-family:'Bricolage Grotesque',sans-serif;")
    body = "  <div style=\"font:800 220px/1 'Bricolage Grotesque',sans-serif;color:#ffffff;\">Demo</div>"
    return sec("Demo", "Live demo: Lantern queries, add failures to Calibrate, fix the knowledge base, re-run.", style, body)


def thank_you(logos):
    style = ("box-sizing:border-box;padding:0 160px;display:flex;flex-direction:column;justify-content:center;gap:90px;"
             "background:#1f2a4d;color:#ffffff;font-family:'Bricolage Grotesque',sans-serif;")
    lg = "".join(f'<img src="{u}" alt="{a}" style="height:{round(h*1.25)}px;">' for u, a, h in logos)
    body = (f"  <div style=\"font:800 200px/1 'Bricolage Grotesque',sans-serif;color:#ffffff;\">Thank You</div>\n"
            f"  <div style=\"align-self:flex-start;background:#ffffff;border-radius:24px;padding:40px 64px;display:flex;gap:90px;align-items:center;\">{lg}</div>")
    return sec("Thank you", "Thank the audience and partners.", style, body)


def resources(qrs):
    cards = ""
    for u, title, url, c in qrs:
        cards += (f'<div style="background:#fff;border:3px solid #1b1a17;border-radius:24px;box-shadow:10px 10px 0 {c};padding:44px;display:flex;flex-direction:column;align-items:center;gap:28px;">'
                  f'<div style="font:800 52px/1.1 \'Bricolage Grotesque\',sans-serif;text-align:center;min-height:115px;display:flex;align-items:center;">{title}</div>'
                  f'<img src="{u}" alt="QR code for {url}" style="width:380px;height:380px;display:block;">'
                  f'<div style="font:600 34px/1 \'IBM Plex Mono\',monospace;color:#1f5fd1;">{url}</div></div>')
    body = (f'  <div style="{H}">Resources</div>\n'
            f'  <div style="flex:1;min-height:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:80px;padding:0 120px;align-content:center;">{cards}</div>')
    return sec("Resources", "Scan to read the 4-level evaluation framework playbook, and to try Calibrate.", BG, body)
