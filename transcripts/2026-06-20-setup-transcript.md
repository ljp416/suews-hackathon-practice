# SUEWS Hackathon Practice Setup Transcript

Date: 2026-06-20

Repository: https://github.com/ljp416/suews-hackathon-practice

Pages URL: https://ljp416.github.io/suews-hackathon-practice/

This transcript records the setup workflow performed by Codex for the SUEWS
Community Hackathon practice repository. Raw GitHub authentication output is
not included.

## User Request

Set up a public practice repository from `UMEP-dev/suews-hackathon-template`,
read the task brief, run a small SUEWS simulation through the suews-agent
runtime, publish `docs/` with GitHub Pages, save this transcript, then commit
and push.

## Step 1 - Repository Creation

- Verified GitHub CLI was available: `gh version 2.86.0`.
- Verified the active GitHub account was `ljp416`.
- Confirmed `ljp416/suews-hackathon-practice` did not already exist.
- Ran:

```powershell
gh repo create ljp416/suews-hackathon-practice --template UMEP-dev/suews-hackathon-template --public --clone
```

- Result: repository created and cloned into the local SUEWS workspace.
- Remote verified as `https://github.com/ljp416/suews-hackathon-practice.git`.

## Step 2 - Task Brief

- Read `TASK_BRIEF.md`.
- Key point: the practice repository is a setup and pipeline check. The judged
  hackathon entry is created on 24 June under `UMEP-dev` after the focus-city
  dataset and heat-to-risk bridge are released.

## Step 3 - SUEWS Smoke Run

The live suews-agent MCP tool was not exposed directly in this Codex session,
so the run used the suews-agent runtime path from the local plugin instructions:
install `suews-mcp` from the `UMEP-dev/SUEWS` `mcp` subdirectory, then run the
unified `suews` CLI.

Runtime setup:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install "git+https://github.com/UMEP-dev/SUEWS.git#subdirectory=mcp"
```

Verification:

```powershell
.\.venv\Scripts\python -c "import supy, suews_mcp; print(supy.__version__); print(suews_mcp.__version__)"
.\.venv\Scripts\suews --help
.\.venv\Scripts\suews-mcp --help
```

- `supy`: `2026.6.5`
- `suews_mcp`: `2026.6.5`
- `suews` and `suews-mcp` commands were available.

Case creation and validation:

```powershell
.\.venv\Scripts\suews init analysis\suews_smoke --template simple-urban --format json
.\.venv\Scripts\suews inspect --format json analysis\suews_smoke\sample_config.yml
.\.venv\Scripts\suews validate --dry-run --format json analysis\suews_smoke\sample_config.yml
```

- `suews init` created `sample_config.yml` and `Kc_2012_data_60.txt`.
- `suews validate` returned `is_valid: true` and `error_count: 0`.
- The case is the bundled KCL/London sample, so readiness is Level 1 - demo.

Run:

```powershell
.\.venv\Scripts\suews run analysis\suews_smoke\sample_config.yml
```

- Effective simulation period: 2012-01-01 00:05 to 2013-01-01 00:00.
- Output files:
  - `analysis/suews_smoke/Output/KCL1_2012_SUEWS_60.txt`
  - `analysis/suews_smoke/Output/KCL_SUEWS_checkpoint.json`

Post-run checks:

```powershell
.\.venv\Scripts\suews diagnose --format json analysis\suews_smoke\Output
.\.venv\Scripts\suews summarise analysis\suews_smoke\Output --variables T2,QH,QE,QN,Rain,Evap,RO --format json
```

- After adding `Output/provenance.json`, diagnostics had 3 passes, 1 warning,
  and 0 failures.
- Remaining diagnostic warning: mean energy-balance closure residual `5.731`
  exceeded the diagnostic threshold.
- Summary reported `nan_pct: 0.0` for `T2`, `QH`, `QE`, `QN`, `Rain`, `Evap`,
  and `RO`.

## Step 4 - GitHub Pages

Enabled GitHub Pages with:

```powershell
gh api --method POST repos/ljp416/suews-hackathon-practice/pages -F "source[branch]=main" -F "source[path]=/docs"
```

Pages configuration:

- Branch: `main`
- Path: `/docs`
- Public: `true`
- URL: https://ljp416.github.io/suews-hackathon-practice/

The final rendered URL was checked after commit and push.

## Step 5 - Commit and Push

Committed and pushed the setup evidence:

```powershell
git add docs/index.md analysis/suews_smoke transcripts/2026-06-20-setup-transcript.md
git commit -m "Add SUEWS hackathon practice smoke run"
git push origin main
```

- Commit: `cd412ed`
- Push: `main -> origin/main`
- Pages verification: HTTP 200, updated title present, and updated
  `suews-agent runtime` text present.
