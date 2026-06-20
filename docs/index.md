# SUEWS Hackathon Practice Setup

This is a practice repository for the SUEWS Community Hackathon setup workflow.
It is not the judged 24 June submission and it does not analyse the focus city.

## What was checked

- A public GitHub repository was created from `UMEP-dev/suews-hackathon-template`.
- The task brief was read locally from `TASK_BRIEF.md`.
- The suews-agent runtime was installed from
  `git+https://github.com/UMEP-dev/SUEWS.git#subdirectory=mcp`.
- A small bundled `simple-urban` SUEWS demo case ran end to end under
  `analysis/suews_smoke/`.
- GitHub Pages was enabled from the `main` branch and `/docs` folder.

## Smoke-run boundary

The smoke run used the bundled KCL/London sample configuration and forcing.
That makes it useful as a toolchain check only. It should not be interpreted as
heat-hazard evidence for the hackathon focus city.

Validation passed with zero errors, the model run completed, and the summary
reported no missing values for `T2`, `QH`, `QE`, `QN`, `Rain`, `Evap`, or `RO`.
Diagnostics returned warnings, including an energy-balance residual warning, so
the result remains a demo rather than a scientific conclusion.

## Next on hackathon day

Replace the sample case with the revealed city dataset and heat-to-risk bridge,
then build the final public story around the city-specific hazard layer, the
socio-economic risk indicator, and the limits of the bridge.
