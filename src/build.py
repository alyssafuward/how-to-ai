"""
Build index.html for "Talking with AI" — a hand-drawn conversation that
reveals itself one exchange at a time.

Every asset is embedded as a base64 data URI so the page is a single
self-contained file.

    python3 src/build.py
"""
import base64
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P1 = os.path.join(ROOT, "assets", "panel1")


def uri(path):
    b = open(path, "rb").read()
    return "data:image/png;base64," + base64.b64encode(b).decode()


# Each reveal step lists the pieces that appear on that click.
#   (asset name, kind, wipe direction)
STEPS = [
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
    [("bot_s04", "seg", "l2r"), ("callout_driving", "callout", "")],
    [("bot_s05", "seg", "b2t"), ("callout_newnotexp", "callout", "")],
    [("bot_s06", "seg", "b2t"), ("callout_letmesee", "callout", "")],
]

CAPTIONS = [
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
    "“Renting a cabin sounds good.”",
    "“Driving distance?”",
    "“No, somewhere new, but not expensive.”",
    "“Let me see…”",
]


def main():
    man = json.load(open(os.path.join(P1, "manifest.json")))
    W, H = man["canvas"]
    A = {a["name"]: a for a in man["assets"]}

    def piece(name, kind, direction, step):
        a = A[name]
        z = {"credit": 1, "seg": 100 - step, "char": 200,
             "callout": 300, "title": 400}[kind]
        rise = " rise" if kind == "callout" else ""
        d = f' data-dir="{direction}"' if direction else ""
        return (
            f'<div class="piece {kind}{rise}" data-step="{step}"{d} '
            f'style="left:{a["x"] / W * 100:.4f}%;top:{a["y"] / H * 100:.4f}%;'
            f'width:{a["w"] / W * 100:.4f}%;z-index:{z}">'
            f'<img src="{uri(os.path.join(P1, name + ".png"))}" alt=""></div>'
        )

    ct = A["credit"]
    pieces = [
        f'<div class="piece credit" '
        f'style="left:{ct["x"] / W * 100:.4f}%;top:{ct["y"] / H * 100:.4f}%;'
        f'width:{ct["w"] / W * 100:.4f}%;z-index:1">'
        f'<img src="{uri(os.path.join(P1, "credit.png"))}" alt=""></div>'
    ]
    for i, items in enumerate(STEPS, start=1):
        for name, kind, direction in items:
            pieces.append(piece(name, kind, direction, i))

    html = TEMPLATE.format(
        pieces="\n  ".join(pieces),
        nsteps=len(STEPS),
        captions=json.dumps(CAPTIONS, ensure_ascii=False),
    )
    open(os.path.join(ROOT, "index.html"), "w").write(html)
    print(f"index.html  {len(html) / 1024 / 1024:.2f} MB")


TEMPLATE = r'''<title>Talking With AI</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=DM+Serif+Display&display=swap');

:root{{
  --paper:#FFFFFF; --page-bg:#EAF3FB; --page-bg-2:#DCEBF7;
  --ink:#1B2A33; --grey:#5C7180; --rule:#CFE3F2;
  --deep-sky:#1F6FA8; --orange:#F0640A; --violet:#6A5BD0; --focus:#1F6FA8;
}}
:root[data-theme="dark"]{{
  --paper:#FFFFFF; --page-bg:#0E1A22; --page-bg-2:#132530;
  --ink:#EAF2F8; --grey:#9DB4C2; --rule:#25424F;
  --deep-sky:#7FC4EE; --orange:#F58A4B; --violet:#A99CF0; --focus:#7FC4EE;
}}
@media (prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --paper:#FFFFFF; --page-bg:#0E1A22; --page-bg-2:#132530;
    --ink:#EAF2F8; --grey:#9DB4C2; --rule:#25424F;
    --deep-sky:#7FC4EE; --orange:#F58A4B; --violet:#A99CF0; --focus:#7FC4EE;
  }}
}}

*{{box-sizing:border-box;}}
html,body{{height:100%;}}
body{{
  margin:0;
  background:radial-gradient(120% 90% at 50% 0%, var(--page-bg-2) 0%, var(--page-bg) 62%);
  color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  overflow:hidden; -webkit-tap-highlight-color:transparent; user-select:none;
}}

.wrap{{
  position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
  padding:56px 16px 84px; overflow:hidden;
}}
.board{{
  position:relative;
  width:min(calc(100vw - 32px), calc((100vh - 132px) * 1.6));
  max-width:100%;
  aspect-ratio:2400 / 1500;
  background:var(--paper);
  border:1px solid var(--rule); border-radius:16px;
  box-shadow:0 24px 60px -20px rgba(19,58,84,.35), 0 2px 8px rgba(19,58,84,.12);
  cursor:pointer; overflow:hidden;
}}
.piece{{
  position:absolute; opacity:0;
  transition:opacity .5s ease, transform .5s ease, clip-path .55s ease;
  pointer-events:none;
}}
.piece img{{display:block;width:100%;height:auto;}}
.piece.credit{{opacity:1;}}
.piece.rise{{transform:translateY(8px) scale(.985);}}
.piece[data-dir="l2r"]{{clip-path:inset(0 100% 0 0);}}
.piece[data-dir="r2l"]{{clip-path:inset(0 0 0 100%);}}
.piece[data-dir="t2b"]{{clip-path:inset(0 0 100% 0);}}
.piece[data-dir="b2t"]{{clip-path:inset(100% 0 0 0);}}
.piece.show{{opacity:1;transform:none;}}
.piece.show[data-dir]{{clip-path:inset(0 0 0 0);}}

.topbar{{
  position:fixed; top:0; left:0; right:0;
  display:flex; align-items:center; justify-content:center;
  padding:12px 16px; font-size:12px; z-index:20; pointer-events:none;
}}
.topbar .btn{{position:absolute;left:16px;top:10px;}}
.topbar .hint{{position:absolute;right:16px;top:15px;}}
.eyebrow{{
  display:flex; align-items:center; gap:8px;
  letter-spacing:.14em; text-transform:uppercase;
  font-size:11px; font-weight:600; color:var(--grey);
}}
.eyebrow .bead{{width:6px;height:6px;border-radius:50%;background:var(--orange);}}
.btn{{
  pointer-events:auto; font:inherit; font-size:12px;
  color:var(--deep-sky); background:var(--paper);
  border:1px solid var(--rule); border-radius:999px; padding:6px 14px; cursor:pointer;
}}
.btn:hover{{border-color:var(--deep-sky);}}
.btn:focus-visible{{outline:2px solid var(--focus);outline-offset:2px;}}
.hint{{color:var(--grey);letter-spacing:.04em;}}
.hint kbd{{
  font:inherit; font-size:11px;
  background:var(--paper); border:1px solid var(--rule); border-radius:4px;
  padding:1px 5px; margin:0 1px; color:var(--deep-sky);
}}

.status{{
  position:fixed; left:50%; bottom:30px; transform:translateX(-50%);
  display:flex; flex-direction:column; align-items:center; gap:9px;
  z-index:10; width:min(92vw,760px);
}}
.caption{{
  font-family:'Caveat',cursive; font-size:clamp(18px,2.6vw,25px); font-weight:600;
  color:var(--deep-sky); min-height:1.2em; text-align:center; line-height:1;
}}
.dots{{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;}}
.dot{{
  width:7px; height:7px; border-radius:50%; background:var(--rule);
  border:0; padding:0; cursor:pointer; transition:background .2s ease, transform .2s ease;
}}
.dot.on{{background:var(--orange);}}
.dot.cur{{transform:scale(1.5);background:var(--deep-sky);}}
.dot:focus-visible{{outline:2px solid var(--focus);outline-offset:2px;}}

.start{{
  position:fixed; inset:0; z-index:50;
  display:flex; align-items:center; justify-content:center; padding:24px;
  background:radial-gradient(120% 90% at 50% 0%, var(--page-bg-2) 0%, var(--page-bg) 62%);
  cursor:pointer; transition:opacity .5s ease, transform .55s ease;
}}
.start.go{{opacity:0;transform:scale(1.12);pointer-events:none;}}
.start-card{{
  text-align:center; background:var(--paper);
  border:1px solid var(--rule); border-radius:20px;
  padding:clamp(32px,5vw,52px) clamp(28px,6vw,64px);
  box-shadow:0 30px 70px -24px rgba(19,58,84,.4);
  max-width:min(440px, calc(100vw - 40px));
}}
.start-card .eyebrow{{justify-content:center;margin-bottom:16px;}}
.start-card h1{{
  font-family:'DM Serif Display',Georgia,serif; font-weight:400;
  font-size:clamp(30px,6vw,44px); line-height:1.05; margin:0;
  color:var(--ink); text-wrap:balance;
}}
.start-card h1 .scribble{{
  font-family:'Caveat',cursive; font-weight:700; color:var(--orange); font-size:1.15em;
}}
.start-card p{{margin:14px 0 0;font-size:13.5px;line-height:1.5;color:var(--grey);}}
.start-card .go-cue{{
  margin-top:22px; font-family:'Caveat',cursive;
  font-size:20px; font-weight:700; color:var(--deep-sky);
}}

@media (prefers-reduced-motion:reduce){{*{{transition:none !important;}}}}
@media (max-width:560px){{
  .hint{{display:none;}}
  .wrap{{padding:48px 12px 92px;}}
  .board{{width:min(calc(100vw - 24px), calc((100vh - 150px) * 1.6));}}
}}
</style>

<div class="wrap" id="wrap">
  <div class="board" id="board" role="group" aria-label="Talking With AI — click to reveal the conversation step by step">
  {pieces}
  </div>
</div>

<div class="topbar">
  <button class="btn" id="restart" type="button">↺ restart</button>
  <div class="eyebrow"><span class="bead"></span>Talking With AI</div>
  <div class="hint"><kbd>click</kbd> or <kbd>space</kbd> forward · <kbd>←</kbd> back</div>
</div>

<div class="status">
  <div class="caption" id="caption" aria-live="polite"></div>
  <div class="dots" id="dots"></div>
</div>

<div class="start" id="start">
  <div class="start-card">
    <div class="eyebrow"><span class="bead"></span>You steer it</div>
    <h1>Talking <span class="scribble">with</span> AI</h1>
    <p>How you talk to an AI shapes how it answers.</p>
    <div class="go-cue">click anywhere to begin →</div>
  </div>
</div>

<script>
(function(){{
  var NSTEPS = {nsteps};
  var CAPTIONS = {captions};
  var pieces = Array.prototype.slice.call(document.querySelectorAll('.piece[data-step]'));
  var board = document.getElementById('board');
  var startEl = document.getElementById('start');
  var captionEl = document.getElementById('caption');
  var dotsEl = document.getElementById('dots');
  var step = 0, started = false;

  for (var i = 1; i <= NSTEPS; i++) {{
    (function (n) {{
      var b = document.createElement('button');
      b.className = 'dot'; b.type = 'button';
      b.setAttribute('aria-label', 'Step ' + n + ': ' + CAPTIONS[n - 1]);
      b.addEventListener('click', function (e) {{ e.stopPropagation(); go(n); }});
      dotsEl.appendChild(b);
    }})(i);
  }}
  var dots = Array.prototype.slice.call(dotsEl.children);

  function render() {{
    pieces.forEach(function (p) {{
      p.classList.toggle('show', +p.getAttribute('data-step') <= step);
    }});
    dots.forEach(function (d, idx) {{
      d.classList.toggle('on', (idx + 1) <= step);
      d.classList.toggle('cur', (idx + 1) === step);
    }});
    captionEl.textContent = step > 0 ? CAPTIONS[step - 1] : '';
  }}
  function go(n) {{ step = Math.max(0, Math.min(NSTEPS, n)); render(); }}
  function next() {{ if (step < NSTEPS) go(step + 1); }}
  function prev() {{ if (step > 0) go(step - 1); }}

  function begin() {{
    if (started) return;
    started = true;
    startEl.classList.add('go');
    setTimeout(function () {{ startEl.style.display = 'none'; }}, 560);
    go(1);
  }}

  startEl.addEventListener('click', begin);
  board.addEventListener('click', function () {{ started ? next() : begin(); }});
  document.getElementById('wrap').addEventListener('click', function (e) {{
    if (e.target === e.currentTarget) started ? next() : begin();
  }});
  document.getElementById('restart').addEventListener('click', function (e) {{
    e.stopPropagation();
    step = 0; started = false;
    startEl.style.display = ''; startEl.classList.remove('go');
    render();
  }});
  document.addEventListener('keydown', function (e) {{
    if (e.key === ' ' || e.key === 'Spacebar' || e.key === 'ArrowRight') {{
      e.preventDefault(); started ? next() : begin();
    }} else if (e.key === 'ArrowLeft') {{
      e.preventDefault(); if (started) prev();
    }}
  }});

  render();
}})();
</script>
'''

if __name__ == "__main__":
    main()
