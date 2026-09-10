# how-to-ai

Hand-drawn, click-through panels explaining how working with AI actually works.
Each panel is built from one of Alyssa Fu Ward's illustrations (a layered PSD),
sliced into pieces and revealed one click at a time.

## Layout

- `index.html` — the built, self-contained page (all art embedded as data URIs)
- `assets/panelN/` — the extracted PNG pieces + a `manifest.json` of canvas offsets
- `src/psd/` — the source illustrations
- `src/extract.py` — PSD → PNG pieces
- `src/build.py` — pieces → `index.html`
- `history/` — a local git-backed viewer for browsing past commits (see below)

## Build

    python3 src/extract.py    # regenerate assets/ from the PSDs
    python3 src/build.py       # regenerate index.html

## Browsing the history locally

    python3 history/serve.py

Opens a local server that serves `index.html` with a small history control:
pick any past commit and see the page exactly as it was then. Git-backed, never
ships in the published page.
