"""
Build index.html for the "how to AI" panel series.

The page opens on a hub of panel tiles. Each panel is described entirely by
data (its pieces, their canvas positions, which click each appears on); one
small engine renders whichever panel you open. Adding a panel = adding a
config block below plus its extracted art.

Every asset is embedded as a base64 data URI, so the page is one file.

    python3 src/build.py
"""
import base64
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOON = 4  # placeholder tiles


def uri(path):
    b = open(path, "rb").read()
    ext = path.rsplit(".", 1)[1].lower()
    mt = "jpeg" if ext in ("jpg", "jpeg") else "png"
    return f"data:image/{mt};base64," + base64.b64encode(b).decode()


def manifest(panel):
    return json.load(open(os.path.join(ROOT, "assets", panel, "manifest.json")))


# ------------------------------------------------------------------ panel 1
P1_STEPS = [
    [("char_bubble", "char", ""), ("top_s01", "seg", "b2t")],
    [("robot", "char", ""), ("top_s02", "seg", "b2t"), ("callout_caribbean", "callout", "")],
    [("top_s03", "seg", "l2r"), ("callout_twokids", "callout", "")],
    [("top_s04", "seg", "l2r"), ("callout_disneyland", "callout", "")],
    [("top_s05", "seg", "b2t"), ("callout_tellmemore", "callout", "")],
    [("top_s06", "seg", "l2r"), ("callout_september", "callout", "")],
    [("top_s07", "seg", "l2r"), ("callout_october", "callout", "")],
    [("top_s08", "seg", "l2r"), ("callout_hotels", "callout", "")],
    [("top_s09", "seg", "b2t"), ("callout_auntgift", "callout", "")],
    [("top_s10", "seg", "l2r"), ("callout_auntlike", "callout", "")],
    [("bot_s01", "seg", "t2b"), ("callout_lowkey", "callout", "")],
    [("bot_s02", "seg", "l2r"), ("callout_camping", "callout", "")],
    [("bot_s03", "seg", "l2r"), ("callout_cabin", "callout", "")],
    [("bot_s04", "seg", "t2b"), ("callout_youhatebugs", "callout", "")],
    [("bot_s05", "seg", "b2t"), ("callout_bugspray", "callout", "")],
    [("bot_s06", "seg", "b2t"), ("callout_letmesee", "callout", "")],
]
P1_CAPTIONS = [
    "“I’m planning a family trip. Where should we go?”",
    "“The Caribbean is a great option.”",
    "“I have two kids under 10.”",
    "“Ah, Disneyland then.”",
    "“Ooh, yeah. Tell me more.”",
    "“The best time to go is September.”",
    "“No, the kids are in school. October.”",
    "“Great. Let me find hotels.”",
    "“We’ll stay with family. What gift can I get my aunt?”",
    "“What is your aunt like?”",
    "“No, something more low-key.”",
    "“How about camping?”",
    "“Renting a cabin sounds good. But how could it go wrong?”",
    "“You hate bugs.”",
    "“No, it’ll be okay. I’ll bring bug spray. What else?”",
    "“Let me see…”",
]
P1_MOTIF = (
    '<polyline points="8,58 34,40 60,46 86,22 112,30" fill="none" stroke="var(--violet)" '
    'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    '<polyline points="8,58 34,40 60,46" fill="none" stroke="var(--orange)" stroke-width="5" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="8" cy="58" r="6" fill="var(--orange)"/><circle cx="34" cy="40" r="6" fill="var(--violet)"/>'
    '<circle cx="60" cy="46" r="6" fill="var(--orange)"/><circle cx="86" cy="22" r="6" fill="var(--violet)"/>'
    '<circle cx="112" cy="30" r="6" fill="var(--violet)"/>'
)


def panel1():
    m = manifest("panel1")
    W, H = m["canvas"]
    A = {a["name"]: a for a in m["assets"]}

    def pc(name, kind, direction, step):
        a = A[name]
        z = {"credit": 1, "seg": 100 - step, "char": 200,
             "callout": 300, "title": 400}[kind]
        return {
            "src": uri(os.path.join(ROOT, "assets", "panel1", name + ".png")),
            "x": a["x"], "y": a["y"], "w": a["w"],
            "in": step, "z": z, "dir": direction, "rise": kind == "callout",
        }

    # The hand-drawn title and the credit line are on the board from the start.
    def always(name, z):
        a = A[name]
        return {
            "src": uri(os.path.join(ROOT, "assets", "panel1", name + ".png")),
            "x": a["x"], "y": a["y"], "w": a["w"],
            "in": 0, "z": z, "dir": "", "rise": False,
        }

    pieces = [always("credit", 1), always("title", 400)]
    for i, items in enumerate(P1_STEPS, start=1):
        for name, kind, direction in items:
            pieces.append(pc(name, kind, direction, i))

    return {
        "id": "talking", "name": "Talking <em>with</em> AI",
        "canvas": [W, H], "reveal": len(P1_STEPS),
        "caps": P1_CAPTIONS, "pieces": pieces, "motif": P1_MOTIF,
        "outro": uri(os.path.join(ROOT, "assets", "closing.jpg")),
    }


# ------------------------------------------------------------------ panel 2
P2_MOTIF = (
    '<rect x="34" y="16" width="52" height="40" rx="4" fill="none" stroke="var(--ink)" stroke-width="3.5"/>'
    '<path d="M40 22c8 6 -6 10 4 14s-6 8 6 12 -4 6 6 8" fill="none" stroke="var(--violet)" '
    'stroke-width="2.5" stroke-linecap="round"/>'
    '<path d="M8 40c8 -6 18 -4 24 -2" fill="none" stroke="var(--orange)" stroke-width="3.5" stroke-linecap="round"/>'
    '<path d="M88 44c8 2 16 4 24 -2" fill="none" stroke="var(--orange)" stroke-width="3.5" stroke-linecap="round"/>'
    '<circle cx="60" cy="40" r="5" fill="var(--violet)"/>'
)


def panel2():
    m = manifest("panel2")
    W, H = m["canvas"]
    A = {a["name"]: a for a in m["assets"]}

    def pc(name, step, z, direction="", until=None):
        a = A[name]
        d = {
            "src": uri(os.path.join(ROOT, "assets", "panel2", name + ".png")),
            "x": a["x"], "y": a["y"], "w": a["w"],
            "in": step, "z": z, "dir": direction, "rise": False,
        }
        if until is not None:
            d["until"] = until
        return d

    pieces = [
        pc("credit", 0, 1),
        pc("box", 2, 10),
        pc("arrow_in", 2, 20, "l2r", until=4),    # "reads" (step 5) has its own connecting arrow all the way in
        pc("arrow_out", 3, 20, "l2r", until=7),   # replaced by arrow_takesaction_out once it appears (step 8)
        pc("giant_ai", 2, 30, until=3),           # removed once the tangle appears
        pc("squiggle", 4, 35, until=4),           # the tangle itself — removed once the flow diagram starts
        pc("box_robot", 4, 34),                   # the robot in the tangle — stays through the flow-diagram reveal
        pc("magic", 4, 45, until=4),               # "It's like magic..." — only while the tangle's still a mystery
        # the flow diagram, one click per layer, in the order Alyssa laid the
        # layers out (top of her layers panel first): reads -> interprets ->
        # takes action -> the result goes back out -> then the three things
        # that feed "takes action" -> the tagline.
        pc("reads", 5, 36),
        pc("interprets", 6, 37),
        pc("takes_action", 7, 38),
        pc("arrow_takesaction_out", 8, 39),
        pc("tools", 9, 40),
        pc("access", 10, 41),
        pc("guardrails", 11, 42),
        pc("tagline", 12, 43),
        pc("output", 3, 50),
        pc("char_bubble", 1, 60),
        pc("title", 4, 70),
    ]
    return {
        "id": "aidoing", "name": "What is the AI <em>doing?</em>",
        "canvas": [W, H], "reveal": 12,
        "caps": [
            "Human tells the AI what to do",
            "The instruction goes in",
            "The AI returns output or actions",
            "It's like magic...",
            "It reads the instructions.",
            "It interprets what they mean.",
            "Then it takes action.",
            "...and sends the result back out.",
            "Using whatever tools it has.",
            "Whatever access it's been given.",
            "Within whatever guardrails are in place.",
            "Take it one step at a time.",
        ],
        "pieces": pieces, "motif": P2_MOTIF,
        "outro": uri(os.path.join(ROOT, "assets", "closing.jpg")),
    }


P3_MOTIF = (
    '<circle cx="10" cy="35" r="6" fill="var(--orange)"/>'
    '<path d="M16 35 C30 35 30 18 46 18" fill="none" stroke="var(--violet)" stroke-width="4" stroke-linecap="round"/>'
    '<rect x="50" y="8" width="32" height="20" rx="3" fill="none" stroke="var(--violet)" stroke-width="3.5"/>'
    '<text x="66" y="23" font-size="14" text-anchor="middle" fill="var(--violet)" font-family="monospace">7</text>'
    '<path d="M16 35 C30 35 30 52 46 52" fill="none" stroke="var(--orange)" stroke-width="4" stroke-linecap="round"/>'
    '<rect x="50" y="42" width="32" height="20" rx="3" fill="none" stroke="var(--orange)" stroke-width="3.5"/>'
    '<text x="66" y="57" font-size="13" text-anchor="middle" fill="var(--orange)" font-family="monospace">7~</text>'
)


def panel3():
    m = manifest("panel3")
    W, H = m["canvas"]
    A = {a["name"]: a for a in m["assets"]}

    def pc(name, step, z, until=None, full=False):
        a = A[name]
        d = {
            "src": uri(os.path.join(ROOT, "assets", "panel3", name + ".png")),
            "x": a["x"], "y": a["y"], "w": a["w"],
            "in": step, "z": z, "dir": "", "rise": False,
        }
        if until is not None:
            d["until"] = until
        if full:
            d["full"] = True
        return d

    CLOSING = uri(os.path.join(ROOT, "assets", "closing.jpg"))

    # Part 1 (steps 1-15): probabilistic branch fully (now on top, purple),
    # then deterministic fully (now on bottom, green) — same shape as panel
    # 1's two conversation branches. Every piece here is a complete PSD
    # group; nothing needed splitting or merging. Each branch's label lands
    # last, after its mechanics have played out.
    #
    # Step 16 is the closing image, mid-panel. Everything from part 1 stays
    # on screen straight through part 2 *except* the simple pattern-match
    # box and the 'Probabilistic' label — those get swapped out (part 2's
    # PSD supplies a merged pattern+guess box and a fresh 'Prob + Determ'
    # label at the same spot) for the guardrails build-up.
    pieces = [
        pc("credit", 0, 1),
        pc("char_bubble", 1, 90),
        # Note: "det_frame"/"det_reads" and "prob_frame"/"prob_reads" are
        # named for what they meant in the *original* (pre-swap) art — the
        # frame+robot and "reads instructions" graphics stayed pinned to
        # their original canvas position when Alyssa redid the layout, only
        # their surrounding content moved. So the piece that's actually at
        # the TOP now (Probabilistic's new home) is the one still named
        # "det_*", and the one at the BOTTOM is still named "prob_*" — this
        # only affects these two pairs; every other piece's name already
        # matches its new position.
        pc("det_frame", 2, 10),
        pc("det_output_frame", 2, 12),
        pc("det_reads", 3, 20),
        pc("prob_pattern", 4, 41, until=16),
        pc("prob_guess", 5, 42, until=16),
        pc("prob_returns", 6, 43),
        pc("prob_returns_most", 6, 44, until=16),
        pc("label_probabilistic", 7, 31, until=16),
        pc("prob_frame", 8, 30),
        pc("prob_reads", 9, 40),
        pc("det_opens", 10, 21),
        pc("det_inputs", 11, 22),
        pc("det_calc_returns", 12, 23),
        pc("det_ai_reads", 13, 24),
        pc("det_returns", 14, 25),
        pc("label_deterministic", 15, 11),

        # step 16: the closing image, mid-panel this time — click advances
        # normally rather than returning to the hub (that's reserved for the
        # real outro at the very end).
        {"src": CLOSING, "x": 0, "y": 0, "w": W, "in": 16, "until": 16,
         "z": 500, "dir": "", "rise": False, "full": True},

        # Part 2 (steps 17-22): the probabilistic box (top) swaps its simple
        # pattern-match content for the merged box, then guardrails build in.
        pc("pattern_guess", 17, 41),
        pc("constrain", 18, 45),
        pc("ai_checks", 19, 46),
        pc("human_checks", 20, 47),
        pc("confidence_note", 21, 44),
        pc("label_probdeterm", 22, 31),   # named last, after seeing how it works
    ]
    return {
        "id": "determprob", "name": "Deterministic <em>vs</em> Probabilistic",
        "canvas": [W, H], "reveal": 22,
        "caps": [
            "“Calculate 2 + 5.”",
            "An AI would do this.",
            "It reads the instructions.",
            "Pattern-matches 2 + 5...",
            "...and gets 7 as its best guess.",
            "Returns 7 — most of the time.",
            "That's probabilistic.",
            "A calculator does this differently.",
            "It reads the instructions.",
            "“Opens” the calculator.",
            "“Inputs” 2 + 5.",
            "The calculator returns 7.",
            "The AI “reads” 7.",
            "Returns 7.",
            "That's deterministic.",
            "",
            "But you can combine both.",
            "Constrain its answers...",
            "...have it check its own answer...",
            "...or have a human check it.",
            "Returns 7 — with higher confidence.",
            "And that's Prob + Determ.",
        ],
        "pieces": pieces, "motif": P3_MOTIF,
        "outro": CLOSING,
    }


P4_MOTIF = (
    '<circle cx="60" cy="18" r="9" fill="var(--violet)"/>'
    '<circle cx="30" cy="42" r="7" fill="var(--violet)" opacity=".8"/>'
    '<circle cx="90" cy="42" r="7" fill="var(--violet)" opacity=".8"/>'
    '<circle cx="15" cy="62" r="6" fill="var(--orange)" opacity=".7"/>'
    '<circle cx="60" cy="62" r="6" fill="var(--orange)" opacity=".7"/>'
    '<circle cx="105" cy="62" r="6" fill="var(--orange)" opacity=".7"/>'
    '<path d="M60 27v6M35 46l18 9M85 46l-18 9M22 56l-4 3M60 68v-1M98 56l4 3" '
    'fill="none" stroke="var(--rule)" stroke-width="2.5" stroke-linecap="round"/>'
)


def panel4():
    m = manifest("panel4")
    W, H = m["canvas"]
    A = {a["name"]: a for a in m["assets"]}

    def pc(name, step, z):
        a = A[name]
        return {
            "src": uri(os.path.join(ROOT, "assets", "panel4", name + ".png")),
            "x": a["x"], "y": a["y"], "w": a["w"],
            "in": step, "z": z, "dir": "", "rise": False,
        }

    # The base (frame, title, human, output) has no agents in it yet; each
    # agent is its own complete group, arrow included, so one click each.
    # Head chef -> expediter -> the two workers -> the evaluator -> the
    # reporter -> back out, then the tagline reappears (it closed the
    # single-agent panel too) right before the closing image.
    pieces = [
        pc("credit", 0, 1),
        pc("base", 1, 10),
        pc("agent_head_chef", 2, 20),
        pc("agent_expediter", 3, 21),
        pc("agent_grill_cook", 4, 22),
        pc("agent_pastry_chef", 5, 23),
        pc("agent_sous_chef", 6, 24),
        pc("agent_server", 7, 25),
        pc("server_exit_arrow", 8, 26),
        pc("tagline", 9, 30),
    ]
    return {
        "id": "multiagent", "name": "What is the AI doing, <em>together?</em>",
        "canvas": [W, H], "reveal": 9,
        "caps": [
            "It's not always just one AI.",
            "The Head Chef plans — the planner agent.",
            "The Expediter orchestrates — the orchestrator agent.",
            "The Grill Cook does the work — a worker agent.",
            "So does the Pastry Chef — another worker agent.",
            "The Sous Chef checks the work — the evaluator agent.",
            "The Server reports back — the reporter agent.",
            "...and sends the result back out.",
            "Take it one step at a time.",
        ],
        "pieces": pieces, "motif": P4_MOTIF,
        "outro": uri(os.path.join(ROOT, "assets", "closing.jpg")),
    }


# ------------------------------------------------------------------ panel 5
P5_MOTIF = (
    '<rect x="6" y="8" width="28" height="20" rx="3" fill="none" stroke="var(--ink)" stroke-width="4"/>'
    '<rect x="46" y="38" width="28" height="20" rx="3" fill="none" stroke="var(--ink)" stroke-width="4"/>'
    '<rect x="86" y="8" width="28" height="20" rx="3" fill="none" stroke="var(--ink)" stroke-width="4"/>'
    '<path d="M14 28c0 10 10 6 24 10" fill="none" stroke="var(--orange)" stroke-width="3.5" stroke-linecap="round"/>'
    '<path d="M74 44c8 -8 6 -20 20 -24" fill="none" stroke="var(--violet)" stroke-width="3.5" stroke-linecap="round"/>'
)

P5_NODES = [
    ("scan", "", "Scan for new bills."),
    ("flag", "t2b", "Flag the relevant one."),
    ("research", "b2t", "Research the bill."),
    ("assess", "t2b", "Assess the impact."),
    ("draft", "b2t", "Draft a stance."),
    ("policy", "t2b", "Send it to policy review."),
    ("leadership", "b2t", "Get leadership sign-off."),
]


def panel5():
    m = manifest("panel5")
    W, H = m["canvas"]
    A = {a["name"]: a for a in m["assets"]}

    def piece(name, step, z, direction="", rise=False):
        a = A[name]
        return {
            "src": uri(os.path.join(ROOT, "assets", "panel5", name + ".png")),
            "x": a["x"], "y": a["y"], "w": a["w"],
            "in": step, "z": z, "dir": direction, "rise": rise,
        }

    pieces = [
        piece("credit", 0, 1),
        piece("mascot", 0, 2),
        piece("title", 0, 3),
    ]
    # step 1 is a blank beat: just the title and the mascot on the board,
    # before the flow starts at step 2.
    for step, (name, direction, _) in enumerate(P5_NODES, start=2):
        if direction:
            pieces.append(piece(f"arrow_{name}", step, step * 10 - 1, direction))
        pieces.append(piece(name, step, step * 10, rise=True))

    return {
        "id": "legislative", "name": "Legislative Policy <em>Tracking</em>",
        "canvas": [W, H], "reveal": len(P5_NODES) + 1,
        "caps": [""] + [c for _, _, c in P5_NODES],
        "pieces": pieces, "motif": P5_MOTIF,
        "outro": uri(os.path.join(ROOT, "assets", "closing.jpg")),
    }


def main():
    # "Legislative Policy Tracking" first; "What is the AI doing?" second;
    # the multi-agent take on it third; "Talking with AI" fourth;
    # "Deterministic vs Probabilistic" fifth.
    data = json.dumps(
        {"panels": [panel5(), panel2(), panel4(), panel1(), panel3()], "soon": SOON - 3},
        ensure_ascii=False,
    )
    html = TEMPLATE.replace("__DATA__", data)
    open(os.path.join(ROOT, "index.html"), "w").write(html)
    print(f"index.html  {len(html) / 1024 / 1024:.2f} MB")


TEMPLATE = r'''<title>Talking With AI</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=DM+Serif+Display&display=swap');

:root{
  --paper:#FFFFFF; --page-bg:#EAF3FB; --page-bg-2:#DCEBF7;
  --ink:#1B2A33; --grey:#5C7180; --rule:#CFE3F2;
  --deep-sky:#1F6FA8; --orange:#F0640A; --violet:#6A5BD0; --focus:#1F6FA8;
}
:root[data-theme="dark"]{
  --paper:#FFFFFF; --page-bg:#0E1A22; --page-bg-2:#132530;
  --ink:#EAF2F8; --grey:#9DB4C2; --rule:#25424F;
  --deep-sky:#7FC4EE; --orange:#F58A4B; --violet:#A99CF0; --focus:#7FC4EE;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#FFFFFF; --page-bg:#0E1A22; --page-bg-2:#132530;
    --ink:#EAF2F8; --grey:#9DB4C2; --rule:#25424F;
    --deep-sky:#7FC4EE; --orange:#F58A4B; --violet:#A99CF0; --focus:#7FC4EE;
  }
}

*{box-sizing:border-box;}
html,body{height:100%;}
body{
  margin:0;
  background:radial-gradient(120% 90% at 50% 0%, var(--page-bg-2) 0%, var(--page-bg) 62%);
  color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  overflow:hidden; -webkit-tap-highlight-color:transparent; user-select:none;
}

.hub{
  position:fixed; inset:0; z-index:1000;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:clamp(20px,4vh,40px); padding:48px 20px; overflow-y:auto;
  transition:opacity .4s ease;
}
.hub.hide{opacity:0;pointer-events:none;}
.hub-head{text-align:center;max-width:520px;}
.hub-head .eyebrow{justify-content:center;margin-bottom:10px;}
.hub-head h1{
  font-family:'DM Serif Display',Georgia,serif; font-weight:400;
  font-size:clamp(26px,4.4vw,38px); line-height:1.1; margin:0; color:var(--ink); text-wrap:balance;
}
.grid{display:grid; grid-template-columns:repeat(3, clamp(132px,20vw,190px)); gap:clamp(12px,1.8vw,20px);}
.tile{
  position:relative; aspect-ratio:1/1; border-radius:16px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:10px; padding:16px; text-align:center; font:inherit; color:var(--ink);
}
.tile--panel{
  background:var(--paper); border:1px solid var(--rule);
  box-shadow:0 14px 30px -16px rgba(19,58,84,.35); cursor:pointer;
  transition:transform .16s ease, box-shadow .16s ease, border-color .16s ease;
}
.tile--panel:hover, .tile--panel:focus-visible{
  transform:translateY(-4px); border-color:var(--deep-sky);
  box-shadow:0 22px 42px -18px rgba(19,58,84,.45); outline:none;
}
.tile--panel:focus-visible{outline:2px solid var(--focus);outline-offset:3px;}
.tile .motif{width:64%;height:auto;display:block;}
.tile .t-name{font-family:'DM Serif Display',Georgia,serif;font-size:clamp(13px,1.5vw,16px);line-height:1.2;}
.tile .t-name em{font-family:'Caveat',cursive;font-style:normal;font-weight:700;color:var(--orange);font-size:1.18em;}
.tile .t-open{font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--deep-sky);}
.tile--soon{border:1.5px dashed var(--rule);background:transparent;}
.tile--soon span{font-size:10px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--grey);opacity:.6;}

.wrap{
  position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
  padding:56px 16px 84px; overflow:hidden;
  opacity:0; pointer-events:none; transition:opacity .4s ease;
}
.wrap.live{opacity:1;pointer-events:auto;}
.board{
  position:relative;
  width:min(calc(100vw - 32px), calc((100vh - 132px) * var(--ar, 1.6)));
  max-width:100%;
  aspect-ratio:var(--arw,2400) / var(--arh,1500);
  background:var(--paper);
  border:1px solid var(--rule); border-radius:16px;
  box-shadow:0 24px 60px -20px rgba(19,58,84,.35), 0 2px 8px rgba(19,58,84,.12);
  cursor:pointer; overflow:hidden;
}
.piece{
  position:absolute; opacity:0;
  transition:opacity .5s ease, transform .5s ease, clip-path .55s ease;
  pointer-events:none;
}
.piece img{display:block;width:100%;height:auto;}
.piece.rise{transform:translateY(8px) scale(.985);}
.piece[data-dir="l2r"]{clip-path:inset(0 100% 0 0);}
.piece[data-dir="r2l"]{clip-path:inset(0 0 0 100%);}
.piece[data-dir="t2b"]{clip-path:inset(0 0 100% 0);}
.piece[data-dir="b2t"]{clip-path:inset(100% 0 0 0);}
.piece.show{opacity:1;transform:none;}
.piece.show[data-dir]{clip-path:inset(0 0 0 0);}

/* a piece that breaks out of the board to fill the screen, mid-sequence
   (not the panel's terminal outro — just styled the same way) */
.piece.full{
  position:fixed; inset:0; z-index:940;
  background:linear-gradient(#F3A2C0 0%, #F3A2C0 52%, #BAD79C 74%, #BAD79C 100%);
}
.piece.full img{width:100%;height:100%;object-fit:contain;display:block;}
@media (max-width:560px){
  .piece.full img{object-fit:cover;object-position:18% center;}
}

.outro{
  position:fixed; inset:0; z-index:905; opacity:0; pointer-events:none;
  transition:opacity .6s ease;
  background:linear-gradient(#F3A2C0 0%, #F3A2C0 52%, #BAD79C 74%, #BAD79C 100%);
}
.outro.show{opacity:1;pointer-events:auto;cursor:pointer;}
.outro img{width:100%;height:100%;object-fit:contain;display:block;}

.topbar{
  position:fixed; top:0; left:0; right:0;
  display:flex; align-items:center; justify-content:center;
  padding:12px 16px; font-size:12px; z-index:930; pointer-events:none;
  opacity:0; transition:opacity .4s ease;
}
.topbar.live{opacity:1;}
.topbar .btn{position:absolute;left:16px;top:10px;}
.topbar .hint{position:absolute;right:16px;top:15px;}
.topbar.at-end .hint, .topbar.at-end .eyebrow{display:none;}
.eyebrow{
  display:flex; align-items:center; gap:8px;
  letter-spacing:.14em; text-transform:uppercase;
  font-size:11px; font-weight:600; color:var(--grey);
}
.eyebrow .bead{width:6px;height:6px;border-radius:50%;background:var(--orange);}
.btn{
  pointer-events:auto; font:inherit; font-size:12px;
  color:var(--deep-sky); background:var(--paper);
  border:1px solid var(--rule); border-radius:999px; padding:6px 14px; cursor:pointer;
}
.btn:hover{border-color:var(--deep-sky);}
.btn:focus-visible{outline:2px solid var(--focus);outline-offset:2px;}
.hint{color:var(--grey);letter-spacing:.04em;}
.hint kbd{
  font:inherit; font-size:11px;
  background:var(--paper); border:1px solid var(--rule); border-radius:4px;
  padding:1px 5px; margin:0 1px; color:var(--deep-sky);
}

.status{
  position:fixed; left:50%; bottom:30px; transform:translateX(-50%);
  display:flex; flex-direction:column; align-items:center; gap:9px;
  z-index:10; width:min(92vw,760px); opacity:0; transition:opacity .4s ease;
}
.status.live{opacity:1;}
.status.at-end{opacity:0;pointer-events:none;}
.caption{
  font-family:'Caveat',cursive; font-size:clamp(18px,2.6vw,25px); font-weight:600;
  color:var(--deep-sky); min-height:1.2em; text-align:center; line-height:1;
}
.dots{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;}
.dot{
  width:7px; height:7px; border-radius:50%; background:var(--rule);
  border:0; padding:0; cursor:pointer; transition:background .2s ease, transform .2s ease;
}
.dot.on{background:var(--orange);}
.dot.cur{transform:scale(1.5);background:var(--deep-sky);}
.dot:focus-visible{outline:2px solid var(--focus);outline-offset:2px;}

@media (prefers-reduced-motion:reduce){*{transition:none !important;}}
@media (max-width:560px){
  .hint{display:none;}
  .wrap{padding:48px 12px 92px;}
  .board{width:min(calc(100vw - 24px), calc((100vh - 150px) * var(--ar,1.6)));}
  .topbar .eyebrow{font-size:10px;}
  .grid{grid-template-columns:repeat(2, clamp(130px,42vw,180px));}
  .outro img{object-fit:cover;object-position:18% center;}
}
</style>

<div class="hub" id="hub">
  <div class="hub-head">
    <div class="eyebrow"><span class="bead"></span>A hand-drawn series</div>
    <h1>Pick a panel</h1>
  </div>
  <div class="grid" id="grid"></div>
</div>

<div class="wrap" id="wrap">
  <div class="board" id="board" role="group" aria-label="Panel — click to reveal it step by step"></div>
</div>

<div class="outro" id="outro"><img id="outroImg" src="" alt="Closing illustration"></div>

<div class="topbar" id="topbar">
  <button class="btn" id="backBtn" type="button">← panels</button>
  <div class="eyebrow"><span class="bead"></span><span id="topName">Panel</span></div>
  <div class="hint"><kbd>click</kbd> or <kbd>space</kbd> forward · <kbd>←</kbd> back</div>
</div>

<div class="status" id="statusBar">
  <div class="caption" id="caption" aria-live="polite"></div>
  <div class="dots" id="dots"></div>
</div>

<script>
(function(){
  var DATA = __DATA__;
  var PANELS = DATA.panels;

  var hub = document.getElementById('hub');
  var grid = document.getElementById('grid');
  var wrap = document.getElementById('wrap');
  var board = document.getElementById('board');
  var outro = document.getElementById('outro');
  var outroImg = document.getElementById('outroImg');
  var topbar = document.getElementById('topbar');
  var statusBar = document.getElementById('statusBar');
  var captionEl = document.getElementById('caption');
  var dotsEl = document.getElementById('dots');
  var topName = document.getElementById('topName');

  var cur = null, step = 0, inPanel = false, pieceEls = [], total = 0;
  function tag(name){ return name.replace(/<[^>]+>/g, ''); }

  PANELS.forEach(function(P){
    var b = document.createElement('button');
    b.className = 'tile tile--panel'; b.type = 'button';
    b.setAttribute('aria-label', 'Open: ' + tag(P.name));
    b.innerHTML = '<svg class="motif" viewBox="0 0 120 70" aria-hidden="true">' + P.motif + '</svg>'
      + '<span class="t-name">' + P.name + '</span><span class="t-open">Open &rarr;</span>';
    b.addEventListener('click', function(){ openPanel(P); });
    grid.appendChild(b);
  });
  for (var i = 0; i < DATA.soon; i++){
    var s = document.createElement('div');
    s.className = 'tile tile--soon'; s.innerHTML = '<span>soon</span>';
    grid.appendChild(s);
  }

  function buildBoard(P){
    board.innerHTML = '';
    board.style.setProperty('--arw', P.canvas[0]);
    board.style.setProperty('--arh', P.canvas[1]);
    board.style.setProperty('--ar', (P.canvas[0] / P.canvas[1]).toFixed(4));
    pieceEls = [];
    var W = P.canvas[0], H = P.canvas[1];
    P.pieces.slice().sort(function(a, b){ return a.z - b.z; }).forEach(function(p){
      var el = document.createElement('div');
      el.className = 'piece' + (p.rise ? ' rise' : '') + (p.full ? ' full' : '');
      if (p.full){
        el.style.zIndex = p.z;
      } else {
        el.style.left = (p.x / W * 100).toFixed(4) + '%';
        el.style.top = (p.y / H * 100).toFixed(4) + '%';
        el.style.width = (p.w / W * 100).toFixed(4) + '%';
        el.style.zIndex = p.z;
      }
      if (p.dir) el.setAttribute('data-dir', p.dir);
      el.dataset.in = p['in'];
      el.dataset.until = (p.until == null ? '' : p.until);
      var img = document.createElement('img'); img.src = p.src; img.alt = '';
      el.appendChild(img);
      board.appendChild(el);
      pieceEls.push(el);
    });
    outroImg.src = P.outro || '';
  }

  function dotsFor(n){
    dotsEl.innerHTML = '';
    for (var i = 1; i <= n; i++){
      (function(k){
        var b = document.createElement('button');
        b.className = 'dot'; b.type = 'button';
        b.setAttribute('aria-label', 'Step ' + k);
        b.addEventListener('click', function(e){ e.stopPropagation(); go(k); });
        dotsEl.appendChild(b);
      })(i);
    }
  }

  function render(){
    var reveal = cur.reveal;
    var s = Math.min(step, reveal);
    var fullShowing = false;
    pieceEls.forEach(function(el){
      var pin = +el.dataset.in;
      var until = el.dataset.until === '' ? null : +el.dataset.until;
      var on = s >= pin && (until == null || s <= until);
      el.classList.toggle('show', on);
      if (on && el.classList.contains('full')) fullShowing = true;
    });
    var atOutro = !!cur.outro && step > reveal;
    var atEnd = atOutro || fullShowing;   // hide chrome for either kind of full-bleed moment
    var dots = Array.prototype.slice.call(dotsEl.children);
    dots.forEach(function(d, idx){
      d.classList.toggle('on', (idx + 1) <= step);
      d.classList.toggle('cur', (idx + 1) === step);
    });
    captionEl.textContent = (step > 0 && step <= reveal && cur.caps[step - 1]) ? cur.caps[step - 1] : '';
    outro.classList.toggle('show', atOutro);   // only the terminal outro returns to the hub on click
    topbar.classList.toggle('at-end', atEnd);
    statusBar.classList.toggle('at-end', atEnd);
  }
  function go(n){ step = Math.max(0, Math.min(total, n)); render(); }
  function next(){
    if (step < total) { go(step + 1); return; }
    if (cur.outro) backToHub();   // already on the terminal outro — advancing means "done"
  }
  function prev(){ if (step > 0) go(step - 1); }

  function openPanel(P){
    cur = P; inPanel = true;
    total = P.reveal + (P.outro ? 1 : 0);
    buildBoard(P);
    dotsFor(total);
    topName.textContent = tag(P.name);
    hub.classList.add('hide');
    wrap.classList.add('live');
    topbar.classList.add('live');
    statusBar.classList.add('live');
    step = 0; go(1);
  }
  function backToHub(){
    inPanel = false;
    wrap.classList.remove('live');
    topbar.classList.remove('live', 'at-end');
    statusBar.classList.remove('live', 'at-end');
    outro.classList.remove('show');
    hub.classList.remove('hide');
    step = 0;
  }

  document.getElementById('backBtn').addEventListener('click', function(e){ e.stopPropagation(); backToHub(); });
  board.addEventListener('click', function(){ if (inPanel) next(); });
  wrap.addEventListener('click', function(e){ if (inPanel && e.target === e.currentTarget) next(); });
  outro.addEventListener('click', function(e){ e.stopPropagation(); backToHub(); });
  document.addEventListener('keydown', function(e){
    if (!inPanel) return;
    if (e.key === ' ' || e.key === 'Spacebar' || e.key === 'ArrowRight'){ e.preventDefault(); next(); }
    else if (e.key === 'ArrowLeft'){ e.preventDefault(); prev(); }
    else if (e.key === 'Escape'){ backToHub(); }
  });
})();
</script>
'''

if __name__ == "__main__":
    main()
