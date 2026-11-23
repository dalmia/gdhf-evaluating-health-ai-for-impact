# Pixel-faithful rebuild of the Calibrate screenshots in the Nudge talk (measured from the original PNGs),
# so the examples can change while the look stays identical. Authored at the screenshot's own pixel size
# and scaled into the same wrapper the screenshot used.
F = "'Inter','Noto Sans Devanagari',-apple-system,sans-serif"
M = "'IBM Plex Mono',ui-monospace,monospace"
G, R = "#16a34a", "#dc2626"


def scaled(inner, w, h, s):
    return (f'<div style="position:relative;width:{round(w*s)}px;height:{round(h*s)}px;overflow:hidden;border-radius:8px;">'
            f'<div style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;transform:scale({s});transform-origin:0 0;'
            f'background:#fff;color:#171717;font-family:{F};">{inner}</div></div>')


def label(t, right=False, mark=None):
    b = ""
    if mark == "ok":
        b = f'<span style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:#dcfce7;color:{G};font-size:22px;margin-left:12px;">✓</span>'
    elif mark == "bad":
        b = f'<span style="display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:#fde2e4;color:{R};font-size:22px;margin-left:12px;">✕</span>'
    al = "flex-end" if right else "flex-start"
    return f'<div style="align-self:{al};display:flex;align-items:center;font:500 31px/1.2 {F};">{t}{b}</div>'


def bubble(t, user=False, big=False):
    bg = "#f3f3f3" if user else "#fff"
    al = "flex-end" if user else "flex-start"
    fs = 36 if big else 31
    return (f'<div style="align-self:{al};max-width:{"76%" if user else "82%"};box-sizing:border-box;background:{bg};border:2px solid #e5e5e5;'
            f'border-radius:26px;padding:22px 28px;font:400 {fs}px/1.45 {F};">{t}</div>')


def chat(turns, big=False):
    out = []
    for role, text, mark in turns:
        if role == "user":
            out += [label("User", right=True), bubble(text, user=True, big=big)]
        else:
            if mark:
                bar = G if mark == "ok" else R
                out.append(f'<div style="display:flex;flex-direction:column;gap:14px;border-left:7px solid {bar};padding-left:26px;margin-left:-2px;">'
                           f'{label("Agent", mark=mark)}{bubble(text, big=big)}</div>')
            else:
                out += [label("Agent"), bubble(text, big=big)]
    return "".join(out)


def tool_call(name, js, ok):
    bar = G if ok else R
    return (f'<div style="display:flex;flex-direction:column;gap:20px;border-left:7px solid {bar};padding-left:26px;margin-top:8px;">'
            f'{label("Agent Tool Call", mark="ok" if ok else "bad")}'
            f'<div style="background:#f3f3f3;border:2px solid #ebebeb;border-radius:30px;padding:26px 30px 28px;display:flex;flex-direction:column;gap:20px;">'
            f'<div style="font:400 31px/1 {F};">{name}</div>'
            f'<div style="background:#fff;border:2px solid #e5e5e5;border-radius:16px;padding:22px 26px;font:400 30px/1.5 {M};white-space:pre;">{js}</div></div></div>')


def expected(name, field, value):
    return (f'<div style="font:500 31px/1.2 {F};">Expected Tool Calls</div>'
            f'<div style="background:#f3f3f3;border:2px solid #ebebeb;border-radius:30px;padding:28px 30px;display:flex;flex-direction:column;gap:22px;">'
            f'<div style="font:400 31px/1 {F};">{name}</div>'
            f'<div style="background:#fafafa;border:2px solid #ececec;border-radius:22px;padding:22px 22px;display:flex;flex-direction:column;gap:18px;">'
            f'<div style="font:400 29px/1 {F};padding-left:2px;">{field}</div>'
            f'<div style="background:#fff;border:2px solid #e5e5e5;border-radius:12px;padding:18px 24px;font:400 31px/1.2 {F};">{value}</div></div></div>')


def chip(kind, text):
    st = {"ok": f"background:#dcfce7;color:{G};", "bad": f"background:#fde2e4;color:{R};",
          "hide": "background:#faf5ff;color:#7e22ce;border:2px solid #d8b4fe;",
          "see": "background:#e6f0fa;color:#1e4f80;border:2px solid #a8c6e6;",
          "ver": "background:#fff;color:#333;border:2px solid #e2e2e2;font-size:22px;padding:4px 9px;"}[kind]
    return f'<span style="display:inline-flex;align-items:center;gap:8px;border-radius:8px;padding:7px 14px;font:400 28px/1.2 {F};white-space:nowrap;{st}">{text}</span>'


def evaluator(name, ok, desc, reasoning=None, word=None, ver="v1", open_=False, criteria=None, stretch=False):
    bg, bd = ("#e9f8ee", "#8fdcaa") if ok else ("#fde6e7", "#f4a4a8")
    w = word or ("Correct" if ok else "Wrong")
    res = chip("ok", "✓ " + w) if ok else chip("bad", "✕ " + w)
    tog = chip("hide", "Hide reasoning ⌃") if open_ else chip("see", "See reasoning ⌄")
    body = ""
    pill = lambda t: f'<span style="align-self:flex-start;background:#171717;color:#fff;border-radius:8px;padding:8px 14px;font:700 28px/1 {M};letter-spacing:{"4px" if t=="REASONING" else "0"};">{t}</span>'
    if open_ and criteria:
        body = (f'<div style="height:2px;background:{bd};opacity:.5;margin:6px 0 10px;"></div>'
                f'{pill("<span>{</span><span>{</span>criteria<span>}</span><span>}</span>")}'
                f'<div style="font:400 34px/1.4 {F};margin-bottom:22px;">{criteria}</div>'
                f'{pill("REASONING")}<div style="font:400 33px/1.45 {F};">{reasoning}</div>')
    elif open_ and reasoning:
        body = (f'<div style="height:2px;background:{bd};opacity:.5;margin:6px 0 4px;"></div>'
                f'<div style="font:600 22px/1 {F};letter-spacing:4px;color:#555;">REASONING</div>'
                f'<div style="font:400 30px/1.45 {F};">{reasoning}</div>')
    grow = "flex:1;" if stretch else ""
    return (f'<div style="{grow}background:{bg};border:2px solid {bd};border-radius:24px;padding:24px 26px;display:flex;flex-direction:column;gap:14px;">'
            f'<div style="display:flex;align-items:flex-start;gap:14px;"><div style="display:flex;align-items:center;gap:14px;flex:1;font:400 35px/1.25 {F};">{name}{chip("ver", ver)}</div>'
            f'<div style="display:flex;gap:12px;flex:none;">{res}{tog}</div></div>'
            f'<div style="font:400 29px/1.45 {F};color:#444;">{desc}</div>{body}</div>')


def box(ok):
    c = G if ok else R
    return f'<span style="display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:7px;background:{c};color:#fff;font-size:24px;flex:none;">{"✓" if ok else "✕"}</span>'


def two_col(left, right):
    return (f'<div style="display:grid;grid-template-columns:1085px 1fr;height:880px;box-sizing:border-box;">'
            f'<div style="padding:30px 56px 30px 34px;display:flex;flex-direction:column;gap:18px;border-right:6px solid #ececec;overflow:hidden;">{left}</div>'
            f'<div style="padding:30px 30px 30px 46px;display:flex;flex-direction:column;gap:22px;overflow:hidden;">{right}</div></div>')


WIDE = (2196, 880)


def rule_card(question, reply_html, value):
    # 1100x800 card, same parts as the original "rule check" screenshots, sized to fill the card
    inner = (f'<div style="padding:30px 34px;display:flex;flex-direction:column;gap:16px;height:700px;box-sizing:border-box;justify-content:flex-start;">'
             f'{label("User", right=True)}{bubble(question, user=True, big=True).replace("max-width:76%", "max-width:92%")}'
             f'{label("Agent")}{bubble(reply_html, big=True).replace("max-width:82%", "max-width:92%").replace("align-self:flex-start;", "align-self:stretch;min-height:150px;box-sizing:border-box;")}'
             f'<div style="background:#effbf1;border:2px solid #86d39a;border-radius:20px;padding:22px 24px;display:flex;flex-direction:column;gap:18px;margin-top:6px;">'
             f'<div style="display:flex;align-items:center;"><span style="font:600 34px/1 {F};">Evaluation criteria</span><span style="margin-left:auto;">{chip("ok", "✓ Pass")}</span></div>'
             f'<div style="display:flex;gap:14px;"><span style="background:#171717;color:#fff;border-radius:12px;padding:18px 24px;font:400 32px/1 {F};">Contains ⌄</span>'
             f'<span style="flex:1;background:#fff;border:2px solid #e5e5e5;border-radius:12px;padding:18px 24px;font:400 32px/1 {F};">{value}</span></div></div></div>')
    return inner


def test_list(failed, passed_count):
    cb = '<span style="flex:none;width:36px;height:36px;border:3px solid #a3a3a3;border-radius:8px;box-sizing:border-box;"></span>'
    x = f'<span style="flex:none;width:40px;height:40px;border-radius:50%;background:#fde2e4;color:{R};display:flex;align-items:center;justify-content:center;font:400 26px/1 {F};">✕</span>'
    rows = "".join(f'<div style="display:flex;align-items:center;gap:20px;height:92px;padding-left:52px;">{cb}{x}'
                   f'<span style="font:400 30px/1 {F};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{n}</span></div>' for n in failed)
    head = lambda caret, dot, txt: (f'<div style="display:flex;align-items:center;gap:16px;height:90px;padding:0 24px 0 28px;border-bottom:2px solid #e5e5e5;">'
                                    f'<span style="color:#555;font:400 26px/1 {F};">{caret}</span><span style="width:14px;height:14px;border-radius:50%;background:{dot};"></span>'
                                    f'<span style="font:400 30px/1 {F};color:#666;flex:1;">{txt}</span>{cb}</div>')
    return (f'<div style="width:701px;height:1041px;box-sizing:border-box;border-top:2px solid #e5e5e5;position:relative;">'
            f'<div style="position:absolute;left:218px;top:-4px;width:94px;height:4px;background:#171717;"></div>'
            f'<div style="padding:24px 20px 0;"><div style="border:2px solid #e2e2e2;border-radius:12px;height:78px;display:flex;align-items:center;gap:18px;padding:0 24px;font:400 30px/1 {F};color:#777;">'
            f'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>Search tests</div>'
            f'<div style="font:400 23px/1 {F};color:#777;padding:22px 0 26px;">Select all</div></div>'
            f'<div style="border-top:2px solid #e5e5e5;">{head("⌄", "#ef4444", f"Failed ({len(failed)})")}</div>'
            f'<div style="padding:8px 0 10px;">{rows}</div>'
            f'{head("›", "#22c55e", f"Passed ({passed_count})")}</div>')


def dashboard(top, evals):
    info = '<span style="display:inline-flex;width:30px;height:30px;border:2.5px solid #777;border-radius:50%;align-items:center;justify-content:center;font:600 18px/1 sans-serif;color:#777;margin-left:12px;">i</span>'
    ext = '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="2" style="margin-left:auto;"><path d="M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"/></svg>'
    def bar(frac):
        return (f'<div style="flex:1;height:12px;border-radius:6px;background:#eee;overflow:hidden;">'
                f'<div style="width:{frac*100:.1f}%;height:100%;background:#5bc466;border-radius:6px;"></div></div>')
    cards = ""
    for name, sub, extra, frac, n in top:
        b = (f'<div style="display:flex;align-items:center;gap:24px;margin-top:22px;">{bar(frac)}<span style="font:400 30px/1 {F};color:#333;">{n}</span></div>'
             if frac is not None else f'<div style="font:400 28px/1 {F};color:#444;margin-top:24px;">{extra}</div>')
        cards += (f'<div style="border:2px solid #e5e5e5;border-radius:22px;padding:30px 28px;">'
                  f'<div style="display:flex;align-items:center;font:500 34px/1 {F};">{name}{"" if name=="Pass rate" else info}</div>'
                  f'<div style="font:600 46px/1 {F};margin-top:22px;">{sub}</div>{b}</div>')
    ev = ""
    for name, pct, frac, n, tool in evals:
        ev += (f'<div style="border:2px solid #e5e5e5;border-radius:22px;padding:30px 28px;">'
               f'<div style="display:flex;align-items:center;font:500 34px/1 {F};">{name}{info}{"" if tool else ext}</div>'
               f'<div style="font:600 46px/1 {F};margin-top:22px;">{pct}</div>'
               f'<div style="display:flex;align-items:center;gap:24px;margin-top:22px;">{bar(frac)}<span style="font:400 30px/1 {F};color:#333;">{n}</span></div></div>')
    return (f'<div style="padding:38px 44px;box-sizing:border-box;height:1010px;">'
            f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:28px;">{cards}</div>'
            f'<div style="font:600 36px/1 {F};margin:48px 0 28px;">Evaluators</div>'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px;">{ev}</div></div>')
