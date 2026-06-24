# True-data Update Transcript

Date: 2026-06-24

Repository: https://github.com/ljp416/suews-hackathon-practice

Pages URL: https://ljp416.github.io/suews-hackathon-practice/

## User Request

Pull the latest version from the original template and update the practice repo,
then use the true hackathon data.

## Upstream Sync

- Added upstream remote:

```powershell
git remote add upstream https://github.com/UMEP-dev/suews-hackathon-template.git
git fetch upstream main
```

- Upstream template was updated on 2026-06-24.
- The generated practice repo and the upstream template have unrelated histories,
  so the update was applied by checking out the changed template text files:

```powershell
git checkout upstream/main -- README.md ONBOARDING_PROMPT.md TASK_BRIEF.md analysis/README.md bridge/heat-to-risk.md data/README.md transcripts/README.md
```

- `docs/index.md` was kept as the working public page instead of replacing it
  with the upstream placeholder.

## True Dataset

- Added released dataset from:
  https://github.com/UMEP-dev/uda-city-hackathon
- Dataset commit: `0df6835c5832fb0ec78094d6acd09a45a953826b`
- Dataset vendored into `data/uda-city-hackathon/`.
- Removed the nested dataset `.git` folder before committing so the data files
  are ordinary tracked files in this repo.

## Verification

Windows UTF-8 note: the dataset contains UTF-8 YAML comments, so `PYTHONUTF8=1`
was required on this host for Python readers that otherwise default to GBK.

Commands:

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\suews validate --dry-run --format json data\uda-city-hackathon\uda-city.yml
```

Result: `is_valid: true`, `error_count: 0`.

```powershell
$env:PYTHONUTF8 = "1"
..\..\.venv\Scripts\python scripts\smoke_test.py
```

Result: 10 sites, 2,016 steps, finite `T2` and `QH`.

```powershell
$env:PYTHONUTF8 = "1"
..\..\.venv\Scripts\python risk_bridge.py --out outputs\derived\risk_present.csv
..\..\.venv\Scripts\python risk_bridge.py --forcing forcing\future_hot_humid\UDA_2024_data_60.txt --out outputs\derived\risk_future.csv
```

Result: present and future reference risk tables written under the dataset's
ignored `outputs/derived/` folder and copied to tracked files under
`analysis/uda_city_true_data/`.

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python -m pytest data\uda-city-hackathon\tests -m "not slow"
```

Result: 8 passed, 1 slow test deselected.

## Result Summary

- Present top risk: `Kampong Lama`.
- Future top risk: `Kampong Lama`.
- Largest future dangerous-heat hours: `Jade Gardens` with 260 hours, but its
  reference risk remains low because exposure is low under the supplied bridge.
- The updated Pages page reports these results and caveats.
