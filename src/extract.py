"""
Extract flattened, canvas-aligned PNG pieces from the hand-drawn PSDs.

Every layer in the source PSDs is already separated (each line segment, each
callout, each character on its own layer), so this just walks the layer tree
and composites the pieces we want onto the full 2400x1500 canvas, then crops
each to its content bbox and records the offset in a manifest.

The PSDs are not in the repo (large, and the rendered art is already checked
in). Drop them in src/psd/ locally before running this.

    python3 src/extract.py

Requires: psd-tools, Pillow.
"""
import json
import os

from PIL import Image
from psd_tools import PSDImage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSD_DIR = os.path.join(ROOT, "src", "psd")


def canvas_composite(layer, size):
    """Composite one layer/group onto a transparent full-canvas image."""
    W, H = size
    img = layer.composite(viewport=(0, 0, W, H), force=True)
    if img is None:
        return Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return img.convert("RGBA")


def group_composite(group, size):
    """Composite a group honouring its children's own visibility flags."""
    W, H = size
    img = group.composite(viewport=(0, 0, W, H))
    if img is None:
        return Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return img.convert("RGBA")


def save_cropped(img, out_dir, name, manifest):
    bbox = img.getbbox()
    if bbox is None:
        print("  (empty)", name)
        return
    crop = img.crop(bbox)
    path = os.path.join(out_dir, name + ".png")
    crop.save(path)
    manifest.append(
        {
            "name": name,
            "x": bbox[0],
            "y": bbox[1],
            "w": crop.width,
            "h": crop.height,
        }
    )


# --------------------------------------------------------------------------
# Panel 1 — "Talking with AI"
# The conversation path is two flattened polylines whose every segment is its
# own sub-layer, plus one grouped layer per callout, plus the two characters.
# --------------------------------------------------------------------------
def extract_panel1():
    psd = PSDImage.open(os.path.join(PSD_DIR, "talking-with-ai.psd"))
    W, H = psd.size
    out = os.path.join(ROOT, "assets", "panel1")
    os.makedirs(out, exist_ok=True)
    layers = list(psd)
    manifest = []

    def child(group_idx, kids):
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        g = list(layers[group_idx])
        for k in kids:
            im = g[k].composite(viewport=(0, 0, W, H), force=True)
            if im is not None:
                base.alpha_composite(im.convert("RGBA"))
        return base

    save_cropped(canvas_composite(layers[5], (W, H)), out, "credit", manifest)
    save_cropped(canvas_composite(layers[29], (W, H)), out, "title", manifest)
    save_cropped(canvas_composite(layers[11], (W, H)), out, "char_bubble", manifest)
    save_cropped(child(12, [0]), out, "robot", manifest)
    save_cropped(child(12, [2, 3]), out, "callout_caribbean", manifest)

    # top line: group 9, children run back-to-front, so reverse into path order
    for k, ci in enumerate([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], start=1):
        save_cropped(child(9, [ci]), out, f"top_s{k:02d}", manifest)
    # bottom (camping) branch: group 8
    for k, ci in enumerate([5, 4, 3, 2, 1, 0], start=1):
        save_cropped(child(8, [ci]), out, f"bot_s{k:02d}", manifest)

    callouts = {
        13: "twokids", 14: "disneyland", 15: "lowkey", 16: "tellmemore",
        17: "september", 18: "october", 19: "hotels", 20: "auntgift",
        21: "auntlike", 22: "camping", 23: "cabin", 24: "youhatebugs",
        25: "bugspray", 26: "letmesee",
    }
    for li, nm in callouts.items():
        save_cropped(canvas_composite(layers[li], (W, H)), out, f"callout_{nm}", manifest)

    json.dump({"canvas": [W, H], "assets": manifest},
              open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(f"panel1: {len(manifest)} pieces -> {out}")


# --------------------------------------------------------------------------
# Panel 2 — "What is the AI doing?"
# A human -> box -> output diagram. The box has two versions of its contents:
# a giant AI robot (shown while the flow is drawn) and, at the end, a tangle
# of scribbles with a small robot (what the AI is "really" doing).
# --------------------------------------------------------------------------
def extract_panel2():
    import numpy as np

    psd = PSDImage.open(os.path.join(PSD_DIR, "what-is-the-ai-doing.psd"))
    W, H = psd.size
    out = os.path.join(ROOT, "assets", "panel2")
    os.makedirs(out, exist_ok=True)
    layers = list(psd)
    manifest = []

    save_cropped(group_composite(layers[4], (W, H)), out, "credit", manifest)
    save_cropped(group_composite(layers[18], (W, H)), out, "char_bubble", manifest)
    save_cropped(group_composite(layers[19], (W, H)), out, "title", manifest)
    save_cropped(group_composite(layers[14], (W, H)), out, "box", manifest)
    save_cropped(canvas_composite(layers[13], (W, H)), out, "giant_ai", manifest)
    save_cropped(group_composite(layers[8], (W, H)), out, "squiggle", manifest)
    # the little robot sitting in the scribble tangle, isolated — it stays on
    # screen (unlike the scribbles) once the flow diagram replaces the tangle
    robot = list(layers[8])[3].composite(viewport=(0, 0, W, H), force=True)
    save_cropped(robot.convert("RGBA") if robot else Image.new("RGBA", (W, H), (0, 0, 0, 0)),
                 out, "box_robot", manifest)
    save_cropped(group_composite(layers[12], (W, H)), out, "output", manifest)

    # layer 15 holds both arrow curves in one sub-layer; split at the middle
    # of the box (nothing crosses there) and fold in the two arrowheads.
    arrows = list(layers[15])
    both = canvas_composite(arrows[0], (W, H))
    head_in = canvas_composite(arrows[1], (W, H))
    head_out = canvas_composite(arrows[2], (W, H))

    def clip_x(img, lo, hi):
        a = np.array(img)
        a[:, :lo, 3] = 0
        a[:, hi:, 3] = 0
        return Image.fromarray(a)

    save_cropped(Image.alpha_composite(clip_x(both.copy(), 0, 1150), head_in),
                 out, "arrow_in", manifest)
    save_cropped(Image.alpha_composite(clip_x(both.copy(), 1150, W), head_out),
                 out, "arrow_out", manifest)

    json.dump({"canvas": [W, H], "assets": manifest},
              open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(f"panel2: {len(manifest)} pieces -> {out}")


# --------------------------------------------------------------------------
# Panel 2 continued — the "flow diagram" reveal
# One click after the scribble tangle, it resolves into the actual steps
# (reads -> interprets -> tools/access/guardrails feed into -> takes action
# -> back out), plus a fresh exit arrow (the old one pointed at the tangle's
# exit point, not "Takes Action"'s) and the "one step at a time" tagline.
# Every layer here is already a single, complete, individually-meaningful
# piece — no per-segment puzzle to solve this time.
# --------------------------------------------------------------------------
def extract_panel2_flow():
    psd = PSDImage.open(os.path.join(PSD_DIR, "what-is-the-ai-doing-flow.psd"))
    W, H = psd.size
    out = os.path.join(ROOT, "assets", "panel2")
    os.makedirs(out, exist_ok=True)
    layers = list(psd)
    manifest = []

    pieces = {
        1: "tagline", 2: "guardrails", 3: "access", 4: "tools",
        5: "arrow_takesaction_out", 6: "takes_action", 7: "interprets",
        8: "reads",
    }
    for li, nm in pieces.items():
        save_cropped(canvas_composite(layers[li], (W, H)), out, nm, manifest)

    # merge into the existing panel2 manifest rather than overwrite it
    man_path = os.path.join(out, "manifest.json")
    existing = json.load(open(man_path))
    names = {a["name"] for a in manifest}
    existing["assets"] = [a for a in existing["assets"] if a["name"] not in names] + manifest
    json.dump(existing, open(man_path, "w"), indent=1)
    print(f"panel2 (flow): {len(manifest)} pieces -> {out}")


# --------------------------------------------------------------------------
# Panel 2 continued — "It's like magic..."
# A one-off caption Alyssa added under the scribble-tangle box (the same
# spot the flow-diagram's tagline occupies one click later).
# --------------------------------------------------------------------------
def extract_panel2_magic():
    psd = PSDImage.open(os.path.join(PSD_DIR, "what-is-the-ai-doing-magic.psd"))
    W, H = psd.size
    out = os.path.join(ROOT, "assets", "panel2")
    os.makedirs(out, exist_ok=True)
    layers = list(psd)
    manifest = []

    save_cropped(canvas_composite(layers[20], (W, H)), out, "magic", manifest)

    man_path = os.path.join(out, "manifest.json")
    existing = json.load(open(man_path))
    names = {a["name"] for a in manifest}
    existing["assets"] = [a for a in existing["assets"] if a["name"] not in names] + manifest
    json.dump(existing, open(man_path, "w"), indent=1)
    print(f"panel2 (magic): {len(manifest)} pieces -> {out}")


# --------------------------------------------------------------------------
# Panel 3 — "Deterministic vs Probabilistic"
# Same "calculate 2+5" instruction, sent to a calculator-style deterministic
# process and an LLM-style probabilistic one. Every top-level layer here is
# either a complete, individually-meaningful group or a small standalone
# label/character layer — nothing needs splitting or merging by hand.
# --------------------------------------------------------------------------
def extract_panel3():
    psd = PSDImage.open(os.path.join(PSD_DIR, "deterministic-vs-probabilistic.psd"))
    W, H = psd.size
    out = os.path.join(ROOT, "assets", "panel3")
    os.makedirs(out, exist_ok=True)
    layers = list(psd)
    manifest = []

    pieces = {
        1: "label_probabilistic",
        2: "prob_returns_most",
        3: "prob_returns",
        4: "prob_guess",
        5: "prob_pattern",
        6: "prob_reads",
        7: "prob_frame",
        8: "label_deterministic",
        9: "det_returns",
        10: "det_ai_reads",
        11: "det_calc_returns",
        12: "det_inputs",
        13: "det_opens",
        14: "det_reads",
        15: "det_output_frame",
        16: "det_frame",
        17: "char_bubble",
        18: "credit",
    }
    for li, nm in pieces.items():
        save_cropped(canvas_composite(layers[li], (W, H)), out, nm, manifest)

    json.dump({"canvas": [W, H], "assets": manifest},
              open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(f"panel3: {len(manifest)} pieces -> {out}")


# --------------------------------------------------------------------------
# Panel 3 continued — guardrails and checks
# After the deterministic-vs-probabilistic comparison plays out and the
# closing image shows once (mid-panel this time, not a terminal outro), the
# probabilistic box resets to its skeleton (frame + reads + returns, no
# middle content, no label — a full redraw supplied as one base layer) and
# rebuilds with guardrails feeding into it: constrain answers, have the AI
# check its own answer, have a human check it, then returns with higher
# confidence.
# --------------------------------------------------------------------------
def extract_panel3_guardrails():
    psd = PSDImage.open(os.path.join(PSD_DIR, "deterministic-vs-probabilistic-guardrails.psd"))
    W, H = psd.size
    out = os.path.join(ROOT, "assets", "panel3")
    os.makedirs(out, exist_ok=True)
    layers = list(psd)
    manifest = []

    pieces = {
        2: "label_probdeterm",
        3: "confidence_note",
        4: "constrain",
        5: "ai_checks",
        6: "human_checks",
        7: "pattern_guess",
        8: "base_reset",
    }
    for li, nm in pieces.items():
        save_cropped(canvas_composite(layers[li], (W, H)), out, nm, manifest)

    man_path = os.path.join(out, "manifest.json")
    existing = json.load(open(man_path))
    names = {a["name"] for a in manifest}
    existing["assets"] = [a for a in existing["assets"] if a["name"] not in names] + manifest
    json.dump(existing, open(man_path, "w"), indent=1)
    print(f"panel3 (guardrails): {len(manifest)} pieces -> {out}")


# --------------------------------------------------------------------------
# Panel 4 — "What is the AI doing?" (multi-agent)
# A second take on the same question: instead of one AI, a kitchen brigade
# of agents (planner, orchestrator, two workers, evaluator, reporter). The
# base layer is the frame/title/human/output with no agents in it yet; each
# agent is its own complete group, arrow included.
# --------------------------------------------------------------------------
def extract_panel4():
    psd = PSDImage.open(os.path.join(PSD_DIR, "what-is-the-ai-doing-multiagent.psd"))
    W, H = psd.size
    out = os.path.join(ROOT, "assets", "panel4")
    os.makedirs(out, exist_ok=True)
    layers = list(psd)
    manifest = []

    pieces = {
        3: "credit",
        6: "tagline",
        7: "server_exit_arrow",
        8: "agent_server",
        9: "agent_sous_chef",
        10: "agent_pastry_chef",
        11: "agent_grill_cook",
        12: "agent_expediter",
        13: "agent_head_chef",
        14: "base",
    }
    for li, nm in pieces.items():
        save_cropped(canvas_composite(layers[li], (W, H)), out, nm, manifest)

    json.dump({"canvas": [W, H], "assets": manifest},
              open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(f"panel4: {len(manifest)} pieces -> {out}")


if __name__ == "__main__":
    extract_panel1()
    extract_panel2()
    extract_panel2_flow()
    extract_panel2_magic()
    extract_panel3()
    extract_panel3_guardrails()
    extract_panel4()
