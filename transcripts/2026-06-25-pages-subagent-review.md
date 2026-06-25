# 2026-06-25 Pages subagent review loop

Goal: improve the public GitHub Pages display for the SUEWS Community
Hackathon practice repo using a builder/reviewer subagent loop.

Method: both builder and reviewer roles used `research-discussion-core` in each
loop to keep the page centered on the core reviewer question: whether the
corrected UDA-city index is a more faithful first-pass humid-heat risk
comparison than the supplied reference bridge, without overclaiming a final
city-risk model.

Loop summary:

1. Added a top `Reviewer answer` section with the core question, short answer,
   and claim boundary.
2. Added a plot-reading bridge so each comparison plot has an evidence role.
3. Moved setup and verification details below the results under
   `Reproducibility`.
4. Added a correction traceability table mapping each reference-bridge issue to
   the correction and evidence artifact.
5. Added stable Figure 1-4 labels and visible captions.
6. Compressed duplicate plot-reading bullets into one bridge sentence.
7. Regenerated Figure 3 with deterministic label offsets, white label backing,
   and callout lines.
8. Clarified the Figure 3 caption: `x = 0` with positive `y` means the old
   bridge shows no relative change while the corrected absolute index shows
   future risk increasing.
9. Reframed `Ideas not fixed yet` as a boundary/next-pass table.
10. Added an `At-a-glance evidence` table near the top with `Claim`,
    `Best evidence on this page`, and `Boundary`.

Final reviewer verdict: accept. No blocker remained. Remaining concerns were
non-blocking polish only: the page is table-heavy on narrow screens, and
`Files to inspect` still reads like a technical follow-up section, but both are
acceptable for the submission because the claim, evidence, and boundaries are
clear.

Verification after the loop:

- `python -m py_compile analysis/uda_city_true_data/generate_corrected_indices.py`
- Regenerated `docs/assets/uda_indices/scenario_delta_old_vs_corrected.png`
  from `analysis/uda_city_true_data/corrected_index_comparison.csv`.
- Checked all four `docs/assets/uda_indices/*.png` files for dimensions and
  nonblank pixel ranges.
- `PYTHONUTF8=1 python -m pytest data/uda-city-hackathon/tests -m "not slow"`
  passed: 8 passed, 1 deselected.
