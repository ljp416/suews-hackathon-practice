# SUEWS Hackathon UDA-city Practice

This repository has been updated from the SUEWS hackathon template and now uses
the released UDA-city dataset.

Dataset: [UMEP-dev/uda-city-hackathon](https://github.com/UMEP-dev/uda-city-hackathon)

## What was updated

- Template notes were refreshed from `UMEP-dev/suews-hackathon-template`.
- The released UDA-city data pack was added under `data/uda-city-hackathon/`.
- The agent manifest was read from `data/uda-city-hackathon/agent_manifest.yml`.
- The canonical 10-neighbourhood config `uda-city.yml` was validated.
- Present and future reference risk tables were generated with `risk_bridge.py`.

## Verification

- `suews validate --dry-run --format json data/uda-city-hackathon/uda-city.yml`
  returned `is_valid: true` and `error_count: 0`.
- The dataset smoke test passed for 10 neighbourhoods over 2,016 steps.
- Present and future risk-bridge runs completed.
- Dataset non-slow tests passed: 8 passed, 1 slow test deselected.

On this Windows host, Python commands that read the UTF-8 YAML need
`PYTHONUTF8=1`.

## Reference result

The supplied bridge uses dangerous-heat hours from SUEWS, daytime population as
exposure, and synthetic vulnerability proxies. It is a reference bridge, not a
final scientific answer.

| Future rank | Neighbourhood | Type | Present hours | Future hours | Delta hours | Present risk | Future risk |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Kampong Lama | hotspot | 42 | 249 | 207 | 1.000 | 1.000 |
| 2 | Fuzhou Lanes | hotspot | 22 | 212 | 190 | 0.800 | 0.930 |
| 3 | Dhobi Lines | hotspot | 26 | 217 | 191 | 0.833 | 0.923 |
| 4 | Mlima Moto | hotspot | 5 | 149 | 144 | 0.429 | 0.761 |
| 5 | Lusitano Square | core | 5 | 129 | 124 | 0.176 | 0.280 |
| 6 | Victoria Exchange | core | 5 | 120 | 115 | 0.151 | 0.225 |

`Jade Gardens` has the highest dangerous-heat hours in both present and future
runs, but it does not rank highest under the reference risk bridge because the
exposure pillar is low. This is the main hazard-versus-risk tension to explain.

## Caveats

- UDA-city is synthetic, not a real place.
- The default threshold is dry-bulb `T2 > 35 C`; a humid-heat metric may be more
  defensible and should be justified if used.
- The socio-economic layer is synthetic, so ranks are more meaningful than
  absolute index values.
- The future forcing is a +2.5 C pseudo-warming scenario, not a downscaled
  climate projection.

## Files to inspect

- `data/uda-city-hackathon/agent_manifest.yml`
- `data/uda-city-hackathon/risk_bridge.md`
- `analysis/uda_city_true_data/README.md`
- `analysis/uda_city_true_data/risk_present.csv`
- `analysis/uda_city_true_data/risk_future.csv`
- `analysis/uda_city_true_data/risk_present_future_comparison.csv`
