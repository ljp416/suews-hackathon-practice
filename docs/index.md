# SUEWS Hackathon UDA-city Practice

This repository uses the released UDA-city dataset and compares the supplied
reference risk bridge against a corrected index that addresses four specific
alignment problems.

Dataset: [UMEP-dev/uda-city-hackathon](https://github.com/UMEP-dev/uda-city-hackathon)

## What was updated

- Template notes were refreshed from `UMEP-dev/suews-hackathon-template`.
- The released UDA-city data pack was added under `data/uda-city-hackathon/`.
- Present and future SUEWS runs were completed for all 10 neighbourhoods.
- The supplied reference bridge was run for present and future.
- A corrected humid-heat risk index was generated with comparison plots.

## Verification

- `suews validate --dry-run --format json data/uda-city-hackathon/uda-city.yml`
  returned `is_valid: true` and `error_count: 0`.
- Dataset smoke test passed for 10 neighbourhoods over 2,016 steps.
- Dataset non-slow tests passed: 8 passed, 1 slow test deselected.
- Corrected-index generator reran present and future SUEWS scenarios and wrote
  CSVs plus PNG plots under `analysis/uda_city_true_data/` and
  `docs/assets/uda_indices/`.

On this Windows host, Python commands that read the UTF-8 YAML need
`PYTHONUTF8=1`.

## Why the reference index is misaligned

The supplied bridge is useful because it shows that hazard and risk can disagree,
but its default scaling creates artifacts:

- The lowest daytime population, 80 people/ha, becomes exposure `0`.
- The geometric mean then turns any zero pillar into total risk `0`.
- Present and future are min-max scaled separately, so a score of `1.0` in both
  scenarios does not mean unchanged absolute risk.
- The hazard is dry-bulb `T2 > 35 C`, even though UDA-city is hot-humid with mean
  RH near 83%.

## Corrected index

This page uses a deliberately simple corrected index:

```text
humid hazard = hours(heat index > 41 C) / analysis hours
exposure = daytime population / maximum daytime population
vulnerability = raw mean of the five supplied vulnerability proxies
social sensitivity = mean(exposure, vulnerability)
corrected risk = humid hazard * social sensitivity
```

This fixes the four main issues without pretending to be the final answer:

- low exposure remains low, not zero;
- one low social pillar does not erase all risk;
- present and future scores share the same absolute scale;
- humidity enters the hazard through heat-index hours.

## New result

| Future rank | Neighbourhood | Type | Humid hours present | Humid hours future | Delta humid hours | Corrected risk present | Corrected risk future |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Kampong Lama | hotspot | 414 | 1391 | 977 | 0.169 | 0.569 |
| 2 | Dhobi Lines | hotspot | 387 | 1368 | 981 | 0.157 | 0.555 |
| 3 | Fuzhou Lanes | hotspot | 369 | 1340 | 971 | 0.152 | 0.551 |
| 4 | Mlima Moto | hotspot | 317 | 1314 | 997 | 0.131 | 0.544 |
| 5 | Lusitano Square | core | 297 | 1310 | 1013 | 0.083 | 0.367 |
| 6 | Victoria Exchange | core | 288 | 1299 | 1011 | 0.080 | 0.360 |
| 7 | Zheng He Towers | core | 232 | 1281 | 1049 | 0.063 | 0.348 |
| 8 | Taman Melati | refuge | 398 | 1374 | 976 | 0.061 | 0.211 |
| 9 | Jade Gardens | refuge | 413 | 1392 | 979 | 0.062 | 0.209 |
| 10 | Serendib Rise | refuge | 377 | 1347 | 970 | 0.055 | 0.195 |

The headline changes are:

- `Jade Gardens` no longer disappears. Its reference risk was `0`; corrected
  risk is `0.062` present and `0.209` future.
- `Kampong Lama` remains the top risk neighbourhood, but corrected risk now
  shows absolute worsening: `0.169 -> 0.569`.
- Humid-heat hours are much larger than dry-bulb hours. For `Kampong Lama`,
  present hazard is `42` dry-bulb hours but `414` humid-heat hours.

## Comparison plots

![Old relative risk compared with corrected absolute humid-heat risk](assets/uda_indices/old_vs_corrected_risk.png)

![Dry-bulb hazard compared with humid-heat hazard](assets/uda_indices/dry_vs_humid_heat_hours.png)

![Future-minus-present risk change under old and corrected indices](assets/uda_indices/scenario_delta_old_vs_corrected.png)

![Reference exposure scaling compared with corrected population divided by maximum](assets/uda_indices/exposure_floor_effect.png)

## Ideas not fixed yet

The corrected index only fixes the first four alignment problems. These remain
as next design ideas:

- Replace daytime population with time-varying exposure: night population,
  worker schedules, school hours, indoor/outdoor time, and mobility.
- Enrich vulnerability: housing quality, health status, cooling centres, water
  access, informal work timing, social support, and medical access.
- Move below neighbourhood averages so vulnerable subgroups inside lower-risk
  areas do not disappear.
- Add future social scenarios instead of changing climate only: population,
  AC access, deprivation, age structure, outdoor work, and adaptive capacity.

## Files to inspect

- `analysis/uda_city_true_data/generate_corrected_indices.py`
- `analysis/uda_city_true_data/corrected_index_comparison.csv`
- `analysis/uda_city_true_data/corrected_index_long.csv`
- `analysis/uda_city_true_data/corrected_hazard_metrics.csv`
- `data/uda-city-hackathon/risk_bridge.md`
