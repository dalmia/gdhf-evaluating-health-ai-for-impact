# Agency Fund version: look of the master deck's Level 1 section (white slides, navy serif headings,
# gold highlighted words, Agency Fund logo top-right, dark multi-colour framework columns),
# with the Agency Fund design system filling in details the master deck doesn't show
# (navy-tinted soft shadows, bordered cards, 12px radius, gold-50 tints, Montserrat for small labels).
import re

NAVY = "#1f2a4d"        # master deck navy (headings, body text)
GOLD = "#c49a3c"        # master deck gold (highlighted words)
PURPLE = "#7a4f9a"
MUTED = "#4a5568"
BORDER = "#CED4DA"      # design system neutral-400 (visible card edge)
TINT = "#F1F3F5"        # design system neutral-100
SERIF = "Gelasio,Georgia,serif"  # Gelasio has Georgia's metrics, so every machine lays out the same
SANS = SERIF  # one typeface throughout, as in the master deck
SHADOW = "0 6px 20px rgba(0,51,102,.14)"  # design system: navy-tinted shadow


def _protect(t):
    # Calibrate UI replicas (Noto Sans / Geist) keep their original look: lift them out before restyling
    saved = []
    out, pos = [], 0
    for m in re.finditer(r'<div data-ui="1" style="[^"]*">|<div style="[^"]*(?:\'Noto Sans\'|\'Geist\'|\'Inter\')[^"]*">', t):
        if m.start() < pos:
            continue
        depth, k = 0, m.start()
        for tag in re.finditer(r'<div\b|</div>', t[m.start():]):
            depth += 1 if tag.group(0) == '<div' else -1
            if depth == 0:
                k = m.start() + tag.end()
                break
        out.append(t[pos:m.start()])
        out.append(f'@@UI{len(saved)}@@')
        saved.append(t[m.start():k])
        pos = k
    out.append(t[pos:])
    return "".join(out), saved


def af(t, logo_uuid):
    t, _saved = _protect(t)
    t = _af(t, logo_uuid)
    for i, blk in enumerate(_saved):
        t = t.replace(f'@@UI{i}@@', blk)
    # slide text that is not a Calibrate screenshot uses the deck typeface, never the UI sans
    def deck_font(m):
        return re.sub(r"'Geist'(?:,'Noto Sans')?,-apple-system,sans-serif", SERIF, m.group(0))
    t = re.sub(r'<section data-label="14 Manual review".*?</section>', deck_font, t, flags=re.S)
    # small labels above example boxes: bold, dark, uppercase, same treatment on every slide
    t = re.sub(r'<div style="font:500 \d+px/[\d.]+ [^;"]*;color:#4a5568;">Agent reply', f'<div style="font:700 26px/1 {SANS};color:{NAVY};letter-spacing:3px;text-transform:uppercase;">Agent reply', t)
    # small labels above example boxes: pill style, same as the FREE TEXT / STRUCTURED OUTPUT tags
    PILL = {'Agent reply': '#9A7003', 'Rule': '#7a4f9a', 'Reasoning': '#2b6cb0'}
    t = re.sub(r'<div style="font:700 \d+px/[\d.]+ Gelasio,Georgia,serif;color:#1f2a4d;letter-spacing:3px;text-transform:uppercase;">(Agent reply|Rule|Reasoning)<', lambda m: f'<div style="align-self:flex-start;background:{PILL[m.group(1)]};color:#fff;border-radius:999px;padding:9px 20px;font:700 26px/1 Gelasio,Georgia,serif;">{m.group(1)}<', t)
    # no all-caps letter-spaced styling anywhere on the slides (Calibrate UI panels keep their own look)
    return t


def _af(t, logo_uuid):
    t = re.sub(r"text-transform:\s*uppercase;?", "", t)
    t = re.sub(r"letter-spacing:\s*\d+(?:\.\d+)?(?:px|em);?", "", t)
    # reply vs tool call keep two different colours, as in the Nudge talk: reply = gold, tool call = navy
    def two_kinds(m):
        s = m.group(0).replace("#1f5fd1", GOLD)
        # bigger, readable label pills: square-ish tag, larger type, more padding
        s = s.replace("background:" + GOLD + ";color:#fff;border-radius:999px;padding:10px 20px;", "background:#9A7003;color:#fff;border-radius:999px;padding:10px 20px;")
        s = s.replace("border-radius:999px;padding:10px 20px;font:600 28px/1 'IBM Plex Mono',monospace;",
                      "border-radius:10px;padding:16px 28px;font:700 34px/1 'IBM Plex Mono',monospace;")
        return s
    t = re.sub(r'<section data-label="08 Two kinds of output".*?</section>', two_kinds, t, flags=re.S)

    def judge(m):
        s = m.group(0)
        box = "color:#1b1a17;background:#ffffff;border:2px solid #CED4DA;border-radius:12px;padding:16px 22px;"
        s = s.replace("<div style=\"font:500 40px/1.3 'Bricolage Grotesque',sans-serif;\">", "<div style=\"font:500 40px/1.3 'Bricolage Grotesque',sans-serif;" + box + "\">")
        s = s.replace("<div style=\"font:500 36px/1.3 'Bricolage Grotesque',sans-serif;text-wrap:pretty;\">", "<div style=\"font:500 36px/1.3 'Bricolage Grotesque',sans-serif;text-wrap:pretty;" + box + "\">")
        s = s.replace("font:600 28px/1 'IBM Plex Mono',monospace;color:#4a4740;", "font:700 26px/1 'IBM Plex Mono',monospace;color:#1f2a4d;letter-spacing:3px;text-transform:uppercase;")
        return s
    t = re.sub(r'<section data-label="15 LLM judge".*?</section>', judge, t, flags=re.S)
    # highlighted words -> gold text, as in the master deck
    def hl(m):
        low = m.group(1).replace(" ", "").lower()
        if "border-radius:999px" in low or "flex-shrink" in low:
            return m.group(0)
        if 'data-hl="h"' in m.group(0):
            return "<span>"
        return '<span data-afhl="1" style="color:#9A7003;font-weight:700;">'
    t = re.sub(r'<span(?: [^>]*?)? style="([^"]*background:\s*(?:#ffd84d|#1f5fd1|rgb\(31, 95, 209\)|rgb\(255, 216, 77\)|#c62828|#1a7f37)[^"]*)">', hl, t)
    # inside big slide headings: no highlight at all, plain heading text
    def plain_heading(m):
        return re.sub(r'<span data-afhl="1" style="[^"]*">', "<span>", m.group(0))
    t = re.sub(r'<div style="[^"]*font:\s*800 (?:96|120|128|140|200)px[^"]*">.*?</div>', plain_heading, t, flags=re.S)

    # fonts: serif for slide text like the master deck; Montserrat for small mono labels
    t = re.sub(r"'Bricolage Grotesque',sans-serif", SERIF, t)
    t = t.replace("font-family:'Bricolage Grotesque'", "font-family:Gelasio")
    t = re.sub(r"'IBM Plex Mono',monospace", SANS, t)
    t = t.replace("&quot;IBM Plex Mono&quot;, monospace", SANS).replace("&quot;Bricolage Grotesque&quot;, sans-serif", SERIF)

    t = t.replace("'IBM Plex Mono',monospace;color:#b44a06;", "'IBM Plex Mono',monospace;color:#9A7003;")
    # white slides, no grid
    t = re.sub(r"background-image:\s*linear-gradient\(rgba\(27,26,23,\.07\) 2px,transparent 2px\),linear-gradient\(90deg,rgba\(27,26,23,\.07\) 2px,transparent 2px\);\s*background-size:\s*60px 60px;", "", t)
    t = t.replace("#f6f3ea", "#FFFFFF")

    # cards: border first, soft navy shadow
    t = re.sub(r"box-shadow:\s*\d+px \d+px 0 #[0-9a-fA-F]{6}", f"box-shadow:{SHADOW}", t)
    t = re.sub(r"border:\s*[23]px solid #1b1a17", f"border:2px solid {BORDER}", t)
    t = t.replace("border-radius:24px", "border-radius:12px").replace("border-radius:20px", "border-radius:12px")

    # cards get their own fill (design system navy-50) so they read as cards on the white slide
    t = re.sub(r"background:\s*#fff;(\s*)border:2px solid " + BORDER, r"background:#E8EEF4;\1border:2px solid " + BORDER, t)
    # colour roles
    t = t.replace("#1f5fd1", NAVY).replace("#6d4fd1", PURPLE)
    t = t.replace("#ffd84d", TINT).replace("#1b1a17", NAVY).replace("#4a4740", MUTED)

    # orange is only a 'wrong answer' colour; where it is just an accent, use the Agency Fund gold
    def accent(m):
        sec = m.group(0)
        if re.search(r'data-label="(02 The reality|03 Where we build|Why Level 1 is hard)"', sec[:200]):
            sec = sec.replace("#b44a06", GOLD)
        if 'data-label="08 Two kinds of output"' in sec[:200]:
            # reply vs tool call keep two different colours, as in the Nudge talk: reply = gold, tool call = navy
            sec = sec.replace("#1f5fd1", GOLD)
            sec = sec.replace("border:3px solid #1b1a17;border-radius:24px;box-shadow:10px 10px 0 " + GOLD, "border:3px solid " + GOLD + ";border-radius:24px;box-shadow:10px 10px 0 " + GOLD)
        return sec
    t = re.sub(r'<section data-label=.*?</section>', accent, t, flags=re.S)

    # serif bold is wide: shrink large headings, loosen line height
    def big(m):
        w, size, lh = m.group(1), int(m.group(2)), float(m.group(3))
        if size < 60:
            return f"font:{w} {round(size * 0.86)}px/{max(lh, 1.25)}"
        return f"font:700 {round(size * 0.8)}px/{max(lh, 1.15)}"
    t = re.sub(r"font:\s*(\d00) (\d+)px/([\d.]+)", big, t)
    t = re.sub(r"letter-spacing:\s*-\d+px", "letter-spacing:0", t)
    t = t.replace("width: 1597px; height: 247px", "")

    # hierarchy: regular-weight body text in muted grey, headings stay navy
    def body(m):
        st = m.group(1)
        if "color:" in st.replace(" ", ""):
            return m.group(0)
        return f'<div style="{st};color:{MUTED};">'
    t = re.sub(r'<div style="([^"]*font:\s*[45]00 [^"]*?);?">', body, t)

    t = re.sub(r'(<div style="(?:flex:none;)?font:700 77px/1\.15 )', r'<div style="max-width:1500px;font:700 70px/1.15 ', t)
    t = t.replace('<div style="max-width:1500px;flex:none;', '<div style="flex:none;max-width:1500px;')
    t = t.replace('max-width:1500px;flex:none;font:700 77px', 'max-width:1500px;flex:none;font:700 70px').replace('flex:none;max-width:1500px;font:700 77px', 'flex:none;max-width:1500px;font:700 70px')
    # on navy slides, highlighted words use a bright gold so they stay readable
    def dark_hl(m):
        return m.group(0).replace('data-afhl="1" style="color:#9A7003;', 'data-afhl="1" style="color:#FBD654;')
    t = re.sub(r'<section data-label="Development outcomes".*?</section>', dark_hl, t, flags=re.S)
    # Agency Fund logo top-right on content slides, as in the master deck
    logo = f'<img src="{logo_uuid}" alt="The Agency Fund" style="position:absolute;top:44px;right:60px;height:72px;">'

    def add_logo(m):
        sec = m.group(0)
        label = re.search(r'data-label="([^"]*)"', sec).group(1)
        if label in ("00 Title", "21b2 Evaluate the evaluator") or "background:" + NAVY in sec[:600] or "padding:0;" in sec[:600]:
            return sec
        sec = sec.replace('style="', 'style="position:relative;', 1)
        return sec.replace("</section>", logo + "</section>")
    t = re.sub(r'<section data-label=.*?</section>', add_logo, t, flags=re.S)

    link = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Gelasio:wght@400;500;600;700&display=swap">'
    t = t.replace("</helmet>", link + "\n</helmet>", 1)
    t = t.replace("body{margin:0;background:#1b1a17;}", f"body{{margin:0;background:{NAVY};}}")
    return t
