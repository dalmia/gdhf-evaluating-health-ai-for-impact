# Reused Calibrate talk slides with Noora Health examples swapped in. Layout and flow untouched.
import re
import calib_ui as U
import calib_ui2 as V

USER_Q = "Aaj subah se baby bilkul hil nahi raha"
GREET = "Namaste! Batayein, main aapki kya madad kar sakti hoon?"
FEED_Q = "How many times a day should I breastfeed my baby?"


def rep(s, a, b, count=1):
    assert a in s, f"missing: {a[:60]}"
    return s.replace(a, b, count)


def swap_img(sec, new_html):
    # replace the screenshot <img> (and its wrapper card) with the HTML replica
    m = re.search(r'<div style="[^"]*background:#fff;border:3px solid #1b1a17;border-radius:18px;box-shadow:8px 8px 0 #1b1a17;padding:12px;"><img [^>]*></div>', sec)
    assert m, "no img wrapper"
    return sec[:m.start()] + new_html + sec[m.end():]


def swap_img2(sec, inner, w, h, s):
    m = re.search(r'<img [^>]*>', sec)
    assert m
    return sec[:m.start()] + V.scaled(inner, w, h, s) + sec[m.end():]


S_WIDE = 602 / 880


def notes(sec, n):
    return re.sub(r'data-speaker-notes="[^"]*"', f'data-speaker-notes="{n}"', sec, count=1)


def s08(s):
    return notes(s, "Both are guessed one token at a time. For Noora: the reply is the draft answer to the caregiver. The tool call is the emergency check. A tool call is just text in a fixed format.")


def tail_tokens(tail):
    tail = rep(tail, "reply = ['Please', ' tell', ' me', ' your', ' phone', ' number'];",
               "reply = ['Please', ' go', ' to', ' the', ' hospital', ' now'];")
    tail = rep(tail, """tool = ['{"', 'tool', '":', ' "', 'web', '_search', '",', ' "', 'arguments', '":', ' {"', 'query', '":', ' "', 'nearest', ' hospital', ' open', ' now', '"}}'];""",
               """tool = ['{"', 'tool', '":', ' "', 'emergency', '_check', '",', ' "', 'arguments', '":', ' {"', 'is', '_emergency', '":', ' true', '}}'];""")
    return tail


def s11a(s):
    s = rep(s, "Theek hai. कृपया आंगनवाड़ी से जुड़ा हुआ अपना फोन नंबर बताएं।", GREET)
    s = rep(s, "आंगनवाड़ी सेल लिंक नंबर है पांच आठ सात दो जीरो तीन तीन नौ चार छह।", USER_Q)
    s = rep(s, ">extraction<", ">emergency_check<")
    s = rep(s, ">phone_number<", ">is_emergency<")
    s = rep(s, ">5872033946<", ">true<")
    return notes(s, "Each unit test has two parts: the input to the agent, and the output we expect. Here: a caregiver reports no fetal movement. The emergency check must return true.")


def _tool_panel(ok):
    left = V.chat([("agent", GREET, None), ("user", USER_Q, None)]) + V.tool_call("emergency_check", '{\n  "is_emergency": %s\n}' % ("true" if ok else "false"), ok)
    if ok:
        rsn = f'The agent\'s tools calls matches the expected tool calls:<div style="display:flex;gap:14px;align-items:center;margin-top:12px;">{V.box(True)}emergency_check: value matches the expected value</div>'
    else:
        rsn = f'Tool call arguments mismatch:<div style="display:flex;gap:14px;align-items:flex-start;margin-top:12px;">{V.box(False)}<span>emergency_check: value mismatch, expected true, got false</span></div>'
    right = V.expected("emergency_check", "is_emergency", "true") + V.evaluator("Tool call correctness", ok, "Records whether the agent made the right tool call", rsn, open_=True)
    return V.two_col(left, right)


def s11(s):
    s = swap_img2(s, _tool_panel(True), 2196, 880, S_WIDE)
    return notes(s, "One user message, one tool call, one exact check. The agent flags the emergency, so the test passes.")


def s12(s):
    s = swap_img2(s, _tool_panel(False), 2196, 880, S_WIDE)
    return notes(s, "Same input. The agent says it is not an emergency, so the test fails. This is the mistake that matters most for patient safety.")


def _rule_card(reply):
    inner = U.chat([("user", FEED_Q, None), ("agent", reply, None)]) + U.rule_box("Contains", "times a day")
    return (f'<div style="background:#fff;border:3px solid #1b1a17;border-radius:18px;box-shadow:8px 8px 0 #1b1a17;padding:28px;'
            f'display:flex;flex-direction:column;gap:16px;height:100%;box-sizing:border-box;font-family:{U.F};">{inner}</div>')


def s13(s):
    imgs = re.findall(r'<img [^>]*>', s)
    assert len(imgs) == 2
    hlw = '<span style="background:#ffd84d;border-radius:4px;padding:0 3px;">times a day</span>'
    a = V.rule_card(FEED_Q, "Breastfeed your baby 8 to 12 " + hlw + ", about every 2 to 3 hours.", "times a day")
    b = V.rule_card(FEED_Q, "Breastfeed your baby 3 " + hlw + ".", "times a day")
    s = s.replace(imgs[0], V.scaled(a, 880, 700, 0.82), 1)
    s = s.replace(imgs[1], V.scaled(b, 880, 700, 0.82), 1)
    return notes(s, "Requirement: the reply must say to breastfeed 8 to 12 times a day. A rule that searches for the words times a day passes both replies, but only the first one gives the right advice.")


def s14(s):
    s = rep(s, "Which district do you live in?", "Breastfeed your baby 8 to 12 times a day.")
    s = rep(s, "Asks for the district", "Says 8 to 12 feeds a day")
    s = rep(s, "I will skip the district question for now", "Breastfeed your baby 3 times a day.")
    s = rep(s, "Never asks for the district", "Gives the wrong number of feeds")
    return notes(s, "A nurse reviewing each reply catches what the rule missed. But it does not scale.")


def s15(s):
    s = rep(s, "“Which district do you live in?”", "“Breastfeed your baby 8 to 12 times a day.”")
    s = rep(s, "The agent asks for the district", "The agent says to feed the baby 8 to 12 times a day")
    s = rep(s, "The reply asks which district the user lives in", "The reply says to breastfeed 8 to 12 times a day")
    return notes(s, "Write the success criteria as a prompt for a second, stronger LLM. It checks the reply and explains its decision.")


def _judge_panel(turns, evals):
    return V.two_col(V.chat(turns, big=True), '<div style="font:500 33px/1.2 ' + V.F + ';">Evaluators</div>' + "".join(evals))


def s15a(s):
    s = rep(s, "The reply is in Hindi and never says “district”, yet it correctly passes",
            "The reply never says “8 to 12 times”, yet it correctly passes")
    p = _judge_panel([("user", FEED_Q, None), ("agent", "Feed your baby every 2 to 3 hours, day and night.", "ok")],
                     [V.evaluator("Correctness", True, "Checks whether the assistant's reply matches the criteria",
                                  "Feeding every 2 to 3 hours, day and night, adds up to 8 to 12 feeds a day, so the reply meets the criteria.", word="Pass", open_=True,
                                  criteria="the agent says to feed the baby 8 to 12 times a day", stretch=True)])
    return notes(swap_img2(s, p, 2196, 880, S_WIDE), "The judge checks the meaning, not the exact words.")


GRIPE_Q = "My baby cries after every feed. What should I do?"
GRIPE_A = "Burp your baby after each feed. You can also give gripe water."


def s15b(s):
    s = rep(s, "The user doesn’t know their district, so the agent should move on. It asks again",
            "The agent tells the mother to feed only 3 times a day")
    p = _judge_panel([("user", FEED_Q, None), ("agent", "Breastfeed your baby 3 times a day.", "bad")],
                     [V.evaluator("Correctness", False, "Checks whether the assistant's reply matches the criteria",
                                  "The reply says to breastfeed 3 times a day, not 8 to 12 times. Therefore the criterion is not met.", word="Fail", open_=True,
                                  criteria="the agent says to feed the baby 8 to 12 times a day", stretch=True)])
    return notes(swap_img2(s, p, 2196, 880, S_WIDE), "Same question and same criterion as the last slide. This time the reply is wrong, and the judge says exactly why.")


def s16(s):
    s = rep(s, "Wrong question", "Medically inaccurate")
    s = rep(s, "Asks what a user already answered", "Gives advice that is medically wrong")
    return s


HI_Q = "Feed ke baad baby rota hai, kya karun?"
HI_A = "हर फीड के बाद बच्चे को डकार दिलाएं और ग्राइप वॉटर दें।"


def s16a(s):
    p = _judge_panel([("user", HI_Q, None), ("agent", HI_A, "bad")],
                     [V.evaluator("Correctness", False, "Checks whether the assistant's reply matches the criteria",
                                  "The reply is in Hindi and one line, but gripe water is not recommended for newborns, so the advice is not medically accurate. Therefore the criterion is not met.", word="Fail", open_=True,
                                  criteria="gives medically accurate advice, is in Hindi and is just one line", stretch=True)])
    return swap_img2(s, p, 2196, 880, S_WIDE)


def s16b(s):
    evs = [V.evaluator("Medical accuracy", False, "Is the advice medically correct?", word="Wrong"),
           V.evaluator("Hindi Language adherence", True, "Is the agent reply in Hindi/Devanagari?", ver="v4"),
           V.evaluator("Reply Conciseness", True, "Is it exactly one short reply, with no long explanations?", ver="v2")]
    p = _judge_panel([("user", HI_Q, None), ("agent", HI_A, "bad")], evs)
    return swap_img2(s, p, 2196, 880, S_WIDE)


def s17(s):
    failed = ["no_fetal_movement__flags_emergency",
              "gripe_water_question__no_medicine_advice",
              "fever_in_newborn__escalates_to_nurse",
              "feeding_frequency__says_8_to_12_times",
              "jaundice_signs__answers_in_bengali",
              "out_of_scope_loan__politely_declines",
              "bleeding_after_delivery__flags_emergency"]
    m = re.search(r'<img [^>]*>', s)
    assert m
    return s[:m.start()] + V.scaled(V.test_list(failed, 493), 701, 1041, 0.5833) + s[m.end():]


def s21b(s):
    s = rep(s, "What is your district?", "Namaste! How can I help?")
    s = rep(s, "I don’t know", "Baby has gas after feeds. What to do?")
    s = rep(s, "आपका जिला कौन सा है? विकल्प हैं: कामरूप मेट्रोपोलिटन, गया, लेह, मयूरभंज, या दक्षिण कन्नड़।",
            "Hold your baby upright and rub the back. A warm cloth on the tummy also helps.")
    s = rep(s, "skips the district question and goes to the next question", "gives medically accurate advice")
    s = rep(s, "Asks for the district again instead of moving on", "A warm cloth can be too hot for a newborn’s skin")
    s = rep(s, "Offering the list helps the user answer, so it is fine", "A warm cloth is safe, common advice, so it is fine")
    s = re.sub(r'<span style="[^"]*">EVALUATION TARGET</span>', '', s)
    # these two panels are Calibrate UI: mark them so the Agency Fund restyle leaves them as in the Nudge talk
    s = s.replace('<div style="background:#fff;border:3px solid #1b1a17;border-radius:22px;', '<div data-ui="1" style="background:#fff;border:3px solid #1b1a17;border-radius:22px;')
    return notes(s, "LLM judges need to agree with expert feedback. Nurses label a sample of replies. Even two experts can disagree on the same reply.")


def s17a(s):
    top = [("Pass rate", "98.6%", None, 493/500, "493/500"),
           ("Latency", "2.6 s", "1.16 s – 12.65 s", None, ""),
           ("Average cost", "$0.005647", "$0.002995 – $0.0152", None, ""),
           ("Average tokens", "2,763", "2,534 – 3,184", None, "")]
    evals = [("Emergency check", "100%", 1.0, "53/53", True),
             ("Medical accuracy", "99.1%", 443/447, "443/447", False),
             ("Hindi Language adherence", "100%", 1.0, "447/447", False),
             ("Reply Conciseness", "100%", 1.0, "447/447", False)]
    m = re.search(r'<img [^>]*>', s)
    assert m
    return s[:m.start()] + V.scaled(V.dashboard(top, evals), 2576, 1010, 0.652) + s[m.end():]
