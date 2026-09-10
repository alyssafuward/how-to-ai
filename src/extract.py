"""
Extract flattened, canvas-aligned PNG pieces from the hand-drawn PSDs.

Every layer in the source PSDs is already separated (each line segment, each
callout, each character on its own layer), so this just walks the layer tree
and composites the pieces we want onto the full 2400x1500 canvas, then crops
each to its content bbox and records the offset in a manifest.

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
        21: "auntlike", 22: "camping", 23: "cabin", 24: "driving",
        25: "newnotexp", 26: "letmesee",
    }
    for li, nm in callouts.items():
        save_cropped(canvas_composite(layers[li], (W, H)), out, f"callout_{nm}", manifest)

    json.dump({"canvas": [W, H], "assets": manifest},
              open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(f"panel1: {len(manifest)} pieces -> {out}")


if __name__ == "__main__":
    extract_panel1()
