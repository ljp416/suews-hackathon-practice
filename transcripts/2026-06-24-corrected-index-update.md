# Corrected Index Update Transcript

Date: 2026-06-24

Repository: https://github.com/ljp416/suews-hackathon-practice

Pages URL: https://ljp416.github.io/suews-hackathon-practice/

## User Request

Fix the first four disalignments in the current UDA-city risk index, draw
comparison plots between old and new indices, show them on Pages, and list the
remaining critique items as future ideas.

## Core framing

The reference bridge is useful as a teaching baseline because it shows
hazard-risk disagreement, but it over-penalizes low-population areas, makes
zeros too destructive, rescales each scenario separately, and underuses the
hot-humid context.

## Implementation

Added:

- `analysis/uda_city_true_data/generate_corrected_indices.py`
- `analysis/uda_city_true_data/corrected_hazard_metrics.csv`
- `analysis/uda_city_true_data/corrected_index_long.csv`
- `analysis/uda_city_true_data/corrected_index_comparison.csv`
- `docs/assets/uda_indices/old_vs_corrected_risk.png`
- `docs/assets/uda_indices/dry_vs_humid_heat_hours.png`
- `docs/assets/uda_indices/scenario_delta_old_vs_corrected.png`
- `docs/assets/uda_indices/exposure_floor_effect.png`

Corrected index:

```text
humid hazard = hours(heat index > 41 C) / analysis hours
exposure = daytime population / maximum daytime population
vulnerability = raw mean of the five supplied vulnerability proxies
social sensitivity = mean(exposure, vulnerability)
corrected risk = humid hazard * social sensitivity
```

## Commands

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python analysis\uda_city_true_data\generate_corrected_indices.py
.\.venv\Scripts\python -m pytest data\uda-city-hackathon\tests -m "not slow"
```

## Verification

- Corrected-index generator reran present and future SUEWS scenarios.
- Dataset tests passed: 8 passed, 1 slow test deselected.
- Four PNG plots were checked for expected dimensions and nonblank pixels.
- Page image references point at existing files under `docs/assets/uda_indices/`.
- Portable-path scan found no local absolute paths in candidate files.

## Result

- `Jade Gardens` no longer has zero risk: corrected risk is `0.062` present and
  `0.209` future.
- `Kampong Lama` remains top risk, but corrected risk now shows absolute
  worsening: `0.169 -> 0.569`.
- Humid heat makes the hazard much larger: `Kampong Lama` has `42` dry-bulb
  hours but `414` humid-heat hours in the present scenario.
