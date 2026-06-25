# 2026-06-25 Pages visual polish loop

Goal: run five additional builder/reviewer loops focused on the public GitHub
Pages display. The aim was to make the page more visually appealing and make
the data support the narrative more directly.

Reference guidance used:

- Nielsen Norman Group visual hierarchy guidance: use contrast, scale, and
  grouping to guide attention.
- Datawrapper annotation guidance: keep explanatory text close to the data,
  especially on smaller screens.
- Datawrapper typography guidance: use readable sans-serif text, high contrast,
  and uppercase sparingly.

Loop summary:

1. Added a CSS layer and a stronger top fold: reviewer answer band, boundary
   aside, metric cards, and evidence-path navigation.
2. Added figure-adjacent key-number callouts for Figures 1-3 so the plots carry
   exact narrative anchors beside the data.
3. Converted Figure 4 to the same callout pattern and verified the exposure
   anchor: reference exposure `0` becomes corrected exposure `0.267`
   (`80 / 300` daytime population).
4. Replaced repeated middle-page prose/tables with a compact `Four tested
   fixes` ladder mapping `problem -> correction -> figure -> key number`.
5. Added stable figure anchors and clickable Figure 1-4 references so the fix
   ladder also works as reviewer navigation.

Final reviewer verdict: accept. No blockers remained. The remaining concern was
minor repetition between metric cards and fix cards, accepted because it improves
scan speed on a public Pages submission.

Verification after the loop:

- Checked required links, anchors, and PNG asset paths in `docs/index.md`.
- `python -m py_compile analysis/uda_city_true_data/generate_corrected_indices.py`
- `PYTHONUTF8=1 python -m pytest data/uda-city-hackathon/tests -m "not slow"`
  passed: 8 passed, 1 deselected.
- `git diff --check` passed.
- Checked changed page/CSS diff for portable-path leaks.
