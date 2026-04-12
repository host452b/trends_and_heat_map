"""Generate ALL remaining notebooks (13-74) for the Global Career Development Index.

Produces pre-rendered HTML notebooks using the render_html_table approach
from generate_notebook.py so they display on GitHub without execution.

Notebooks generated:
  13-17  Ranking notebooks (regenerated with HTML)
  18-21  Trend notebooks
  22-66  Country panorama notebooks (45 countries)
  67-73  Special topic notebooks
  74     Query tool notebook (executable code cells)
"""

import sys
from pathlib import Path

import pandas as pd
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from generate_notebook import render_html_table, SCORE_COLUMNS, TREND_COLUMNS, _cell_style  # noqa: E402

NB_DIR = ROOT / "notebooks"
CSV_DIR = ROOT / "data" / "csv"
MAPPING_DIR = ROOT / "mapping"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COLOR_LEGEND = (
    "评分色阶：红色(低分0) → 黄色(中等5) → 绿色(高分10)  \n"
    "口碑方差：绿色(稳定0) → 红色(分化5)  \n"
    "趋势：红色(暴跌-5) → 白色(持平0) → 绿色(暴涨+5)"
)


def load_all_data():
    """Load and concatenate all 12 CSV files."""
    dfs = []
    for f in sorted(CSV_DIR.glob("*.csv")):
        dfs.append(pd.read_csv(f))
    return pd.concat(dfs, ignore_index=True)


def _make_nb():
    """Return a fresh notebook with Python 3 kernel metadata."""
    nb = new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    return nb


def _add_html_table_cells(nb, df, page_size=60, label=""):
    """Add paginated pre-rendered HTML table cells to notebook."""
    pages = render_html_table(df, page_size=page_size)
    for i, html in enumerate(pages, 1):
        tag = f" — {label}" if label else ""
        cell = new_code_cell(f"# Page {i} of {len(pages)}{tag}")
        cell.outputs = [
            nbformat.v4.new_output(
                output_type="display_data",
                data={"text/html": html},
            )
        ]
        nb.cells.append(cell)


def _add_stats_cell(nb, text):
    """Add a pre-rendered text output cell."""
    cell = new_code_cell("# Statistics")
    cell.outputs = [
        nbformat.v4.new_output(output_type="stream", name="stdout", text=text)
    ]
    nb.cells.append(cell)


def _select_cols(df, cols):
    """Return df with only those columns that exist."""
    return df[[c for c in cols if c in df.columns]]


def _write_nb(nb, filename):
    """Write notebook to notebooks/ directory."""
    NB_DIR.mkdir(parents=True, exist_ok=True)
    path = NB_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"  Created {path.name}")


# Column sets for different views
BASE_COLS = [
    "sub_category", "sub_category_en", "country_or_region",
    "major_category", "major_code",
]

RANKING_SCORE_COLS = [
    "growth_coeff", "opportunity", "value_added", "cost_performance",
    "ai_resistance", "stability", "developed_scarcity", "intl_mobility",
    "remote_friendly", "autonomy", "fulfillment", "composite_index",
]

AI_COLS = [
    "ai_resistance", "ai_timeline", "value_added", "growth_coeff",
    "skill_versatility", "autonomy", "physical_demand",
    "trend_5yr", "composite_index",
]

CP_COLS = [
    "cost_performance", "learning_cost", "education_req", "value_added",
    "growth_coeff", "opportunity", "stability", "composite_index",
]

SCARCITY_COLS = [
    "developed_scarcity", "intl_mobility", "value_added", "growth_coeff",
    "license_barrier", "supply_demand", "stability", "composite_index",
]

QOL_COLS = [
    "remote_friendly", "family_friendly", "burnout", "autonomy",
    "fulfillment", "value_added", "stability", "composite_index",
]

TREND_DISPLAY_COLS = [
    "trend_2000_2026", "trend_5yr", "demand_direction",
    "ai_resistance", "ai_timeline", "growth_coeff",
    "opportunity", "value_added", "composite_index",
]

COUNTRY_DISPLAY_COLS = [
    "sub_category", "sub_category_en", "mid_category",
    "major_category", "major_code",
    "growth_coeff", "opportunity", "value_added", "cost_performance",
    "ai_resistance", "supply_demand", "developed_scarcity",
    "remote_friendly", "autonomy", "fulfillment",
    "trend_2000_2026", "trend_5yr", "composite_index",
]

SPECIAL_COLS = [
    "sub_category", "sub_category_en", "country_or_region",
    "mid_category", "major_code",
    "growth_coeff", "opportunity", "value_added", "cost_performance",
    "ai_resistance", "supply_demand", "remote_friendly",
    "autonomy", "fulfillment", "entrepreneurship",
    "trend_2000_2026", "trend_5yr", "composite_index",
]


# ===================================================================
# Notebook 13: 综合发展指数 Top 100
# ===================================================================
def gen_nb13(df):
    nb = _make_nb()
    display_cols = BASE_COLS + RANKING_SCORE_COLS

    nb.cells.append(new_markdown_cell(
        "# 综合发展指数 Top 100\n\n"
        "Global Career Development Composite Index — Top 100 occupations worldwide.\n\n"
        + COLOR_LEGEND
    ))

    # Global Top 100
    nb.cells.append(new_markdown_cell("## Global Top 100 by Composite Index"))
    top100 = df.nlargest(100, "composite_index")[display_cols].reset_index(drop=True)
    top100.index = top100.index + 1
    top100.insert(0, "Rank", range(1, len(top100) + 1))
    _add_html_table_cells(nb, top100, label="Global Top 100")

    # Top 10 per major_category
    nb.cells.append(new_markdown_cell("## Top 10 per Major Category (大类)"))
    for cat in sorted(df["major_category"].unique()):
        nb.cells.append(new_markdown_cell(f"### {cat}"))
        sub = df[df["major_category"] == cat].nlargest(10, "composite_index")[display_cols].reset_index(drop=True)
        sub.insert(0, "Rank", range(1, len(sub) + 1))
        _add_html_table_cells(nb, sub, label=cat)

    # Bottom 50
    nb.cells.append(new_markdown_cell("## Bottom 50 (Lowest Composite Scores)"))
    bottom50 = df.nsmallest(50, "composite_index")[display_cols].reset_index(drop=True)
    bottom50.insert(0, "Rank", range(1, len(bottom50) + 1))
    _add_html_table_cells(nb, bottom50, label="Bottom 50")

    _write_nb(nb, "13_综合发展指数Top100.ipynb")


# ===================================================================
# Notebook 14: AI 抗性排行
# ===================================================================
def gen_nb14(df):
    nb = _make_nb()
    display_cols = BASE_COLS + AI_COLS

    nb.cells.append(new_markdown_cell(
        "# AI 抗性排行\n\n"
        "AI Resistance Rankings — Which occupations are safest from automation?\n\n"
        + COLOR_LEGEND
    ))

    # Top 50 AI-resistant
    nb.cells.append(new_markdown_cell("## Top 50 Most AI-Resistant Occupations"))
    top50 = df.nlargest(50, "ai_resistance")[display_cols].reset_index(drop=True)
    top50.insert(0, "Rank", range(1, len(top50) + 1))
    _add_html_table_cells(nb, top50, label="Top 50 AI-Resistant")

    # Top 50 AI-vulnerable
    nb.cells.append(new_markdown_cell("## Top 50 Most AI-Vulnerable Occupations"))
    bot50 = df.nsmallest(50, "ai_resistance")[display_cols].reset_index(drop=True)
    bot50.insert(0, "Rank", range(1, len(bot50) + 1))
    _add_html_table_cells(nb, bot50, label="Top 50 AI-Vulnerable")

    # By-category summary
    nb.cells.append(new_markdown_cell("## AI Resistance by Major Category"))
    cat_ai = df.groupby("major_category")["ai_resistance"].agg(
        ["mean", "median", "std", "min", "max"]
    ).round(2).sort_values("mean", ascending=False)
    cat_ai.columns = ["Mean", "Median", "Std", "Min", "Max"]
    cat_ai = cat_ai.reset_index()
    _add_html_table_cells(nb, cat_ai, label="By Category")

    # AI timeline distribution
    nb.cells.append(new_markdown_cell("## AI Timeline Distribution"))
    tl = df["ai_timeline"].value_counts().sort_index().reset_index()
    tl.columns = ["ai_timeline", "count"]
    tl["pct"] = (tl["count"] / tl["count"].sum() * 100).round(1)
    _add_stats_cell(nb, tl.to_string(index=False))

    _write_nb(nb, "14_AI抗性排行.ipynb")


# ===================================================================
# Notebook 15: 性价比排行
# ===================================================================
def gen_nb15(df):
    nb = _make_nb()
    display_cols = BASE_COLS + CP_COLS

    nb.cells.append(new_markdown_cell(
        "# 职业性价比排行\n\n"
        "Cost-Performance Rankings — Best return on investment for career choices.\n\n"
        + COLOR_LEGEND
    ))

    # Global Top 50
    nb.cells.append(new_markdown_cell("## Global Top 50 Highest Cost-Performance"))
    top50 = df.nlargest(50, "cost_performance")[display_cols].reset_index(drop=True)
    top50.insert(0, "Rank", range(1, len(top50) + 1))
    _add_html_table_cells(nb, top50, label="Top 50 Cost-Performance")

    # By education level
    nb.cells.append(new_markdown_cell("## Best Cost-Performance by Education Level"))
    for edu in sorted(df["typical_education"].dropna().unique()):
        sub = df[df["typical_education"] == edu]
        if len(sub) < 3:
            continue
        top10 = sub.nlargest(10, "cost_performance")[display_cols].reset_index(drop=True)
        top10.insert(0, "Rank", range(1, len(top10) + 1))
        nb.cells.append(new_markdown_cell(f"### {edu} (n={len(sub)})"))
        _add_html_table_cells(nb, top10, label=edu)

    # Top 5 per country
    nb.cells.append(new_markdown_cell("## Top 5 Cost-Performance per Country"))
    for country in sorted(df["country_or_region"].unique()):
        sub = df[df["country_or_region"] == country].nlargest(5, "cost_performance")[display_cols].reset_index(drop=True)
        sub.insert(0, "Rank", range(1, len(sub) + 1))
        nb.cells.append(new_markdown_cell(f"### {country}"))
        _add_html_table_cells(nb, sub, label=country)

    _write_nb(nb, "15_性价比排行.ipynb")


# ===================================================================
# Notebook 16: 稀缺度与移民价值
# ===================================================================
def gen_nb16(df):
    nb = _make_nb()
    display_cols = BASE_COLS + SCARCITY_COLS

    nb.cells.append(new_markdown_cell(
        "# 稀缺度与移民价值排行\n\n"
        "Scarcity & Immigration Value Rankings — "
        "Which occupations are most needed in developed countries and most internationally mobile?\n\n"
        + COLOR_LEGEND
    ))

    # Top 50 developed_scarcity
    nb.cells.append(new_markdown_cell("## Top 50 Most Scarce Occupations in Developed Countries"))
    top50 = df.nlargest(50, "developed_scarcity")[display_cols].reset_index(drop=True)
    top50.insert(0, "Rank", range(1, len(top50) + 1))
    _add_html_table_cells(nb, top50, label="Top 50 Scarcity")

    # Top 50 intl_mobility
    nb.cells.append(new_markdown_cell("## Top 50 Highest International Mobility"))
    top50m = df.nlargest(50, "intl_mobility")[display_cols].reset_index(drop=True)
    top50m.insert(0, "Rank", range(1, len(top50m) + 1))
    _add_html_table_cells(nb, top50m, label="Top 50 Mobility")

    # Immigration-valuable combo
    nb.cells.append(new_markdown_cell(
        "## Immigration-Valuable Occupations\n\n"
        "Occupations with BOTH `developed_scarcity >= 7` AND `intl_mobility >= 7` — "
        "the best candidates for skilled immigration pathways."
    ))
    combo = df[(df["developed_scarcity"] >= 7) & (df["intl_mobility"] >= 7)].copy()
    combo = combo.sort_values("developed_scarcity", ascending=False)
    stats = (
        f"Found {len(combo)} occupation-country combinations meeting criteria\n"
        f"Unique occupations: {combo['sub_category'].nunique()}\n"
        f"Unique countries: {combo['country_or_region'].nunique()}"
    )
    _add_stats_cell(nb, stats)
    combo_display = combo[display_cols].reset_index(drop=True)
    combo_display.insert(0, "Rank", range(1, len(combo_display) + 1))
    _add_html_table_cells(nb, combo_display, page_size=60, label="Immigration-Valuable")

    _write_nb(nb, "16_稀缺度与移民价值.ipynb")


# ===================================================================
# Notebook 17: 生活质量排行
# ===================================================================
def gen_nb17(df):
    nb = _make_nb()
    display_cols = BASE_COLS + QOL_COLS

    nb.cells.append(new_markdown_cell(
        "# 职业生活质量排行\n\n"
        "Quality of Life Rankings — Which occupations offer the best work-life balance?\n\n"
        "**Note:** Higher burnout score = less burnout (better).\n\n"
        + COLOR_LEGEND
    ))

    sections = [
        ("Top 50 Most Remote-Friendly", "remote_friendly"),
        ("Top 50 Most Family-Friendly", "family_friendly"),
        ("Top 50 Lowest Burnout (Highest Score = Least Burnout)", "burnout"),
        ("Top 50 Highest Autonomy", "autonomy"),
        ("Top 50 Highest Fulfillment", "fulfillment"),
    ]
    for title, col in sections:
        nb.cells.append(new_markdown_cell(f"## {title}"))
        top50 = df.nlargest(50, col)[display_cols].reset_index(drop=True)
        top50.insert(0, "Rank", range(1, len(top50) + 1))
        _add_html_table_cells(nb, top50, label=title)

    # Dream jobs composite
    nb.cells.append(new_markdown_cell(
        "## Dream Jobs Composite\n\n"
        "Average of (remote_friendly + family_friendly + burnout + autonomy + fulfillment) / 5.\n"
        "The ultimate work-life balance occupations."
    ))
    dream_components = ["remote_friendly", "family_friendly", "burnout", "autonomy", "fulfillment"]
    df_copy = df.copy()
    df_copy["dream_score"] = df_copy[dream_components].mean(axis=1).round(2)
    dream_cols = BASE_COLS + dream_components + ["dream_score", "value_added", "composite_index"]
    top50d = df_copy.nlargest(50, "dream_score")[dream_cols].reset_index(drop=True)
    top50d.insert(0, "Rank", range(1, len(top50d) + 1))
    _add_html_table_cells(nb, top50d, label="Dream Jobs")

    _write_nb(nb, "17_生活质量排行.ipynb")


# ===================================================================
# Notebook 18: 2000-2026赢家与输家
# ===================================================================
def gen_nb18(df):
    nb = _make_nb()
    display_cols = BASE_COLS + TREND_DISPLAY_COLS

    nb.cells.append(new_markdown_cell(
        "# 2000-2026 赢家与输家\n\n"
        "Winners and Losers of 2000-2026 — Which occupations gained or lost the most?\n\n"
        + COLOR_LEGEND
    ))

    # Top 50 winners
    nb.cells.append(new_markdown_cell(
        "## Top 50 Winners (Strongest Positive Trend 2000-2026)\n\n"
        "Occupations with trend_2000_2026 scores from +5 (booming) to +3."
    ))
    winners = df.nlargest(50, "trend_2000_2026")[display_cols].reset_index(drop=True)
    winners.insert(0, "Rank", range(1, len(winners) + 1))
    _add_html_table_cells(nb, winners, label="Winners")

    # Winner stats
    w_stats = df.nlargest(50, "trend_2000_2026")
    stats_text = (
        f"=== Winners Summary ===\n"
        f"trend_2000_2026 range: [{w_stats['trend_2000_2026'].min():.1f}, {w_stats['trend_2000_2026'].max():.1f}]\n"
        f"Unique occupations: {w_stats['sub_category'].nunique()}\n"
        f"Major categories: {', '.join(sorted(w_stats['major_category'].unique()))}\n"
    )
    _add_stats_cell(nb, stats_text)

    # Top 50 losers
    nb.cells.append(new_markdown_cell(
        "## Top 50 Losers (Strongest Negative Trend 2000-2026)\n\n"
        "Occupations with trend_2000_2026 scores from -5 (collapsing) to -3."
    ))
    losers = df.nsmallest(50, "trend_2000_2026")[display_cols].reset_index(drop=True)
    losers.insert(0, "Rank", range(1, len(losers) + 1))
    _add_html_table_cells(nb, losers, label="Losers")

    # Loser stats
    l_stats = df.nsmallest(50, "trend_2000_2026")
    stats_text = (
        f"=== Losers Summary ===\n"
        f"trend_2000_2026 range: [{l_stats['trend_2000_2026'].min():.1f}, {l_stats['trend_2000_2026'].max():.1f}]\n"
        f"Unique occupations: {l_stats['sub_category'].nunique()}\n"
        f"Major categories: {', '.join(sorted(l_stats['major_category'].unique()))}\n"
    )
    _add_stats_cell(nb, stats_text)

    # Trend by category
    nb.cells.append(new_markdown_cell("## Trend Summary by Major Category"))
    cat_trend = df.groupby("major_category").agg(
        mean_trend=("trend_2000_2026", "mean"),
        median_trend=("trend_2000_2026", "median"),
        mean_5yr=("trend_5yr", "mean"),
        pct_positive=("trend_2000_2026", lambda x: (x > 0).mean() * 100),
        pct_negative=("trend_2000_2026", lambda x: (x < 0).mean() * 100),
    ).round(2).sort_values("mean_trend", ascending=False).reset_index()
    _add_html_table_cells(nb, cat_trend, label="Trend by Category")

    _write_nb(nb, "18_2000-2026赢家与输家.ipynb")


# ===================================================================
# Notebook 19: AI冲击波分析
# ===================================================================
def gen_nb19(df):
    nb = _make_nb()
    display_cols = BASE_COLS + AI_COLS

    nb.cells.append(new_markdown_cell(
        "# AI 冲击波分析\n\n"
        "AI Impact Wave Analysis — When will AI significantly impact each occupation?\n\n"
        + COLOR_LEGEND
    ))

    # Overview by timeline
    nb.cells.append(new_markdown_cell("## Occupations per AI Timeline Bucket"))
    tl_stats = df.groupby("ai_timeline").agg(
        count=("sub_category", "size"),
        unique_occupations=("sub_category", "nunique"),
        mean_ai_resistance=("ai_resistance", "mean"),
        mean_composite=("composite_index", "mean"),
        mean_value_added=("value_added", "mean"),
    ).round(2).sort_index().reset_index()
    _add_html_table_cells(nb, tl_stats, label="Timeline Overview")

    # Occupations per timeline bucket
    for timeline in sorted(df["ai_timeline"].dropna().unique()):
        nb.cells.append(new_markdown_cell(f"### {timeline}"))
        sub = df[df["ai_timeline"] == timeline].sort_values("ai_resistance", ascending=True)
        # Show top 60 most vulnerable in each bucket
        sub_display = sub.head(60)[display_cols].reset_index(drop=True)
        sub_display.insert(0, "#", range(1, len(sub_display) + 1))
        _add_html_table_cells(nb, sub_display, label=timeline)
        count_text = f"Total in {timeline}: {len(sub)} records, {sub['sub_category'].nunique()} unique occupations"
        _add_stats_cell(nb, count_text)

    # By-category AI vulnerability
    nb.cells.append(new_markdown_cell("## AI Vulnerability by Category x Timeline"))
    cross = pd.crosstab(df["major_category"], df["ai_timeline"])
    cross = cross.reset_index()
    _add_html_table_cells(nb, cross, label="Category x Timeline")

    _write_nb(nb, "19_AI冲击波分析.ipynb")


# ===================================================================
# Notebook 20: 各国职业结构演变
# ===================================================================
def gen_nb20(df):
    nb = _make_nb()

    nb.cells.append(new_markdown_cell(
        "# 各国职业结构演变\n\n"
        "Country-Level Career Structure Evolution — "
        "Which countries are gaining/losing in career development trends?\n\n"
        + COLOR_LEGEND
    ))

    # Country summary
    nb.cells.append(new_markdown_cell("## Country Trend Summary"))
    country_trend = df.groupby(["iso_code", "country_or_region"]).agg(
        n_occupations=("sub_category", "nunique"),
        mean_trend_2000_2026=("trend_2000_2026", "mean"),
        median_trend_2000_2026=("trend_2000_2026", "median"),
        mean_trend_5yr=("trend_5yr", "mean"),
        mean_composite=("composite_index", "mean"),
        mean_ai_resistance=("ai_resistance", "mean"),
        pct_positive_trend=("trend_2000_2026", lambda x: round((x > 0).mean() * 100, 1)),
        pct_negative_trend=("trend_2000_2026", lambda x: round((x < 0).mean() * 100, 1)),
    ).round(2).sort_values("mean_trend_2000_2026", ascending=False).reset_index()
    _add_html_table_cells(nb, country_trend, label="Country Summary")

    # Top gaining countries
    nb.cells.append(new_markdown_cell("## Top 10 Countries with Strongest Positive Trends"))
    top_gain = country_trend.nlargest(10, "mean_trend_2000_2026")
    _add_html_table_cells(nb, top_gain, label="Gaining Countries")

    # Top losing countries
    nb.cells.append(new_markdown_cell("## Top 10 Countries with Weakest / Negative Trends"))
    top_lose = country_trend.nsmallest(10, "mean_trend_2000_2026")
    _add_html_table_cells(nb, top_lose, label="Losing Countries")

    # By country x category trend
    nb.cells.append(new_markdown_cell("## Mean Trend 2000-2026 by Country x Category"))
    cross = pd.pivot_table(
        df, values="trend_2000_2026",
        index="country_or_region", columns="major_code",
        aggfunc="mean"
    ).round(2).reset_index()
    _add_html_table_cells(nb, cross, label="Country x Category Trend")

    _write_nb(nb, "20_各国职业结构演变.ipynb")


# ===================================================================
# Notebook 21: 供需失衡预警
# ===================================================================
def gen_nb21(df):
    nb = _make_nb()
    display_cols = BASE_COLS + [
        "supply_demand", "developed_scarcity", "growth_coeff",
        "market_size", "opportunity", "trend_2000_2026", "trend_5yr",
        "composite_index",
    ]

    nb.cells.append(new_markdown_cell(
        "# 供需失衡预警\n\n"
        "Supply-Demand Imbalance Alert — Identifying extreme shortage and oversupply.\n\n"
        "supply_demand: 高分 = 供不应求 (shortage), 低分 = 供过于求 (oversupply)\n\n"
        + COLOR_LEGEND
    ))

    # Top 50 shortage (high supply_demand)
    nb.cells.append(new_markdown_cell("## Top 50 Most Severe Shortages (Highest supply_demand)"))
    top_short = df.nlargest(50, "supply_demand")[display_cols].reset_index(drop=True)
    top_short.insert(0, "Rank", range(1, len(top_short) + 1))
    _add_html_table_cells(nb, top_short, label="Shortage")

    # Top 50 oversupply (low supply_demand)
    nb.cells.append(new_markdown_cell("## Top 50 Most Severe Oversupply (Lowest supply_demand)"))
    top_over = df.nsmallest(50, "supply_demand")[display_cols].reset_index(drop=True)
    top_over.insert(0, "Rank", range(1, len(top_over) + 1))
    _add_html_table_cells(nb, top_over, label="Oversupply")

    # By-country shortage/oversupply summary
    nb.cells.append(new_markdown_cell("## By-Country Shortage / Oversupply Summary"))
    country_sd = df.groupby(["iso_code", "country_or_region"]).agg(
        mean_supply_demand=("supply_demand", "mean"),
        n_shortage=("supply_demand", lambda x: (x >= 7).sum()),
        n_oversupply=("supply_demand", lambda x: (x <= 3).sum()),
        n_balanced=("supply_demand", lambda x: ((x > 3) & (x < 7)).sum()),
        mean_scarcity=("developed_scarcity", "mean"),
    ).round(2).sort_values("mean_supply_demand", ascending=False).reset_index()
    _add_html_table_cells(nb, country_sd, label="Country Supply-Demand")

    # By-category
    nb.cells.append(new_markdown_cell("## By-Category Supply-Demand Summary"))
    cat_sd = df.groupby("major_category").agg(
        mean_supply_demand=("supply_demand", "mean"),
        n_shortage=("supply_demand", lambda x: (x >= 7).sum()),
        n_oversupply=("supply_demand", lambda x: (x <= 3).sum()),
    ).round(2).sort_values("mean_supply_demand", ascending=False).reset_index()
    _add_html_table_cells(nb, cat_sd, label="Category Supply-Demand")

    _write_nb(nb, "21_供需失衡预警.ipynb")


# ===================================================================
# Country Panorama Notebooks (22-66)
# ===================================================================
COUNTRY_ORDER = [
    ("CN", 22), ("US", 23), ("JP", 24), ("KR", 25), ("TW", 26),
    ("HK", 27), ("SG", 28), ("TH", 29), ("VN", 30), ("ID", 31),
    ("MY", 32), ("PH", 33), ("IN", 34), ("PK", 35), ("BD", 36),
    ("AE", 37), ("IL", 38), ("SA", 39), ("TR", 40), ("GB", 41),
    ("FR", 42), ("DE", 43), ("NL", 44), ("CH", 45), ("SE", 46),
    ("DK", 47), ("FI", 48), ("IT", 49), ("ES", 50), ("PT", 51),
    ("PL", 52), ("CZ", 53), ("RU", 54), ("CA", 55), ("MX", 56),
    ("BR", 57), ("AR", 58), ("CL", 59), ("CO", 60), ("AU", 61),
    ("NZ", 62), ("ZA", 63), ("NG", 64), ("KE", 65), ("EG", 66),
]


def gen_country_notebooks(df):
    """Generate 45 country panorama notebooks (22-66)."""
    # Load country metadata
    meta = pd.read_csv(MAPPING_DIR / "country_meta.csv")
    iso_to_name = dict(zip(meta["iso_code"], meta["country_or_region"]))
    iso_to_en = dict(zip(meta["iso_code"], meta["country_en"]))

    for iso, num in COUNTRY_ORDER:
        cn_name = iso_to_name.get(iso, iso)
        en_name = iso_to_en.get(iso, iso)
        title = f"{cn_name}职业全景 ({en_name} Career Panorama)"
        desc = f"{cn_name}所有职业的综合发展指数排行，覆盖12大类。"
        filename = f"{num:02d}_{iso}_{cn_name}职业全景.ipynb"

        nb = _make_nb()

        # Title cell
        nb.cells.append(new_markdown_cell(
            f"# {title}\n\n{desc}\n\n{COLOR_LEGEND}"
        ))

        # Filter data
        country_df = df[df["iso_code"] == iso].copy()
        country_df = country_df.sort_values("composite_index", ascending=False)

        # Stats
        stats = (
            f"记录数: {len(country_df)}\n"
            f"职业细类: {country_df['sub_category'].nunique()}\n"
            f"大类覆盖: {country_df['major_category'].nunique()}\n"
            f"composite_index 均值: {country_df['composite_index'].mean():.2f}\n"
            f"composite_index 中位数: {country_df['composite_index'].median():.2f}"
        )
        _add_stats_cell(nb, stats)

        # Full table
        display_cols = [c for c in COUNTRY_DISPLAY_COLS if c in country_df.columns]
        table_df = country_df[display_cols].reset_index(drop=True)
        table_df.insert(0, "Rank", range(1, len(table_df) + 1))
        _add_html_table_cells(nb, table_df, page_size=60, label=cn_name)

        # Summary by major_category
        nb.cells.append(new_markdown_cell(f"## {cn_name} — 大类汇总"))
        cat_summary = country_df.groupby("major_category").agg(
            n=("sub_category", "nunique"),
            mean_composite=("composite_index", "mean"),
            mean_growth=("growth_coeff", "mean"),
            mean_ai_resist=("ai_resistance", "mean"),
            mean_trend=("trend_2000_2026", "mean"),
        ).round(2).sort_values("mean_composite", ascending=False).reset_index()
        _add_html_table_cells(nb, cat_summary, label="Category Summary")

        _write_nb(nb, filename)


# ===================================================================
# Special Topic Notebooks (67-73)
# ===================================================================

def gen_nb67(df):
    """自媒体与内容创作者生态"""
    nb = _make_nb()
    nb.cells.append(new_markdown_cell(
        "# 自媒体与内容创作者生态\n\n"
        "New Media & Content Creator Ecosystem — "
        "All occupations in the 新媒体内容 (New Media Content) mid-category across all countries.\n\n"
        + COLOR_LEGEND
    ))

    sub = df[df["mid_category"] == "新媒体内容"].copy()
    sub = sub.sort_values("composite_index", ascending=False)

    stats = (
        f"记录数: {len(sub)}\n"
        f"职业细类: {sub['sub_category'].nunique()}\n"
        f"国家/地区: {sub['country_or_region'].nunique()}\n"
        f"Occupations: {', '.join(sorted(sub['sub_category'].unique()))}"
    )
    _add_stats_cell(nb, stats)

    display_cols = [c for c in SPECIAL_COLS if c in sub.columns]
    table = sub[display_cols].reset_index(drop=True)
    table.insert(0, "#", range(1, len(table) + 1))
    _add_html_table_cells(nb, table, page_size=60, label="Content Creators")

    # Summary by occupation
    nb.cells.append(new_markdown_cell("## Summary by Occupation"))
    occ_summary = sub.groupby("sub_category").agg(
        mean_composite=("composite_index", "mean"),
        mean_growth=("growth_coeff", "mean"),
        mean_ai=("ai_resistance", "mean"),
        mean_remote=("remote_friendly", "mean"),
        mean_autonomy=("autonomy", "mean"),
        mean_entrepreneurship=("entrepreneurship", "mean"),
    ).round(2).sort_values("mean_composite", ascending=False).reset_index()
    _add_html_table_cells(nb, occ_summary, label="By Occupation")

    _write_nb(nb, "67_自媒体与内容创作者生态.ipynb")


def gen_nb68(df):
    """一人公司与自由职业"""
    nb = _make_nb()
    nb.cells.append(new_markdown_cell(
        "# 一人公司与自由职业\n\n"
        "Solo Business & Freelancing — Occupations with high entrepreneurship and autonomy, "
        "suitable for one-person companies and freelancers.\n\n"
        "Filter: `entrepreneurship >= 7.0` AND `autonomy >= 7.0`\n\n"
        + COLOR_LEGEND
    ))

    sub = df[(df["entrepreneurship"] >= 7.0) & (df["autonomy"] >= 7.0)].copy()
    sub = sub.sort_values("entrepreneurship", ascending=False)

    stats = (
        f"记录数: {len(sub)}\n"
        f"职业细类: {sub['sub_category'].nunique()}\n"
        f"国家/地区: {sub['country_or_region'].nunique()}"
    )
    _add_stats_cell(nb, stats)

    display_cols = [c for c in SPECIAL_COLS if c in sub.columns]
    table = sub[display_cols].reset_index(drop=True)
    table.insert(0, "#", range(1, len(table) + 1))
    _add_html_table_cells(nb, table, page_size=60, label="Solo/Freelance")

    # Summary by category
    nb.cells.append(new_markdown_cell("## Distribution by Major Category"))
    cat_summary = sub.groupby("major_category").agg(
        count=("sub_category", "size"),
        unique=("sub_category", "nunique"),
        mean_entrepreneurship=("entrepreneurship", "mean"),
        mean_autonomy=("autonomy", "mean"),
        mean_remote=("remote_friendly", "mean"),
        mean_composite=("composite_index", "mean"),
    ).round(2).sort_values("count", ascending=False).reset_index()
    _add_html_table_cells(nb, cat_summary, label="By Category")

    _write_nb(nb, "68_一人公司与自由职业.ipynb")


def gen_nb69(df):
    """网红与影响力经济"""
    nb = _make_nb()
    nb.cells.append(new_markdown_cell(
        "# 网红与影响力经济\n\n"
        "KOL / Influencer Economy — "
        "Occupations related to KOL, influencer, and internet celebrity careers.\n\n"
        + COLOR_LEGEND
    ))

    kol_keywords = ["KOL", "网红", "YouTuber", "博主", "VTuber", "播客", "短视频", "MCN"]
    mask = df["sub_category"].str.contains("|".join(kol_keywords), case=False, na=False)
    sub = df[mask].copy()
    sub = sub.sort_values("composite_index", ascending=False)

    stats = (
        f"记录数: {len(sub)}\n"
        f"职业细类: {sub['sub_category'].nunique()}\n"
        f"国家/地区: {sub['country_or_region'].nunique()}\n"
        f"Occupations: {', '.join(sorted(sub['sub_category'].unique()))}"
    )
    _add_stats_cell(nb, stats)

    display_cols = [c for c in SPECIAL_COLS if c in sub.columns]
    table = sub[display_cols].reset_index(drop=True)
    table.insert(0, "#", range(1, len(table) + 1))
    _add_html_table_cells(nb, table, page_size=60, label="KOL/Influencer")

    # Cross-country comparison
    nb.cells.append(new_markdown_cell("## Cross-Country Comparison"))
    country_summary = sub.groupby(["sub_category", "country_or_region"]).agg(
        composite=("composite_index", "first"),
        growth=("growth_coeff", "first"),
        ai_resist=("ai_resistance", "first"),
    ).round(2).reset_index()
    pivot = pd.pivot_table(country_summary, values="composite",
                           index="sub_category", columns="country_or_region",
                           aggfunc="first").round(2)
    pivot = pivot.reset_index()
    _add_html_table_cells(nb, pivot, page_size=60, label="Cross-Country")

    _write_nb(nb, "69_网红与影响力经济.ipynb")


def gen_nb70(df):
    """直播产业全景"""
    nb = _make_nb()
    nb.cells.append(new_markdown_cell(
        "# 直播产业全景\n\n"
        "Live-Streaming Industry Panorama — "
        "All occupations related to live streaming and livestream commerce.\n\n"
        + COLOR_LEGEND
    ))

    live_keywords = ["直播", "主播", "VTuber", "Streamer", "streamer", "Livestream"]
    mask_zh = df["sub_category"].str.contains("|".join(live_keywords[:3]), case=False, na=False)
    mask_en = df["sub_category_en"].str.contains("|".join(live_keywords[3:]), case=False, na=False)
    sub = df[mask_zh | mask_en].copy()
    sub = sub.sort_values("composite_index", ascending=False)

    stats = (
        f"记录数: {len(sub)}\n"
        f"职业细类: {sub['sub_category'].nunique()}\n"
        f"国家/地区: {sub['country_or_region'].nunique()}\n"
        f"Occupations: {', '.join(sorted(sub['sub_category'].unique()))}"
    )
    _add_stats_cell(nb, stats)

    display_cols = [c for c in SPECIAL_COLS if c in sub.columns]
    table = sub[display_cols].reset_index(drop=True)
    table.insert(0, "#", range(1, len(table) + 1))
    _add_html_table_cells(nb, table, page_size=60, label="Live-Streaming")

    # By country
    nb.cells.append(new_markdown_cell("## Live-Streaming Scores by Country"))
    country_live = sub.groupby("country_or_region").agg(
        n_occupations=("sub_category", "nunique"),
        mean_composite=("composite_index", "mean"),
        mean_growth=("growth_coeff", "mean"),
        mean_value=("value_added", "mean"),
        mean_trend=("trend_2000_2026", "mean"),
    ).round(2).sort_values("mean_composite", ascending=False).reset_index()
    _add_html_table_cells(nb, country_live, label="By Country")

    _write_nb(nb, "70_直播产业全景.ipynb")


def gen_nb71(df):
    """运动员与体育产业"""
    nb = _make_nb()
    nb.cells.append(new_markdown_cell(
        "# 运动员与体育产业\n\n"
        "Sports & Athletics Industry — "
        "All occupations in the 体育竞技 (Sports Athletics) mid-category.\n\n"
        + COLOR_LEGEND
    ))

    sub = df[df["mid_category"] == "体育竞技"].copy()
    sub = sub.sort_values("composite_index", ascending=False)

    stats = (
        f"记录数: {len(sub)}\n"
        f"职业细类: {sub['sub_category'].nunique()}\n"
        f"国家/地区: {sub['country_or_region'].nunique()}\n"
        f"Occupations: {', '.join(sorted(sub['sub_category'].unique()))}"
    )
    _add_stats_cell(nb, stats)

    display_cols = [c for c in SPECIAL_COLS if c in sub.columns]
    table = sub[display_cols].reset_index(drop=True)
    table.insert(0, "#", range(1, len(table) + 1))
    _add_html_table_cells(nb, table, page_size=60, label="Sports")

    # Summary by occupation
    nb.cells.append(new_markdown_cell("## Summary by Occupation"))
    occ_summary = sub.groupby("sub_category").agg(
        mean_composite=("composite_index", "mean"),
        mean_value=("value_added", "mean"),
        mean_ai=("ai_resistance", "mean"),
        mean_growth=("growth_coeff", "mean"),
        mean_fulfillment=("fulfillment", "mean"),
        mean_trend=("trend_2000_2026", "mean"),
    ).round(2).sort_values("mean_composite", ascending=False).reset_index()
    _add_html_table_cells(nb, occ_summary, label="By Occupation")

    _write_nb(nb, "71_运动员与体育产业.ipynb")


def gen_nb72(df):
    """平台零工与新型雇佣"""
    nb = _make_nb()
    nb.cells.append(new_markdown_cell(
        "# 平台零工与新型雇佣\n\n"
        "Platform Gig & New Employment — "
        "All occupations in the 平台零工 (Platform Gig) mid-category.\n\n"
        + COLOR_LEGEND
    ))

    sub = df[df["mid_category"] == "平台零工"].copy()
    sub = sub.sort_values("composite_index", ascending=False)

    stats = (
        f"记录数: {len(sub)}\n"
        f"职业细类: {sub['sub_category'].nunique()}\n"
        f"国家/地区: {sub['country_or_region'].nunique()}\n"
        f"Occupations: {', '.join(sorted(sub['sub_category'].unique()))}"
    )
    _add_stats_cell(nb, stats)

    display_cols = [c for c in SPECIAL_COLS if c in sub.columns]
    table = sub[display_cols].reset_index(drop=True)
    table.insert(0, "#", range(1, len(table) + 1))
    _add_html_table_cells(nb, table, page_size=60, label="Platform Gig")

    # Summary by occupation
    nb.cells.append(new_markdown_cell("## Summary by Occupation"))
    occ_summary = sub.groupby("sub_category").agg(
        mean_composite=("composite_index", "mean"),
        mean_cost_perf=("cost_performance", "mean"),
        mean_autonomy=("autonomy", "mean"),
        mean_stability=("stability", "mean"),
        mean_ai=("ai_resistance", "mean"),
        mean_trend=("trend_2000_2026", "mean"),
    ).round(2).sort_values("mean_composite", ascending=False).reset_index()
    _add_html_table_cells(nb, occ_summary, label="By Occupation")

    # By country
    nb.cells.append(new_markdown_cell("## Platform Gig Scores by Country"))
    country_gig = sub.groupby("country_or_region").agg(
        n=("sub_category", "nunique"),
        mean_composite=("composite_index", "mean"),
        mean_cost_perf=("cost_performance", "mean"),
        mean_stability=("stability", "mean"),
    ).round(2).sort_values("mean_composite", ascending=False).reset_index()
    _add_html_table_cells(nb, country_gig, label="By Country")

    _write_nb(nb, "72_平台零工与新型雇佣.ipynb")


def gen_nb73(df):
    """文化产业生态"""
    nb = _make_nb()
    nb.cells.append(new_markdown_cell(
        "# 文化产业生态\n\n"
        "Cultural Industry Ecosystem — "
        "All occupations in the 文化、艺术与传媒 (ART) major category, grouped by mid_category.\n\n"
        + COLOR_LEGEND
    ))

    sub = df[df["major_code"] == "ART"].copy()
    sub = sub.sort_values("composite_index", ascending=False)

    stats = (
        f"记录数: {len(sub)}\n"
        f"职业细类: {sub['sub_category'].nunique()}\n"
        f"中类: {sub['mid_category'].nunique()}\n"
        f"国家/地区: {sub['country_or_region'].nunique()}"
    )
    _add_stats_cell(nb, stats)

    # Overview by mid_category
    nb.cells.append(new_markdown_cell("## Overview by Mid-Category"))
    mid_summary = sub.groupby("mid_category").agg(
        n_occupations=("sub_category", "nunique"),
        n_records=("sub_category", "size"),
        mean_composite=("composite_index", "mean"),
        mean_growth=("growth_coeff", "mean"),
        mean_ai=("ai_resistance", "mean"),
        mean_value=("value_added", "mean"),
        mean_fulfillment=("fulfillment", "mean"),
        mean_trend=("trend_2000_2026", "mean"),
    ).round(2).sort_values("mean_composite", ascending=False).reset_index()
    _add_html_table_cells(nb, mid_summary, label="Mid-Category Overview")

    # Top occupations per mid_category
    for mid_cat in sorted(sub["mid_category"].unique()):
        nb.cells.append(new_markdown_cell(f"### {mid_cat}"))
        mid_sub = sub[sub["mid_category"] == mid_cat].sort_values("composite_index", ascending=False)
        display_cols = [c for c in SPECIAL_COLS if c in mid_sub.columns]
        table = mid_sub[display_cols].reset_index(drop=True)
        table.insert(0, "#", range(1, len(table) + 1))
        # Show at most 120 rows per mid_category (2 pages)
        _add_html_table_cells(nb, table.head(120), page_size=60, label=mid_cat)

    _write_nb(nb, "73_文化产业生态.ipynb")


# ===================================================================
# Notebook 74: Query Tool
# ===================================================================
def gen_nb74():
    """Query tool notebook with executable code cells (no pre-rendered output)."""
    nb = _make_nb()

    nb.cells.append(new_markdown_cell(
        "# Career Development Index — Query Tool\n\n"
        "Interactive utility notebook for querying the Global Career Development Index data.\n\n"
        "Run each cell to load data and define query functions, then use them in new cells.\n\n"
        "**Note:** This notebook is designed to be executed interactively."
    ))

    # Cell 1: load_all_data
    nb.cells.append(new_code_cell('''import pandas as pd
from pathlib import Path

def load_all_data():
    """Load all 12 CSV files and return concatenated DataFrame."""
    csv_dir = Path("../data/csv")
    if not csv_dir.exists():
        csv_dir = Path("data/csv")  # fallback for running from root
    dfs = []
    for f in sorted(csv_dir.glob("*.csv")):
        dfs.append(pd.read_csv(f))
    df = pd.concat(dfs, ignore_index=True)
    print(f"Loaded {len(df)} records, {df['sub_category'].nunique()} occupations, "
          f"{df['country_or_region'].nunique()} countries/regions")
    return df

df = load_all_data()
'''))

    # Cell 2: find_jobs
    nb.cells.append(new_code_cell('''def find_jobs(country=None, category=None, keyword=None,
              min_composite=None, min_ai_resistance=None,
              min_remote=None, min_salary=None, sort_by="composite_index",
              top_n=20):
    """Find jobs matching given filters.

    Args:
        country: Country name (Chinese) or iso_code, e.g. '中国' or 'CN'
        category: major_category or major_code, e.g. 'TECH'
        keyword: Search in sub_category or sub_category_en
        min_composite: Minimum composite_index
        min_ai_resistance: Minimum ai_resistance score
        min_remote: Minimum remote_friendly score
        min_salary: Minimum value_added score
        sort_by: Column to sort by (default: composite_index)
        top_n: Number of results to show (default: 20)

    Returns:
        Filtered and sorted DataFrame
    """
    result = df.copy()

    if country:
        mask = (result["country_or_region"] == country) | (result["iso_code"] == country)
        result = result[mask]

    if category:
        mask = (result["major_category"] == category) | (result["major_code"] == category)
        result = result[mask]

    if keyword:
        mask = (result["sub_category"].str.contains(keyword, case=False, na=False) |
                result["sub_category_en"].str.contains(keyword, case=False, na=False))
        result = result[mask]

    if min_composite is not None:
        result = result[result["composite_index"] >= min_composite]
    if min_ai_resistance is not None:
        result = result[result["ai_resistance"] >= min_ai_resistance]
    if min_remote is not None:
        result = result[result["remote_friendly"] >= min_remote]
    if min_salary is not None:
        result = result[result["value_added"] >= min_salary]

    result = result.sort_values(sort_by, ascending=False).head(top_n)

    display_cols = [
        "sub_category", "sub_category_en", "country_or_region",
        "major_code", "composite_index", "ai_resistance",
        "value_added", "cost_performance", "remote_friendly",
        "growth_coeff", "trend_5yr",
    ]
    return result[[c for c in display_cols if c in result.columns]]

# Example: find_jobs(country="CN", min_ai_resistance=7, min_remote=7)
'''))

    # Cell 3: compare
    nb.cells.append(new_code_cell('''def compare(occupation, countries=None):
    """Compare an occupation across multiple countries.

    Args:
        occupation: sub_category name (Chinese), e.g. '前端工程师'
        countries: List of country names or iso_codes. If None, show all.

    Returns:
        Comparison DataFrame
    """
    result = df[df["sub_category"] == occupation].copy()
    if countries:
        mask = result["country_or_region"].isin(countries) | result["iso_code"].isin(countries)
        result = result[mask]

    result = result.sort_values("composite_index", ascending=False)

    display_cols = [
        "country_or_region", "iso_code", "composite_index",
        "value_added", "cost_performance", "ai_resistance",
        "growth_coeff", "supply_demand", "developed_scarcity",
        "remote_friendly", "stability", "trend_2000_2026", "trend_5yr",
    ]
    return result[[c for c in display_cols if c in result.columns]]

# Example: compare("前端工程师", ["CN", "US", "JP", "DE", "IN"])
'''))

    # Cell 4: top_n
    nb.cells.append(new_code_cell('''def top_n(category=None, metric="composite_index", n=20, country=None):
    """Get top N occupations by a given metric.

    Args:
        category: major_code or major_category (None = all)
        metric: Score column to rank by
        n: Number of results
        country: Optional country filter

    Returns:
        Top N DataFrame
    """
    result = df.copy()
    if category:
        mask = (result["major_category"] == category) | (result["major_code"] == category)
        result = result[mask]
    if country:
        mask = (result["country_or_region"] == country) | (result["iso_code"] == country)
        result = result[mask]

    result = result.nlargest(n, metric)

    display_cols = [
        "sub_category", "sub_category_en", "country_or_region",
        "major_code", metric, "composite_index",
        "value_added", "ai_resistance", "growth_coeff", "trend_5yr",
    ]
    # Deduplicate while preserving order
    seen = set()
    unique_cols = []
    for c in display_cols:
        if c not in seen and c in result.columns:
            seen.add(c)
            unique_cols.append(c)
    return result[unique_cols]

# Example: top_n(category="TECH", metric="ai_resistance", n=15, country="US")
'''))

    # Cell 5: country_overview
    nb.cells.append(new_code_cell('''def country_overview(iso_code):
    """Get an overview of a country\'s career landscape.

    Args:
        iso_code: Country ISO code (e.g. 'CN', 'US', 'JP')

    Returns:
        Summary statistics by major_category
    """
    result = df[df["iso_code"] == iso_code].copy()
    country_name = result["country_or_region"].iloc[0] if len(result) > 0 else iso_code

    print(f"=== {country_name} ({iso_code}) ===")
    print(f"Total occupations: {result['sub_category'].nunique()}")
    print(f"Total records: {len(result)}")
    print(f"Mean composite_index: {result['composite_index'].mean():.2f}")
    print(f"Mean ai_resistance: {result['ai_resistance'].mean():.2f}")
    print(f"Mean trend_2000_2026: {result['trend_2000_2026'].mean():.2f}")
    print()

    summary = result.groupby("major_category").agg(
        n=("sub_category", "nunique"),
        mean_composite=("composite_index", "mean"),
        mean_ai=("ai_resistance", "mean"),
        mean_growth=("growth_coeff", "mean"),
        mean_value=("value_added", "mean"),
        mean_trend=("trend_2000_2026", "mean"),
    ).round(2).sort_values("mean_composite", ascending=False)
    return summary

# Example: country_overview("CN")
'''))

    # Cell 6: transition_path
    nb.cells.append(new_code_cell('''def transition_path(from_occupation, target_category=None, country=None, top_n=10):
    """Suggest career transition paths from a given occupation.

    Finds occupations with high skill_versatility and career_switch scores
    in the target category, comparing key metrics.

    Args:
        from_occupation: Current sub_category name (Chinese)
        target_category: Target major_code (e.g. 'TECH'). None = all.
        country: Optional country filter (iso_code)
        top_n: Number of suggestions

    Returns:
        DataFrame with transition suggestions and score comparisons
    """
    # Get source occupation info
    source = df[df["sub_category"] == from_occupation]
    if country:
        source = source[source["iso_code"] == country]
    if len(source) == 0:
        print(f"Occupation '{from_occupation}' not found.")
        return pd.DataFrame()
    source_row = source.iloc[0]

    # Find target occupations
    targets = df.copy()
    if target_category:
        mask = (targets["major_category"] == target_category) | (targets["major_code"] == target_category)
        targets = targets[mask]
    if country:
        targets = targets[targets["iso_code"] == country]

    # Score transition viability
    targets = targets.copy()
    targets["transition_score"] = (
        targets["skill_versatility"] * 0.3 +
        targets["career_switch"] * 0.3 +
        targets["growth_coeff"] * 0.2 +
        targets["composite_index"] * 0.2
    ).round(2)

    targets = targets.nlargest(top_n, "transition_score")

    display_cols = [
        "sub_category", "sub_category_en", "country_or_region",
        "major_code", "transition_score", "skill_versatility",
        "career_switch", "composite_index", "growth_coeff",
        "value_added", "ai_resistance",
    ]
    result = targets[[c for c in display_cols if c in targets.columns]]

    print(f"From: {from_occupation} (composite={source_row['composite_index']:.2f}, "
          f"ai_resistance={source_row['ai_resistance']:.1f})")
    print(f"Suggested transitions ({top_n}):\\n")
    return result

# Example: transition_path("收银员", target_category="TECH", country="CN")
'''))

    # Cell 7: Usage examples
    nb.cells.append(new_markdown_cell(
        "## Usage Examples\n\n"
        "```python\n"
        "# Find high-paying, AI-resistant tech jobs in China\n"
        "find_jobs(country='CN', category='TECH', min_ai_resistance=7, min_salary=7)\n"
        "\n"
        "# Compare data scientist across countries\n"
        "compare('数据科学家')\n"
        "\n"
        "# Top 15 by cost_performance in the US\n"
        "top_n(metric='cost_performance', n=15, country='US')\n"
        "\n"
        "# Country overview for Japan\n"
        "country_overview('JP')\n"
        "\n"
        "# Career transition from cashier to tech\n"
        "transition_path('收银员', target_category='TECH', country='CN')\n"
        "```"
    ))

    _write_nb(nb, "74_query_tool.ipynb")


# ===================================================================
# Main
# ===================================================================
def main():
    print("Loading all data ...")
    df = load_all_data()
    print(f"  Total: {len(df)} rows, {df['sub_category'].nunique()} occupations, "
          f"{df['country_or_region'].nunique()} countries\n")

    print("=== Ranking Notebooks (13-17) ===")
    gen_nb13(df)
    gen_nb14(df)
    gen_nb15(df)
    gen_nb16(df)
    gen_nb17(df)

    print("\n=== Trend Notebooks (18-21) ===")
    gen_nb18(df)
    gen_nb19(df)
    gen_nb20(df)
    gen_nb21(df)

    print("\n=== Country Panorama Notebooks (22-66) ===")
    gen_country_notebooks(df)

    print("\n=== Special Topic Notebooks (67-73) ===")
    gen_nb67(df)
    gen_nb68(df)
    gen_nb69(df)
    gen_nb70(df)
    gen_nb71(df)
    gen_nb72(df)
    gen_nb73(df)

    print("\n=== Query Tool Notebook (74) ===")
    gen_nb74()

    print("\nDone! All notebooks generated.")


if __name__ == "__main__":
    main()
