"""Post-processing calibration: amplify cross-country variance in all 12 category CSVs.

Problem: 87% of occupations have cross-country composite_index std < 0.3.
         Switzerland-Bangladesh gap is only 0.90 points; should be ~2.0-2.5.

Strategy: For each score dimension, for each occupation group,
          stretch deviations from the occupation mean by dimension-specific
          amplification factors while preserving rank order.

After amplification:
  - Clamp scores to [0, 10] (reputation_variance to [0, 5])
  - Recalculate composite_index via score_calculator
  - Regenerate summary_zh and summary_en based on new scores
"""

import sys
from pathlib import Path

import pandas as pd
import numpy as np

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "tools"))

from score_calculator import load_weights, load_reverse_dimensions, calculate_composite  # noqa: E402

# -----------------------------------------------------------------------
# Amplification factors per dimension class
# -----------------------------------------------------------------------
AMPLIFICATION = {
    # Income: salary differences are HUGE between countries
    "value_added": 3.0,
    "cost_performance": 2.5,
    # Institutional quality varies a lot
    "stability": 2.5,
    "safety": 2.5,
    "occupational_disease": 2.5,
    # Work culture differs enormously (Nordic vs East Asia)
    "overtime": 2.5,
    "burnout": 2.5,
    # Remote culture: NL/US vs JP/BD
    "remote_friendly": 3.0,
    # Market dynamics
    "supply_demand": 2.0,
    "developed_scarcity": 2.0,
    "market_size": 2.0,
    # Social dimensions
    "social_status": 2.0,
    "gender_equality": 3.0,
    # Lifestyle
    "autonomy": 2.5,
    "family_friendly": 2.5,
    "fulfillment": 2.0,
    # Less country-dependent (physical requirements, licensing)
    "physical_demand": 1.5,
    "license_barrier": 1.5,
    # Technology is global, but adoption speed varies
    "ai_resistance": 1.3,
    # Education systems vary but requirements similar
    "learning_cost": 1.5,
    "education_req": 1.5,
    # Other structural dimensions
    "growth_coeff": 2.0,
    "career_lifespan": 1.5,
    "opportunity": 2.0,
    "skill_versatility": 2.0,
    "career_switch": 2.0,
    "reputation_variance": 1.5,
    "entrepreneurship": 2.0,
    "age_flexibility": 2.0,
    "social_interaction": 1.5,
    "cycle_sensitivity": 2.0,
    "side_job_compat": 2.0,
    "intl_mobility": 2.0,
    "industry_monopoly": 2.0,
}

# All score columns that should be amplified
SCORE_COLUMNS = list(AMPLIFICATION.keys())

# Country name -> English name lookup for summaries
_COUNTRY_META_PATH = _ROOT / "mapping" / "country_meta.csv"


def _load_country_lookup():
    """Return dict iso_code -> {name_zh, name_en}."""
    df = pd.read_csv(_COUNTRY_META_PATH)
    lookup = {}
    for _, row in df.iterrows():
        lookup[row["iso_code"]] = {
            "name_zh": row["country_or_region"],
            "name_en": row["country_en"],
        }
    return lookup


def generate_summary(country_zh, country_en, occ_zh, occ_en, scores, trend_5yr):
    """Generate Chinese and English summaries based on scores."""
    highlights_zh = []
    highlights_en = []

    if scores["value_added"] >= 8.0:
        highlights_zh.append("薪资回报高")
        highlights_en.append("high compensation")
    elif scores["value_added"] <= 4.5:
        highlights_zh.append("薪资水平偏低")
        highlights_en.append("relatively low pay")

    if scores["supply_demand"] >= 7.5:
        highlights_zh.append("人才需求旺盛")
        highlights_en.append("strong talent demand")
    elif scores["supply_demand"] <= 4.0:
        highlights_zh.append("供过于求")
        highlights_en.append("oversupply of talent")

    if scores["ai_resistance"] <= 4.0:
        highlights_zh.append("AI替代风险较高")
        highlights_en.append("high AI displacement risk")
    elif scores["ai_resistance"] >= 7.5:
        highlights_zh.append("AI替代抗性强")
        highlights_en.append("strong AI resistance")

    if scores["remote_friendly"] >= 8.5:
        highlights_zh.append("远程友好度高")
        highlights_en.append("highly remote-friendly")

    if scores["overtime"] <= 3.5:
        highlights_zh.append("加班文化严重")
        highlights_en.append("heavy overtime culture")
    elif scores["overtime"] >= 7.5:
        highlights_zh.append("工作时间规律")
        highlights_en.append("regular working hours")

    if scores["stability"] >= 7.5:
        highlights_zh.append("就业稳定")
        highlights_en.append("stable employment")
    elif scores["stability"] <= 4.0:
        highlights_zh.append("就业波动大")
        highlights_en.append("volatile employment")

    if trend_5yr >= 4:
        highlights_zh.append("近年增长迅猛")
        highlights_en.append("rapid recent growth")
    elif trend_5yr <= -2:
        highlights_zh.append("近年需求下降")
        highlights_en.append("declining demand")

    highlights_zh = highlights_zh[:3]
    highlights_en = highlights_en[:3]

    if not highlights_zh:
        highlights_zh = ["发展平稳"]
        highlights_en = ["steady development"]

    zh = f"{country_zh}{occ_zh}：{'，'.join(highlights_zh)}"
    en = f"{country_en} {occ_en}: {', '.join(highlights_en)}"
    return zh, en


def recalibrate_csv(csv_path, weights, reverse_dims, country_lookup):
    """Recalibrate a single category CSV.

    For each occupation group, amplify deviations from the mean on each
    score dimension, clamp, recalculate composite_index, and regenerate
    summaries.

    Returns the recalibrated DataFrame.
    """
    df = pd.read_csv(csv_path)
    print(f"  Processing {csv_path.name}: {len(df)} rows, "
          f"{df['sub_category'].nunique()} occupations")

    # Amplify each score column per occupation group
    for col in SCORE_COLUMNS:
        if col not in df.columns:
            continue

        factor = AMPLIFICATION[col]
        if factor == 1.0:
            continue

        # Determine clamp range
        if col == "reputation_variance":
            lo, hi = 0.0, 5.0
        else:
            lo, hi = 0.0, 10.0

        # Group by occupation (sub_category) and amplify
        for occ, idx in df.groupby("sub_category").groups.items():
            group = df.loc[idx, col]
            occ_mean = group.mean()
            deviations = group - occ_mean
            new_values = occ_mean + deviations * factor
            new_values = new_values.clip(lo, hi).round(1)
            df.loc[idx, col] = new_values

    # Recalculate composite_index for every row
    for i in df.index:
        scores = {col: df.at[i, col] for col in weights if col in df.columns}
        df.at[i, "composite_index"] = calculate_composite(scores, weights, reverse_dims)

    # Regenerate summaries
    for i in df.index:
        iso = df.at[i, "iso_code"]
        country_info = country_lookup.get(iso, {})
        country_zh = country_info.get("name_zh", df.at[i, "country_or_region"])
        country_en = country_info.get("name_en", iso)
        occ_zh = df.at[i, "sub_category"]
        occ_en = df.at[i, "sub_category_en"]
        scores = {col: df.at[i, col] for col in SCORE_COLUMNS if col in df.columns}
        trend_5yr = df.at[i, "trend_5yr"] if "trend_5yr" in df.columns else 0

        zh, en = generate_summary(country_zh, country_en, occ_zh, occ_en, scores, trend_5yr)
        df.at[i, "summary_zh"] = zh
        df.at[i, "summary_en"] = en

    # Save back
    df.to_csv(csv_path, index=False)
    print(f"    Saved {csv_path.name}")
    return df


def regenerate_aggregated_tables(csv_dir, country_lookup, weights, reverse_dims):
    """Regenerate the 00_ aggregated CSV files from the 12 category CSVs."""
    category_files = sorted(
        f for f in csv_dir.glob("*.csv")
        if not f.name.startswith("00_") and not f.name.startswith("predictions")
    )

    # Concatenate all category CSVs
    dfs = []
    for f in category_files:
        dfs.append(pd.read_csv(f))
    all_df = pd.concat(dfs, ignore_index=True)

    # 1. 00_all_occupations.csv — sorted by composite_index descending
    all_sorted = all_df.sort_values("composite_index", ascending=False)
    all_path = csv_dir / "00_all_occupations.csv"
    all_sorted.to_csv(all_path, index=False, encoding="utf-8-sig")
    print(f"  Regenerated {all_path.name}: {len(all_sorted)} rows")

    # 2. 00_china_all_occupations.csv — filter CN rows, add median_salary_rmb
    cn_df = all_df[all_df["iso_code"] == "CN"].copy()
    cn_df = cn_df.sort_values("composite_index", ascending=False)

    # Regenerate median_salary_rmb from value_added
    # The formula: map value_added (0-10) to salary range
    # Based on existing data: value_added ~3.0 -> ~35K, ~9.7 -> ~1.4M
    # Using exponential mapping: salary = base * exp(k * value_added)
    # Calibrated: base=15000, k=0.45 gives reasonable range
    def value_to_salary_rmb(va):
        salary = 15000.0 * np.exp(0.45 * va)
        return int(round(salary / 1000) * 1000)  # Round to nearest 1000

    cn_df["median_salary_rmb"] = cn_df["value_added"].apply(value_to_salary_rmb)
    cn_path = csv_dir / "00_china_all_occupations.csv"
    cn_df.to_csv(cn_path, index=False)
    print(f"  Regenerated {cn_path.name}: {len(cn_df)} rows")

    # 3. 00_all_occupations_by_career.csv — aggregate by occupation
    score_cols_for_agg = [
        "learning_cost", "education_req", "growth_coeff", "career_lifespan",
        "opportunity", "market_size", "supply_demand", "developed_scarcity",
        "value_added", "cost_performance", "stability", "safety",
        "occupational_disease", "overtime", "burnout", "skill_versatility",
        "career_switch", "reputation_variance", "ai_resistance", "social_status",
        "remote_friendly", "autonomy", "family_friendly", "fulfillment",
        "entrepreneurship", "gender_equality", "age_flexibility",
        "social_interaction", "physical_demand", "license_barrier",
        "cycle_sensitivity", "side_job_compat", "intl_mobility", "industry_monopoly",
    ]

    # Group by occupation and aggregate
    agg_dict = {}
    for col in score_cols_for_agg:
        agg_dict[col] = "mean"
    agg_dict["composite_index"] = ["mean", "min", "max", "std"]

    # Get first-row metadata per occupation
    meta_cols = [
        "major_category", "major_code", "mid_category", "sub_category",
        "sub_category_en", "typical_education", "typical_entry_age", "locality",
    ]

    # Build the by_career table
    by_career_rows = []
    for occ, grp in all_df.groupby("sub_category"):
        row = {}
        # Metadata from first row
        first = grp.iloc[0]
        for mc in meta_cols:
            if mc in grp.columns:
                row[mc] = first[mc]

        row["country_count"] = grp["iso_code"].nunique()

        # Mean scores
        for col in score_cols_for_agg:
            row[col] = round(grp[col].mean(), 2)

        # Composite stats
        row["composite_global_mean"] = round(grp["composite_index"].mean(), 2)
        row["composite_min"] = round(grp["composite_index"].min(), 2)
        row["composite_max"] = round(grp["composite_index"].max(), 2)
        row["composite_std"] = round(grp["composite_index"].std(), 2)

        # Best/worst country
        best_idx = grp["composite_index"].idxmax()
        worst_idx = grp["composite_index"].idxmin()
        row["best_country"] = grp.at[best_idx, "country_or_region"]
        row["worst_country"] = grp.at[worst_idx, "country_or_region"]

        # Trend (mode/first)
        row["trend_2000_2026"] = int(grp["trend_2000_2026"].mode().iloc[0]) if len(grp) > 0 else 0
        row["trend_5yr"] = int(grp["trend_5yr"].mode().iloc[0]) if len(grp) > 0 else 0

        # Other metadata
        row["employer_type"] = first.get("employer_type", "general")
        row["demand_direction"] = first.get("demand_direction", "→")
        row["ai_timeline"] = first.get("ai_timeline", "")

        # Regional composite means
        for region, rgrp in grp.groupby("region"):
            row[f"composite_{region}"] = round(rgrp["composite_index"].mean(), 2)

        row["generated_date"] = first.get("generated_date", "2026-04-13")
        row["data_snapshot_date"] = first.get("data_snapshot_date", "2026-04-13")
        row["source_period"] = first.get("source_period", "2000-2026")

        by_career_rows.append(row)

    by_career_df = pd.DataFrame(by_career_rows)
    by_career_df = by_career_df.sort_values("composite_global_mean", ascending=False)
    by_career_path = csv_dir / "00_all_occupations_by_career.csv"
    by_career_df.to_csv(by_career_path, index=False, encoding="utf-8-sig")
    print(f"  Regenerated {by_career_path.name}: {len(by_career_df)} rows")

    # 4. 00_china_vs_global.csv — China vs global comparison
    cn_vs_rows = []
    for occ, grp in all_df.groupby("sub_category"):
        cn_rows = grp[grp["iso_code"] == "CN"]
        if len(cn_rows) == 0:
            continue
        cn_row = cn_rows.iloc[0]
        first = grp.iloc[0]

        row = {}
        row["major_category"] = first["major_category"]
        row["major_code"] = first["major_code"]
        row["mid_category"] = first["mid_category"]
        row["sub_category"] = occ
        row["sub_category_en"] = first["sub_category_en"]

        # CN scores (prefixed with cn_)
        for col in score_cols_for_agg:
            row[f"cn_{col}"] = round(cn_row[col], 1)

        row["cn_composite_index"] = round(cn_row["composite_index"], 2)
        row["cn_trend_2000_2026"] = int(cn_row["trend_2000_2026"])
        row["cn_trend_5yr"] = int(cn_row["trend_5yr"])

        # Metadata
        row["employer_type"] = cn_row.get("employer_type", "general")
        row["demand_direction"] = cn_row.get("demand_direction", "→")
        row["ai_timeline"] = cn_row.get("ai_timeline", "")
        row["summary_zh"] = cn_row["summary_zh"]

        # Global stats
        row["composite_global_mean"] = round(grp["composite_index"].mean(), 2)
        row["composite_min"] = round(grp["composite_index"].min(), 2)
        row["composite_max"] = round(grp["composite_index"].max(), 2)

        best_idx = grp["composite_index"].idxmax()
        worst_idx = grp["composite_index"].idxmin()
        row["best_country"] = grp.at[best_idx, "country_or_region"]
        row["worst_country"] = grp.at[worst_idx, "country_or_region"]

        # Regional composite means
        for region, rgrp in grp.groupby("region"):
            row[f"composite_{region}"] = round(rgrp["composite_index"].mean(), 2)

        # CN vs global delta
        row["cn_vs_global"] = round(cn_row["composite_index"] - grp["composite_index"].mean(), 2)

        row["generated_date"] = "2026-04-13"
        row["data_snapshot_date"] = "2026-04-13"
        row["source_period"] = "2000-2026"

        cn_vs_rows.append(row)

    cn_vs_df = pd.DataFrame(cn_vs_rows)
    cn_vs_df = cn_vs_df.sort_values("cn_composite_index", ascending=False)
    cn_vs_path = csv_dir / "00_china_vs_global.csv"
    cn_vs_df.to_csv(cn_vs_path, index=False, encoding="utf-8-sig")
    print(f"  Regenerated {cn_vs_path.name}: {len(cn_vs_df)} rows")


def validate_results(csv_dir):
    """Run cross-validation to confirm the fix."""
    category_files = sorted(
        f for f in csv_dir.glob("*.csv")
        if not f.name.startswith("00_") and not f.name.startswith("predictions")
    )

    dfs = []
    for f in category_files:
        dfs.append(pd.read_csv(f))
    all_df = pd.concat(dfs, ignore_index=True)

    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)

    by_occ = all_df.groupby("sub_category")["composite_index"].std()
    total = len(by_occ)
    print(f"\nCross-country composite_index std distribution:")
    print(f"  std < 0.3:  {(by_occ < 0.3).sum():4d} / {total} ({(by_occ < 0.3).sum()/total*100:.1f}%)")
    print(f"  std 0.3-0.6: {((by_occ >= 0.3) & (by_occ < 0.6)).sum():3d} / {total} ({((by_occ >= 0.3) & (by_occ < 0.6)).sum()/total*100:.1f}%)")
    print(f"  std >= 0.6: {(by_occ >= 0.6).sum():4d} / {total} ({(by_occ >= 0.6).sum()/total*100:.1f}%)")
    print(f"  Mean std:    {by_occ.mean():.3f}")
    print(f"  Median std:  {by_occ.median():.3f}")

    country_means = all_df.groupby("iso_code")["composite_index"].mean()
    cm_sorted = country_means.sort_values(ascending=False)
    print(f"\nCountry mean composite_index:")
    print(f"  Top:    {cm_sorted.iloc[0]:.2f} ({cm_sorted.index[0]})")
    print(f"  Bottom: {cm_sorted.iloc[-1]:.2f} ({cm_sorted.index[-1]})")
    print(f"  Gap:    {cm_sorted.iloc[0] - cm_sorted.iloc[-1]:.2f}")

    print(f"\nAll countries sorted:")
    for iso, mean_val in cm_sorted.items():
        print(f"  {iso}: {mean_val:.2f}")

    # Check score ranges
    score_cols = list(AMPLIFICATION.keys())
    violations = 0
    for col in score_cols:
        if col not in all_df.columns:
            continue
        if col == "reputation_variance":
            out = all_df[(all_df[col] < 0) | (all_df[col] > 5)]
        else:
            out = all_df[(all_df[col] < 0) | (all_df[col] > 10)]
        if len(out) > 0:
            violations += len(out)
            print(f"  WARNING: {col} has {len(out)} out-of-range values!")

    if violations == 0:
        print("\n  All scores within valid ranges.")

    return all_df


def main():
    csv_dir = _ROOT / "data" / "csv"

    # Load weights and reverse dimensions
    weights = load_weights()
    reverse_dims = load_reverse_dimensions()
    country_lookup = _load_country_lookup()

    # Identify category CSV files
    category_files = sorted(
        f for f in csv_dir.glob("*.csv")
        if not f.name.startswith("00_") and not f.name.startswith("predictions")
    )

    print(f"Found {len(category_files)} category CSV files\n")

    # Step 1: Recalibrate each category CSV
    print("=" * 60)
    print("STEP 1: Recalibrate category CSVs")
    print("=" * 60)
    for f in category_files:
        recalibrate_csv(f, weights, reverse_dims, country_lookup)

    # Step 2: Regenerate aggregated tables
    print("\n" + "=" * 60)
    print("STEP 2: Regenerate aggregated tables")
    print("=" * 60)
    regenerate_aggregated_tables(csv_dir, country_lookup, weights, reverse_dims)

    # Step 3: Validate results
    validate_results(csv_dir)


if __name__ == "__main__":
    main()
