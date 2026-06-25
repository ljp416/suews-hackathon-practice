#!/usr/bin/env python
"""Generate corrected UDA-city heat-risk indices and comparison plots.

Run from the repository root with UTF-8 mode on Windows:

    $env:PYTHONUTF8 = "1"
    .\\.venv\\Scripts\\python analysis\\uda_city_true_data\\generate_corrected_indices.py

The corrected index addresses four critique points in the reference bridge:

1. exposure uses population / max(population), so the lowest population is low
   but not zero;
2. the final social term is additive, so one low social pillar does not erase
   all risk;
3. hazard is an absolute fraction of analysis hours, so present and future
   scores share the same scale;
4. hazard uses humid heat index hours rather than dry-bulb T2 alone.
"""

from __future__ import annotations

import math
import os
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from supy.suews_sim import SUEWSSimulation


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = REPO_ROOT / "data" / "uda-city-hackathon"
ANALYSIS_ROOT = REPO_ROOT / "analysis" / "uda_city_true_data"
PLOT_ROOT = REPO_ROOT / "docs" / "assets" / "uda_indices"

CONFIG = DATA_ROOT / "uda-city.yml"
PRESENT_FORCING = None
FUTURE_FORCING = DATA_ROOT / "forcing" / "future_hot_humid" / "UDA_2024_data_60.txt"

SPINUP_DAYS = 14
DRY_THRESHOLD_C = 35.0
HEAT_INDEX_THRESHOLD_C = 41.0


def require_utf8_mode() -> None:
    if os.name == "nt" and not sys.flags.utf8_mode:
        raise SystemExit(
            "Run with PYTHONUTF8=1 on Windows so supy can read UTF-8 YAML."
        )


def heat_index_c(t_c: pd.Series, rh_pct: pd.Series) -> pd.Series:
    """NOAA-style heat index in Celsius from temperature C and relative humidity."""
    t_f = t_c * 9.0 / 5.0 + 32.0
    rh = rh_pct.clip(lower=0.0, upper=100.0)
    simple = 0.5 * (t_f + 61.0 + ((t_f - 68.0) * 1.2) + (rh * 0.094))
    rothfusz = (
        -42.379
        + 2.04901523 * t_f
        + 10.14333127 * rh
        - 0.22475541 * t_f * rh
        - 0.00683783 * t_f * t_f
        - 0.05481717 * rh * rh
        + 0.00122874 * t_f * t_f * rh
        + 0.00085282 * t_f * rh * rh
        - 0.00000199 * t_f * t_f * rh * rh
    )
    hi_f = simple.where(simple < 80.0, rothfusz)
    return (hi_f - 32.0) * 5.0 / 9.0


def load_neighbourhoods() -> pd.DataFrame:
    data = yaml.safe_load((DATA_ROOT / "neighbourhoods.yml").read_text(encoding="utf-8"))
    rows = []
    for item in data["neighbourhoods"]:
        rows.append(
            {
                "gridiv": item["gridiv"],
                "name": item["name"],
                "type": item["type"],
                "population_day": item["population_density_per_ha"]["day"],
                "population_night": item["population_density_per_ha"]["night"],
            }
        )
    return pd.DataFrame(rows)


def vulnerability_raw(socio: pd.DataFrame) -> pd.Series:
    socio_i = socio.set_index("gridiv")
    components = pd.DataFrame(
        {
            "elderly": socio_i["frac_over65"],
            "young": socio_i["frac_under5"],
            "no_ac": 1.0 - socio_i["ac_access"],
            "outdoor_work": socio_i["frac_outdoor_workers"],
            "deprivation": socio_i["deprivation_index"],
        },
        index=socio_i.index,
    )
    return components.mean(axis=1).rename("vulnerability_raw")


def run_scenario(forcing: Path | None) -> tuple[pd.DataFrame, pd.DataFrame]:
    warnings.simplefilter("ignore")
    sim = SUEWSSimulation(str(CONFIG))
    if forcing is not None:
        sim.update_forcing(str(forcing))
    sim.run()
    if not sim.is_complete:
        raise RuntimeError("SUEWS simulation did not complete")
    return sim.results, sim.forcing.df


def hourly_forcing(forcing: pd.DataFrame, target_index: pd.DatetimeIndex) -> pd.DataFrame:
    cols = forcing[["RH"]].astype(float)
    if isinstance(cols.index, pd.DatetimeIndex):
        hourly = cols.resample("h").mean()
        aligned = hourly.reindex(target_index, method="nearest", tolerance=pd.Timedelta("31min"))
        return aligned.interpolate().ffill().bfill()
    return pd.DataFrame({"RH": np.nan}, index=target_index)


def scenario_hazard(
    scenario: str, results: pd.DataFrame, forcing: pd.DataFrame
) -> pd.DataFrame:
    rows = []
    for grid in results.index.get_level_values(0).unique():
        t2 = results.loc[grid][("SUEWS", "T2")].dropna()
        t2 = t2.iloc[SPINUP_DAYS * 288 :]
        t2_hourly = t2.resample("h").mean()
        f_hourly = hourly_forcing(forcing, t2_hourly.index)
        heat_index = heat_index_c(t2_hourly, f_hourly["RH"])
        rows.append(
            {
                "scenario": scenario,
                "gridiv": int(grid),
                "analysis_hours": int(t2_hourly.notna().sum()),
                "dry_heat_hours": int((t2_hourly > DRY_THRESHOLD_C).sum()),
                "humid_heat_hours": int((heat_index > HEAT_INDEX_THRESHOLD_C).sum()),
                "mean_t2_c": float(t2_hourly.mean()),
                "max_t2_c": float(t2_hourly.max()),
                "mean_heat_index_c": float(heat_index.mean()),
                "max_heat_index_c": float(heat_index.max()),
                "mean_rh_pct": float(f_hourly["RH"].mean()),
            }
        )
    return pd.DataFrame(rows).sort_values(["scenario", "gridiv"])


def build_corrected_index(hazards: pd.DataFrame) -> pd.DataFrame:
    neighbourhoods = load_neighbourhoods()
    socio = pd.read_csv(DATA_ROOT / "socioeconomic.csv")
    vuln = vulnerability_raw(socio)
    pop_max = neighbourhoods["population_day"].max()

    old = []
    for scenario in ("present", "future"):
        risk = pd.read_csv(ANALYSIS_ROOT / f"risk_{scenario}.csv")
        risk = risk.rename(
            columns={
                "dangerous_heat_hours": "old_dry_hours",
                "risk_index": "old_risk_index",
                "risk_rank": "old_risk_rank",
            }
        )
        risk["scenario"] = scenario
        old.append(risk[["scenario", "gridiv", "old_dry_hours", "old_risk_index", "old_risk_rank"]])
    old_df = pd.concat(old, ignore_index=True)

    df = hazards.merge(neighbourhoods, on="gridiv", how="left")
    df = df.merge(old_df, on=["scenario", "gridiv"], how="left")
    df["exposure_absolute"] = df["population_day"].astype(float) / float(pop_max)
    df["vulnerability_raw"] = df["gridiv"].map(vuln)
    df["social_sensitivity"] = 0.5 * df["exposure_absolute"] + 0.5 * df["vulnerability_raw"]
    df["humid_hazard_fraction"] = df["humid_heat_hours"] / df["analysis_hours"]
    df["corrected_risk_index"] = df["humid_hazard_fraction"] * df["social_sensitivity"]
    df["corrected_risk_rank"] = (
        df.groupby("scenario")["corrected_risk_index"]
        .rank(ascending=False, method="min")
        .astype(int)
    )
    return df.sort_values(["scenario", "corrected_risk_rank", "gridiv"])


def wide_comparison(long_df: pd.DataFrame) -> pd.DataFrame:
    keep = [
        "gridiv",
        "name",
        "type",
        "dry_heat_hours",
        "humid_heat_hours",
        "old_risk_index",
        "corrected_risk_index",
        "old_risk_rank",
        "corrected_risk_rank",
    ]
    present = long_df[long_df["scenario"] == "present"][keep]
    future = long_df[long_df["scenario"] == "future"][keep]
    wide = present.merge(future, on=["gridiv", "name", "type"], suffixes=("_present", "_future"))
    wide["delta_dry_heat_hours"] = wide["dry_heat_hours_future"] - wide["dry_heat_hours_present"]
    wide["delta_humid_heat_hours"] = wide["humid_heat_hours_future"] - wide["humid_heat_hours_present"]
    wide["delta_old_risk_index"] = wide["old_risk_index_future"] - wide["old_risk_index_present"]
    wide["delta_corrected_risk_index"] = (
        wide["corrected_risk_index_future"] - wide["corrected_risk_index_present"]
    )
    return wide.sort_values(["corrected_risk_rank_future", "gridiv"])


def save_barh(ax, labels: list[str], values: list[float], title: str, color: str) -> None:
    y = np.arange(len(labels))
    ax.barh(y, values, color=color)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.25)


def plot_scenario_delta(wide: pd.DataFrame) -> None:
    """Plot scenario deltas with deterministic label offsets for readability."""
    PLOT_ROOT.mkdir(parents=True, exist_ok=True)
    label_offsets = {
        "Kampong Lama": (14, 4),
        "Dhobi Lines": (12, 4),
        "Fuzhou Lanes": (12, 0),
        "Mlima Moto": (-14, 4),
        "Lusitano Square": (14, 8),
        "Victoria Exchange": (14, -10),
        "Zheng He Towers": (14, 4),
        "Taman Melati": (16, 14),
        "Jade Gardens": (16, 0),
        "Serendib Rise": (16, -14),
    }

    fig, ax = plt.subplots(figsize=(10, 6.5))
    for _, row in wide.iterrows():
        x = row["delta_old_risk_index"]
        y = row["delta_corrected_risk_index"]
        ax.scatter(x, y, s=65, zorder=3)
        dx, dy = label_offsets.get(row["name"], (10, 4))
        ax.annotate(
            row["name"],
            xy=(x, y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=8,
            ha="left" if dx >= 0 else "right",
            va="center",
            bbox={
                "boxstyle": "round,pad=0.15",
                "facecolor": "white",
                "edgecolor": "none",
                "alpha": 0.78,
            },
            arrowprops={
                "arrowstyle": "-",
                "color": "0.45",
                "linewidth": 0.6,
                "shrinkA": 0,
                "shrinkB": 4,
            },
            zorder=4,
        )
    ax.axvline(0, color="black", linewidth=0.8, alpha=0.4)
    ax.axhline(0, color="black", linewidth=0.8, alpha=0.4)
    ax.set_xlim(
        wide["delta_old_risk_index"].min() - 0.018,
        wide["delta_old_risk_index"].max() + 0.025,
    )
    ax.set_ylim(
        wide["delta_corrected_risk_index"].min() - 0.025,
        wide["delta_corrected_risk_index"].max() + 0.025,
    )
    ax.set_xlabel("Old relative risk delta (future - present)")
    ax.set_ylabel("Corrected absolute risk delta (future - present)")
    ax.set_title("Separate min-max scaling hides absolute worsening")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(PLOT_ROOT / "scenario_delta_old_vs_corrected.png", dpi=180)
    plt.close(fig)


def plot_outputs(long_df: pd.DataFrame, wide: pd.DataFrame) -> None:
    PLOT_ROOT.mkdir(parents=True, exist_ok=True)
    ordered = wide.sort_values("corrected_risk_rank_future")["name"].tolist()

    fig, axes = plt.subplots(1, 2, figsize=(13, 7), sharey=True)
    for ax, scenario in zip(axes, ("present", "future")):
        sub = long_df[long_df["scenario"] == scenario].set_index("name").loc[ordered].reset_index()
        y = np.arange(len(sub))
        h = 0.36
        ax.barh(y - h / 2, sub["old_risk_index"], h, label="Reference relative risk", color="#7b8794")
        ax.barh(y + h / 2, sub["corrected_risk_index"], h, label="Corrected absolute humid risk", color="#cf4f38")
        ax.set_yticks(y, sub["name"])
        ax.invert_yaxis()
        ax.set_xlim(left=0)
        ax.set_title(scenario.title())
        ax.grid(axis="x", alpha=0.25)
    axes[0].set_xlabel("Index score")
    axes[1].set_xlabel("Index score")
    axes[0].legend(loc="lower right")
    fig.suptitle("Old relative risk vs corrected absolute humid-heat risk", fontsize=14)
    fig.tight_layout()
    fig.savefig(PLOT_ROOT / "old_vs_corrected_risk.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(13, 7), sharey=True)
    for ax, scenario in zip(axes, ("present", "future")):
        sub = long_df[long_df["scenario"] == scenario].set_index("name").loc[ordered].reset_index()
        y = np.arange(len(sub))
        h = 0.36
        ax.barh(y - h / 2, sub["dry_heat_hours"], h, label="Dry T2 > 35 C", color="#456990")
        ax.barh(y + h / 2, sub["humid_heat_hours"], h, label="Heat index > 41 C", color="#d1495b")
        ax.set_yticks(y, sub["name"])
        ax.invert_yaxis()
        ax.set_title(scenario.title())
        ax.grid(axis="x", alpha=0.25)
    axes[0].set_xlabel("Hours after spin-up")
    axes[1].set_xlabel("Hours after spin-up")
    axes[0].legend(loc="lower right")
    fig.suptitle("Dry-bulb hazard vs humid-heat hazard", fontsize=14)
    fig.tight_layout()
    fig.savefig(PLOT_ROOT / "dry_vs_humid_heat_hours.png", dpi=180)
    plt.close(fig)

    plot_scenario_delta(wide)

    exposure = long_df[long_df["scenario"] == "present"][
        ["name", "population_day", "exposure_absolute"]
    ].copy()
    old_present = pd.read_csv(ANALYSIS_ROOT / "risk_present.csv")[["name", "exposure"]]
    exposure = exposure.merge(old_present, on="name", how="left").sort_values("population_day")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = np.arange(len(exposure))
    ax.plot(x, exposure["exposure"], marker="o", label="Reference min-max exposure", color="#7b8794")
    ax.plot(x, exposure["exposure_absolute"], marker="o", label="Corrected population / max", color="#2a9d8f")
    ax.set_xticks(x, exposure["name"], rotation=35, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Exposure score")
    ax.set_title("Lowest population is low exposure, not zero exposure")
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(PLOT_ROOT / "exposure_floor_effect.png", dpi=180)
    plt.close(fig)


def main() -> int:
    require_utf8_mode()
    ANALYSIS_ROOT.mkdir(parents=True, exist_ok=True)

    scenario_frames = []
    for name, forcing in (("present", PRESENT_FORCING), ("future", FUTURE_FORCING)):
        print(f"Running {name} scenario...")
        results, forcing_df = run_scenario(forcing)
        scenario_frames.append(scenario_hazard(name, results, forcing_df))

    hazards = pd.concat(scenario_frames, ignore_index=True)
    corrected = build_corrected_index(hazards)
    comparison = wide_comparison(corrected)

    hazards.to_csv(ANALYSIS_ROOT / "corrected_hazard_metrics.csv", index=False)
    corrected.to_csv(ANALYSIS_ROOT / "corrected_index_long.csv", index=False)
    comparison.to_csv(ANALYSIS_ROOT / "corrected_index_comparison.csv", index=False)
    plot_outputs(corrected, comparison)

    cols = [
        "gridiv",
        "name",
        "type",
        "humid_heat_hours_present",
        "humid_heat_hours_future",
        "delta_humid_heat_hours",
        "corrected_risk_index_present",
        "corrected_risk_index_future",
        "delta_corrected_risk_index",
        "corrected_risk_rank_future",
    ]
    print(comparison[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"Wrote outputs to {ANALYSIS_ROOT.relative_to(REPO_ROOT)} and {PLOT_ROOT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
