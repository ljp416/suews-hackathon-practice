# UDA-city True-data Run

Status: completed

Dataset: `data/uda-city-hackathon` from `UMEP-dev/uda-city-hackathon`

Dataset commit pulled: `0df6835c5832fb0ec78094d6acd09a45a953826b`

Runtime:

- `supy`: 2026.6.5
- `suews_mcp`: 2026.6.5
- Windows note: commands that read UTF-8 YAML need `PYTHONUTF8=1` on this host.

## What was run

The released UDA-city pack was added under `data/uda-city-hackathon/`.
The agent entry point is `data/uda-city-hackathon/agent_manifest.yml`.
The canonical SUEWS configuration is `data/uda-city-hackathon/uda-city.yml`.

Validation:

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\suews validate --dry-run --format json data\uda-city-hackathon\uda-city.yml
```

Result: `is_valid: true`, `error_count: 0`.

Smoke test:

```powershell
$env:PYTHONUTF8 = "1"
..\..\.venv\Scripts\python scripts\smoke_test.py
```

Result: `OK: 10 site(s) x 2,016 steps (7 days) under supy 2026.6.5; NARP+OHM on disk; T2 26.2..38.9 C; config: uda-city.yml.`

Reference bridge runs:

```powershell
$env:PYTHONUTF8 = "1"
..\..\.venv\Scripts\python risk_bridge.py --out outputs\derived\risk_present.csv
..\..\.venv\Scripts\python risk_bridge.py --forcing forcing\future_hot_humid\UDA_2024_data_60.txt --out outputs\derived\risk_future.csv
```

Generated output tables from `risk_bridge.py` were written under the dataset's
ignored `outputs/derived/` folder, then copied here as tracked evidence:

- `analysis/uda_city_true_data/risk_present.csv`
- `analysis/uda_city_true_data/risk_future.csv`
- `analysis/uda_city_true_data/risk_present_future_comparison.csv`

Test gate:

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python -m pytest data\uda-city-hackathon\tests -m "not slow"
```

Result: 8 passed, 1 slow test deselected.

## Main result

The reference bridge ranks `Kampong Lama` first in both present and future
scenarios. `Jade Gardens` has the highest dangerous-heat hours in both scenarios
but low reference risk, because the bridge's exposure pillar is min-max scaled
from daytime population and this neighbourhood has the lowest exposure group.

| Future rank | Neighbourhood | Type | Present hours | Future hours | Delta hours | Present risk | Future risk |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Kampong Lama | hotspot | 42 | 249 | 207 | 1.000 | 1.000 |
| 2 | Fuzhou Lanes | hotspot | 22 | 212 | 190 | 0.800 | 0.930 |
| 3 | Dhobi Lines | hotspot | 26 | 217 | 191 | 0.833 | 0.923 |
| 4 | Mlima Moto | hotspot | 5 | 149 | 144 | 0.429 | 0.761 |
| 5 | Lusitano Square | core | 5 | 129 | 124 | 0.176 | 0.280 |
| 6 | Victoria Exchange | core | 5 | 120 | 115 | 0.151 | 0.225 |

## Boundary

This is a reference run with the supplied bridge, not the final judged argument.
The threshold is the default dry-bulb `T2 > 35 C`, the socio-economic layer is
synthetic, and the future forcing is a controlled +2.5 C pseudo-warming rather
than a downscaled climate projection.
