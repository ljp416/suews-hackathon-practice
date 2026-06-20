# SUEWS Smoke Run

Status: completed

Readiness: Level 1 - demo

This practice run confirms that the suews-agent runtime can create, validate,
run, diagnose, and summarise a small SUEWS case in this repository.

## Case

- Template: `simple-urban`
- Site: bundled KCL/London sample
- Config: `analysis/suews_smoke/sample_config.yml`
- Forcing: `analysis/suews_smoke/Kc_2012_data_60.txt`
- Output directory: `analysis/suews_smoke/Output/`

This is not a focus-city analysis. It uses sample data only, so it should be
treated as a toolchain smoke test.

## Verification

- `suews init` created the sample config and forcing file.
- `suews inspect --format json` read the sample config successfully.
- `suews validate --dry-run --format json` returned `is_valid: true` with
  `error_count: 0`.
- `suews run` completed and wrote:
  - `Output/KCL1_2012_SUEWS_60.txt`
  - `Output/KCL_SUEWS_checkpoint.json`
- `suews summarise` reported `nan_pct: 0.0` for `T2`, `QH`, `QE`, `QN`,
  `Rain`, `Evap`, and `RO`.

Diagnostics returned warnings, not failures:

- `provenance.json` was missing during the first diagnostic pass; this sidecar
  has now been added manually for this practice repository.
- Mean energy-balance closure residual was reported as `5.731`, so this run is
  evidence that the workflow executes, not evidence for scientific conclusions.

## Summary Values

| Variable | Mean | Min | Max | NaN pct |
| --- | ---: | ---: | ---: | ---: |
| T2 | 11.9145 | -5.2429 | 30.4038 | 0.0 |
| QH | 88.7596 | -40.8153 | 339.7017 | 0.0 |
| QE | 27.5850 | 1.6983 | 195.3424 | 0.0 |
| QN | 44.7600 | -83.7954 | 646.9792 | 0.0 |
| Rain | 0.0935 | 0.0 | 17.2 | 0.0 |
| Evap | 0.0401 | 0.0024 | 0.2845 | 0.0 |
| RO | 0.0653 | 0.0 | 14.0567 | 0.0 |
