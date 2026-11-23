import json, re, sys, uuid, base64, os
sys.path.insert(0, os.path.dirname(__file__))
import new_slides as N

R = '/home/claude/repos'
base = open(f'{R}/Nudge-talk/index.html').read()
comm = open(f'{R}/calibrate-ai-commons-talk/index.html').read()


def part(html, typ):
    m = re.search(r'(<script type="__bundler/%s">)(.*?)(</script>)' % typ, html, re.S)
    return m


man = json.loads(part(base, 'manifest').group(2))
man.update(json.loads(part(comm, 'manifest').group(2)))
tN = json.loads(part(base, 'template').group(2))
tC = json.loads(part(comm, 'template').group(2))


def sections(t):
    return {m.group(1): m.group(0) for m in re.finditer(r'<section data-label="([^"]*)".*?</section>', t, re.S)}


SN, SC = sections(tN), sections(tC)
head = tN[:tN.find('<section')]
tail = tN[tN.rfind('</section>') + len('</section>'):]

# logos -> manifest entries
logos = []
for f, alt, h in [('b93ca651-image.png', 'J-PAL', 84), ('6ac30810-image.png', 'APHRC', 96), ('af-transparent.png', 'The Agency Fund', 104)]:
    p = f'/mnt/user-data/uploads/{f}' if f != 'af-transparent.png' else '/home/claude/build/af-transparent.png'
    u = str(uuid.uuid5(uuid.NAMESPACE_URL, 'gdhf-' + f))
    man[u] = {'mime': 'image/png', 'compressed': False, 'data': base64.b64encode(open(p, 'rb').read()).decode()}
    logos.append((u, alt, h))

# master deck slide images, if present: /home/claude/build/master/slide-NN.png
def qr_uuid(name):
    u = str(uuid.uuid5(uuid.NAMESPACE_URL, 'gdhf-' + name))
    man[u] = {'mime': 'image/png', 'compressed': False, 'data': base64.b64encode(open(f'/home/claude/build/{name}.png', 'rb').read()).decode()}
    return u


def img_slide(path, what):
    u = str(uuid.uuid5(uuid.NAMESPACE_URL, 'gdhf-' + os.path.basename(path)))
    man[u] = {'mime': 'image/png', 'compressed': False, 'data': base64.b64encode(open(path, 'rb').read()).decode()}
    return (f'<section data-label="{what}" data-speaker-notes="{what}" '
            f'style="box-sizing:border-box;padding:0;background:#fff;display:flex;align-items:center;justify-content:center;">'
            f'<img src="{u}" alt="{what}" style="width:100%;height:100%;object-fit:contain;display:block;"></section>')


def master(n, what):
    p = f'/home/claude/build/master/slide-{n:02d}.png'
    if not os.path.exists(p):
        return N.master_placeholder(n, what)
    u = str(uuid.uuid5(uuid.NAMESPACE_URL, f'gdhf-master-{n}'))
    man[u] = {'mime': 'image/png', 'compressed': False, 'data': base64.b64encode(open(p, 'rb').read()).decode()}
    return (f'<section data-label="Master {n}" data-speaker-notes="Master deck slide {n}: {what}" '
            f'style="box-sizing:border-box;padding:0;background:#fff;display:flex;align-items:center;justify-content:center;">'
            f'<img src="{u}" alt="{what}" style="width:100%;height:100%;object-fit:contain;display:block;"></section>')


import noora_part2 as P
tail = P.tail_tokens(tail)

def mark_ui(s):
    # panels that replicate the Calibrate UI keep the Nudge-talk look in every theme
    return s.replace('<div style="width:100%;background:#fff;border:3px solid #1b1a17;border-radius:22px;', '<div data-ui="1" style="width:100%;background:#fff;border:3px solid #1b1a17;border-radius:22px;').replace(
        '<div style="flex:1;min-height:0;margin-top:12px;background:#fff;border:3px solid #1b1a17;border-radius:22px;', '<div data-ui="1" style="flex:1;min-height:0;margin-top:12px;background:#fff;border:3px solid #1b1a17;border-radius:22px;')


def fix_maisha(s):
    s = s.replace("Noora Health and Intelehealth", "Noora Health and Maisha Meds")
    i = s.index('alt="Intelehealth logo"')
    card_start = s.rfind('<div style="flex:1;min-width:0;background:#fff;', 0, i)
    card_end = s.rindex('</div></div></section>')
    num = lambda n: f'<div style="font:600 30px/1.4 \'IBM Plex Mono\',monospace;color:#9A7003;flex:none;">{n}</div>'
    item = lambda n, t, w=500: f'<div style="display:flex;gap:22px;align-items:flex-start;">{num(n)}<div style="font:{w} 38px/1.25 \'Bricolage Grotesque\',sans-serif;text-wrap:pretty;">{t}</div></div>'
    card = (s[card_start:s.index('>', card_start) + 1]
            + f'<div style="height:88px;display:flex;align-items:center;"><img src="{qr_uuid("maisha")}" alt="Maisha Meds logo" style="display:block;height:88px;width:auto;object-fit:contain;"></div>'
            + item("01", "Sending patients AI-drafted instructions for their medicines")
            + item("02", "Using LLM judges to track and monitor the quality of these messages over time")
            + item("03", "Flagging messages that contradict a listed warning or describe its directions of use incorrectly", 800)
            + '</div>')
    return s[:card_start] + card + s[card_end:].replace('</div></div></section>', '</div></section>', 1)


def fix_recap(s):
    # remove the bottom callout; colour loop 2 and 3 descriptions like their loops
    s = re.sub(r'<div style="display:grid;grid-template-columns:1fr 2fr;column-gap:36px;height:108px;.*?What we learn in the field updates what counts as a pass</div></div></div></div>', '', s, flags=re.S)
    s = s.replace("text-wrap:pretty;\">Evaluate your LLM judges", "text-wrap:pretty;color:#b44a06;\">Evaluate your LLM judges")
    s = s.replace("text-wrap:pretty;\">Monitor after launch", "text-wrap:pretty;color:#1a7f37;\">Monitor after launch")
    return s


def fix08(s):
    # bigger token text and taller token boxes so the animation reads from the back of the room
    s = s.replace("font:600 34px/1.2 'Bricolage Grotesque',sans-serif;background:{{ t.bg }}", "font:600 46px/1.25 'Bricolage Grotesque',sans-serif;background:{{ t.bg }}")
    s = s.replace("font:500 28px/1.25 'IBM Plex Mono',monospace;background:{{ t.bg }}", "font:500 36px/1.3 'IBM Plex Mono',monospace;background:{{ t.bg }}")
    s = s.replace("min-height:150px", "min-height:220px")
    return s


def fix06(s):
    s = s.replace("padding:8px 18px;font:600 24px/1 'IBM Plex Mono',monospace;\">Translation", "padding:10px 22px;font:600 30px/1 'IBM Plex Mono',monospace;\">Translation")
    s = s.replace("font:500 30px/1.25 'Bricolage Grotesque',sans-serif;color:#4a4740;\">My baby", "font:600 40px/1.3 'Bricolage Grotesque',sans-serif;color:#1b1a17;\">My baby")
    # fill the space: bigger boxes and text, content sits higher, room left for the translation
    s = s.replace("height:112px", "height:150px").replace("font:600 34px/1.2", "font:600 38px/1.2")
    s = s.replace("height:220px", "height:320px").replace("font:800 52px/1.05", "font:800 64px/1.05")
    s = s.replace("flex-direction:column;gap:20px;", "flex-direction:column;gap:28px;")
    s = s.replace("grid-template-columns:1.3fr 70px 290px 70px 1fr;align-items:center;", "grid-template-columns:1.3fr 80px 300px 80px 1.1fr;align-items:center;padding-bottom:110px;")
    return s

order = [
    N.title(logos),
    SN['02 The reality'], SN['03 Where we build'],
    fix06(SN['06 AI is non-deterministic']), SN['07 Next-word guessing'],
    N.why_fail(),
    N.framework(), N.feedback(),
    N.noora(),
    N.dev_outcomes(),
    # Part 2: Calibrate talk slides reused as-is (original screenshots)
    N.level1_divider(),
    fix08(SN['08 Two kinds of output']),
    P.s11a(SN['11a Define the test']), P.s11(SN['11 Tool call single turn']), P.s12(SN['12 Tool call multi-turn']),
    P.s13(SN['13 Free text']), P.s14(SN['14 Manual review']), P.s15(SN['15 LLM judge']),
    P.s15a(SN['15a Judge passes']), P.s15b(SN['15b Judge fails']),
    P.s16(SN['16 Many ways to fail']), P.s16a(SN['16a One rule for everything']), P.s16b(SN['16b One judge per check']),
    P.s17(SN['17 Many test cases']), P.s17a(SN['17a Where errors come from']), SN['18 Choosing a model'].replace('background:#e9e6dd;color:#1b1a17;">CLOSED<', 'background:#495057;color:#fff;">CLOSED<').replace('>OPEN SOURCE<', '>OPEN<'), SN['20 Ship with confidence'],
    SN['21 Something fishy'], SN['21a Judges make mistakes'], 
    P.s21b(SC['21b Human labels']), mark_ui(SC['Measure alignment']), mark_ui(SC['21d Tune the judge']), SC['21b2 Evaluate the evaluator'],
    fix_recap(SC['22 Recap']), fix_maisha(SC['Noora and Intelehealth'].replace('LLM judges score open-ended responses', 'LLM judges score free-text replies').replace('#b44a06', '#9A7003')), SC['23 Calibrate'], N.demo_title(), SC['23a Open source'].replace('Join our WhatsApp', 'Join the WhatsApp'),
    # Part 3: demo
    N.resources([(qr_uuid('qr_playbook'), '4-level evaluation framework', 'eval.playbook.org.ai', '#1f5fd1'), (qr_uuid('qr_calibrate'), 'Calibrate', 'calibrate.artpark.ai', '#1a7f37')]),
    N.thank_you(logos),
]
tpl = head + '\n'.join(order) + tail
GELASIO = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gelasio:wght@400;500;600;700&family=Inter:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;500&display=swap">'
tpl = tpl.replace('</helmet>', GELASIO + '\n</helmet>', 1)

# prune manifest: keep fonts/scripts, and images referenced in the template
keep = {}
for k, v in man.items():
    if not v['mime'].startswith('image/') or k in tpl:
        keep[k] = v


import io
from PIL import Image as _I
for k, v in list(keep.items()):
    if v['mime'] in ('image/png', 'image/jpeg') and not v.get('compressed') and len(v['data']) > 400_000:
        im = _I.open(io.BytesIO(base64.b64decode(v['data'])))
        if im.width > 2400:
            im = im.resize((2400, round(im.height * 2400 / im.width)), _I.LANCZOS)
        buf = io.BytesIO()
        im.convert('RGB').save(buf, 'JPEG', quality=86, optimize=True)
        keep[k] = {'mime': 'image/jpeg', 'compressed': False, 'data': base64.b64encode(buf.getvalue()).decode()}


def enc(o):
    return json.dumps(o, ensure_ascii=False).replace('</', '<\\u002F')


out = base
m = part(out, 'manifest'); out = out[:m.start(2)] + enc(keep) + out[m.end(2):]
m = part(out, 'template'); out = out[:m.start(2)] + enc(tpl) + out[m.end(2):]
out = re.sub(r'<title>[^<]*</title>', '<title>Navigating Challenges in Evaluating Health AI for Impact</title>', out, count=1)
open('/home/claude/build/index.html', 'w').write(out)
import af_theme
tpl_af = af_theme.af(tpl, logos[2][0])
out2 = base
m = part(out2, 'manifest'); out2 = out2[:m.start(2)] + enc(keep) + out2[m.end(2):]
m = part(out2, 'template'); out2 = out2[:m.start(2)] + enc(tpl_af) + out2[m.end(2):]
out2 = re.sub(r'<title>[^<]*</title>', '<title>Navigating Challenges in Evaluating Health AI for Impact (Agency Fund style)</title>', out2, count=1)
out2 = out2.replace('background: #faf9f5', 'background: #F8F9FA').replace('background:#faf9f5', 'background:#F8F9FA')
open('/home/claude/build/index-af.html', 'w').write(out2)
print('slides', len(order), 'MB', round(len(out) / 1e6, 2), 'manifest', len(keep), '/', len(man))
