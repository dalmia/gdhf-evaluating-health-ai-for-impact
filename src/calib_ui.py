# HTML replicas of the Calibrate UI screenshots used in the Nudge talk, so the examples can be Noora's.
F = "'Noto Sans','Noto Sans Devanagari',-apple-system,sans-serif"
M = "'IBM Plex Mono',monospace"
GREEN, RED, PURPLE = "#1a7f37", "#c62828", "#7c3aed"


def label(t, align="flex-start", mark=None):
    m = ""
    if mark == "ok":
        m = f'<span style="color:{GREEN};margin-left:8px;">✓</span>'
    elif mark == "bad":
        m = f'<span style="color:{RED};margin-left:8px;">✕</span>'
    return f'<div style="align-self:{align};font:500 24px/1 {F};color:#1a1a1a;">{t}{m}</div>'


def bubble(t, user=False, bar=None):
    bg = "#f3f3f3" if user else "#fff"
    align = "flex-end" if user else "flex-start"
    b = f"border-left:6px solid {bar};" if bar else ""
    return (f'<div style="align-self:{align};max-width:88%;background:{bg};border:2px solid #e5e5e5;{b}'
            f'border-radius:20px;padding:16px 22px;font:400 26px/1.4 {F};color:#1a1a1a;">{t}</div>')


def chat(turns):
    """turns: list of (role, text, mark) with role in agent/user; mark None/ok/bad marks the evaluated agent turn"""
    out = []
    for role, text, mark in turns:
        if role == "user":
            out.append(label("User", "flex-end"))
            out.append(bubble(text, user=True))
        else:
            bar = GREEN if mark == "ok" else RED if mark == "bad" else None
            out.append(label("Agent", mark=mark))
            out.append(bubble(text, bar=bar))
    return f'<div style="display:flex;flex-direction:column;gap:12px;">{"".join(out)}</div>'


def chip(t, kind):
    c = {"ok": (GREEN, "#dcfce7"), "bad": (RED, "#fde2e4"), "hide": (PURPLE, "#f3e8ff"), "ver": ("#555", "#fff")}[kind]
    bd = "border:1.5px solid #ccc;" if kind == "ver" else ""
    return f'<span style="{bd}background:{c[1]};color:{c[0]};border-radius:8px;padding:5px 10px;font:500 20px/1 {F};white-space:nowrap;">{t}</span>'


def blk(t):
    return f'<span style="align-self:flex-start;background:#1b1a17;color:#fff;border-radius:6px;padding:5px 10px;font:600 18px/1 {M};letter-spacing:1px;">{t}</span>'


def evaluator(name, ok, desc, criteria=None, reasoning=None, word=("Pass", "Fail"), ver="v1", open_=True):
    bg, bd = ("#effbf1", "#86d39a") if ok else ("#fff1f1", "#f2a3a3")
    res = chip("✓ " + word[0], "ok") if ok else chip("✕ " + word[1], "bad")
    body = ""
    if open_ and criteria:
        body += blk("<span>{</span><span>{</span>criteria<span>}</span><span>}</span>") + f'<div style="font:400 24px/1.35 {F};">{criteria}</div>'
    if open_ and reasoning:
        body += blk("REASONING") + f'<div style="font:400 24px/1.35 {F};">{reasoning}</div>'
    toggle = chip("Hide reasoning ⌃", "hide") if open_ else chip("See reasoning ⌄", "hide")
    return (f'<div style="background:{bg};border:2px solid {bd};border-radius:14px;padding:18px 20px;display:flex;flex-direction:column;gap:10px;">'
            f'<div style="display:flex;align-items:center;gap:10px;"><span style="font:500 28px/1.1 {F};">{name}</span>{chip(ver, "ver")}'
            f'<span style="margin-left:auto;display:flex;gap:8px;">{res}{toggle}</span></div>'
            f'<div style="font:400 20px/1.3 {F};color:#555;">{desc}</div>{body}</div>')


def tool_call(name, json, ok):
    bar = GREEN if ok else RED
    return (f'<div style="display:flex;flex-direction:column;gap:12px;border-left:6px solid {bar};padding-left:16px;">'
            f'{label("Agent Tool Call", mark="ok" if ok else "bad")}'
            f'<div style="background:#f3f3f3;border:2px solid #e5e5e5;border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:12px;">'
            f'<div style="font:500 24px/1 {F};">{name}</div>'
            f'<div style="background:#fff;border:2px solid #e5e5e5;border-radius:12px;padding:16px 20px;font:400 24px/1.5 {M};white-space:pre;">{json}</div></div></div>')


def expected_tool(name, field, value):
    return (f'<div style="font:500 24px/1 {F};">Expected Tool Calls</div>'
            f'<div style="background:#f3f3f3;border:2px solid #e5e5e5;border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:12px;">'
            f'<div style="font:500 24px/1 {F};">{name}</div>'
            f'<div style="background:#fff;border:2px solid #e5e5e5;border-radius:12px;padding:14px 18px;display:flex;flex-direction:column;gap:8px;">'
            f'<div style="font:500 22px/1 {F};">{field}</div><div style="font:400 22px/1 {F};color:#333;">{value}</div></div></div>')


def rule_box(op, value, ok=True):
    return (f'<div style="background:#effbf1;border:2px solid #86d39a;border-radius:14px;padding:16px 18px;display:flex;flex-direction:column;gap:12px;">'
            f'<div style="display:flex;align-items:center;"><span style="font:600 24px/1 {F};">Evaluation criteria</span><span style="margin-left:auto;">{chip("✓ Pass", "ok")}</span></div>'
            f'<div style="display:flex;gap:10px;"><span style="background:#1b1a17;color:#fff;border-radius:10px;padding:12px 18px;font:400 22px/1 {F};">{op} ⌄</span>'
            f'<span style="flex:1;background:#fff;border:2px solid #e5e5e5;border-radius:10px;padding:12px 18px;font:400 22px/1 {F};">{value}</span></div></div>')


def panel(left, right, right_title=None, height=626, split="1fr 1fr"):
    rt = f'<div style="font:500 24px/1 {F};">{right_title}</div>' if right_title else ""
    return (f'<div style="height:{height}px;box-sizing:border-box;background:#fff;border:3px solid #1b1a17;border-radius:18px;box-shadow:8px 8px 0 #1b1a17;'
            f'padding:28px;display:grid;grid-template-columns:{split};gap:28px;width:100%;color:#1a1a1a;font-family:{F};">'
            f'<div style="display:flex;flex-direction:column;gap:12px;min-height:0;overflow:hidden;">{left}</div>'
            f'<div style="display:flex;flex-direction:column;gap:14px;border-left:2px solid #eee;padding-left:28px;min-height:0;overflow:hidden;">{rt}{right}</div></div>')


def hl(w):
    return f'<span style="background:#ffd84d;border-radius:4px;padding:0 3px;">{w}</span>'
