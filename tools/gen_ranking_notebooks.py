"""Generate 5 ranking notebooks (13-17) for the Global Career Development Index.

Each notebook loads ALL 12 CSV data files, concatenates them,
and produces styled rankings with red-green heatmaps.
"""

import os
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from pathlib import Path

# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
NB_DIR = ROOT / "notebooks"
CSV_DIR = ROOT / "data" / "csv"

# Key display columns (not all 58)
BASE_COLS = [
    "sub_category", "sub_category_en", "country_or_region",
    "major_category", "major_code", "region",
]

SCORE_COLUMNS = [
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_nb():
    """Return a fresh notebook with Python 3 kernel metadata."""
    nb = new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    return nb


def _loader_cell():
    """Code cell that loads all CSVs from data/csv/ and concatenates."""
    csv_rel = os.path.relpath(CSV_DIR, NB_DIR)
    return new_code_cell(f"""import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Heiti TC', 'Arial Unicode MS', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

from pathlib import Path

csv_dir = Path('{csv_rel}')
all_files = sorted(csv_dir.glob('*.csv'))
print(f"Loading {{len(all_files)}} CSV files ...")

dfs = []
for f in all_files:
    tmp = pd.read_csv(f)
    dfs.append(tmp)
    print(f"  {{f.name}}: {{len(tmp)}} rows")

df = pd.concat(dfs, ignore_index=True)
print(f"\\nTotal: {{len(df)}} rows, {{df['sub_category'].nunique()}} occupations, "
      f"{{df['country_or_region'].nunique()}} countries/regions")
""")


def _style_gradient(df_expr, score_cols, extra_gradient_cols=None):
    """Return code string that applies RdYlGn background gradient."""
    lines = [
        f"styled = {df_expr}.style \\",
    ]
    for col in (score_cols or []):
        if col == "reputation_variance":
            lines.append(f"    .background_gradient(subset=['{col}'], cmap='RdYlGn_r', vmin=0, vmax=5) \\")
        else:
            lines.append(f"    .background_gradient(subset=['{col}'], cmap='RdYlGn', vmin=0, vmax=10) \\")
    if extra_gradient_cols:
        for col in extra_gradient_cols:
            lines.append(f"    .background_gradient(subset=['{col}'], cmap='RdYlGn', vmin=0, vmax=10) \\")
    lines.append("    .set_properties(**{'font-size': '11px'})")
    lines.append("styled")
    return "\n".join(lines)


def _write_nb(nb, filename):
    """Write notebook to notebooks/ directory."""
    NB_DIR.mkdir(parents=True, exist_ok=True)
    path = NB_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"  Created {path}")


# ---------------------------------------------------------------------------
# Notebook 13: 综合发展指数 Top 100
# ---------------------------------------------------------------------------
def gen_nb13():
    nb = _make_nb()

    # Title
    nb.cells.append(new_markdown_cell(
        "# 综合发展指数 Top 100\n\n"
        "Global Career Development Composite Index — Top 100 occupations worldwide.\n\n"
        "评分色阶：红色(低分0) → 黄色(中等5) → 绿色(高分10)"
    ))

    # Load data
    nb.cells.append(_loader_cell())

    # Define display columns
    nb.cells.append(new_code_cell("""# Key columns to display
base_cols = ['sub_category', 'sub_category_en', 'country_or_region', 'major_category', 'major_code', 'region']
score_show = [
    'growth_coeff', 'opportunity', 'value_added', 'cost_performance',
    'ai_resistance', 'stability', 'developed_scarcity', 'intl_mobility',
    'remote_friendly', 'autonomy', 'fulfillment', 'composite_index',
]
display_cols = base_cols + score_show
"""))

    # Global Top 100
    nb.cells.append(new_markdown_cell("## Global Top 100 by Composite Index"))
    nb.cells.append(new_code_cell("""top100 = df.nlargest(100, 'composite_index')[display_cols].reset_index(drop=True)
top100.index = top100.index + 1
top100.index.name = 'Rank'

score_gradient_cols = [c for c in score_show if c in df.columns]
styled = top100.style \\
    .background_gradient(subset=score_gradient_cols, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Top 10 per major_category
    nb.cells.append(new_markdown_cell("## Top 10 per Major Category (大类)"))
    nb.cells.append(new_code_cell("""for cat in sorted(df['major_category'].unique()):
    sub = df[df['major_category'] == cat].nlargest(10, 'composite_index')[display_cols].reset_index(drop=True)
    sub.index = sub.index + 1
    sub.index.name = 'Rank'
    print(f"\\n{'='*60}")
    print(f"  {cat}")
    print(f"{'='*60}")
    styled = sub.style \\
        .background_gradient(subset=score_gradient_cols, cmap='RdYlGn', vmin=0, vmax=10) \\
        .set_properties(**{'font-size': '11px'})
    display(styled)
"""))

    # Top 10 per region
    nb.cells.append(new_markdown_cell("## Top 10 per Region (区域)"))
    nb.cells.append(new_code_cell("""for region in sorted(df['region'].unique()):
    sub = df[df['region'] == region].nlargest(10, 'composite_index')[display_cols].reset_index(drop=True)
    sub.index = sub.index + 1
    sub.index.name = 'Rank'
    print(f"\\n{'='*60}")
    print(f"  {region}")
    print(f"{'='*60}")
    styled = sub.style \\
        .background_gradient(subset=score_gradient_cols, cmap='RdYlGn', vmin=0, vmax=10) \\
        .set_properties(**{'font-size': '11px'})
    display(styled)
"""))

    # Bottom 50
    nb.cells.append(new_markdown_cell("## Bottom 50 (Lowest Composite Scores)"))
    nb.cells.append(new_code_cell("""bottom50 = df.nsmallest(50, 'composite_index')[display_cols].reset_index(drop=True)
bottom50.index = bottom50.index + 1
bottom50.index.name = 'Rank'

styled = bottom50.style \\
    .background_gradient(subset=score_gradient_cols, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    _write_nb(nb, "13_综合发展指数Top100.ipynb")


# ---------------------------------------------------------------------------
# Notebook 14: AI 抗性排行
# ---------------------------------------------------------------------------
def gen_nb14():
    nb = _make_nb()

    nb.cells.append(new_markdown_cell(
        "# AI 抗性排行\n\n"
        "AI Resistance Rankings — Which occupations are safest from automation?\n\n"
        "评分色阶：红色(低分0) → 黄色(中等5) → 绿色(高分10)"
    ))

    nb.cells.append(_loader_cell())

    nb.cells.append(new_code_cell("""# Key columns for AI analysis
base_cols = ['sub_category', 'sub_category_en', 'country_or_region', 'major_category', 'major_code', 'region']
ai_cols = ['ai_resistance', 'ai_timeline', 'value_added', 'growth_coeff',
           'skill_versatility', 'autonomy', 'physical_demand', 'composite_index']
display_cols = base_cols + ai_cols
"""))

    # Top 50 AI-resistant
    nb.cells.append(new_markdown_cell("## Top 50 Most AI-Resistant Occupations"))
    nb.cells.append(new_code_cell("""top50_resist = df.nlargest(50, 'ai_resistance')[display_cols].reset_index(drop=True)
top50_resist.index = top50_resist.index + 1
top50_resist.index.name = 'Rank'

score_gradient = [c for c in ai_cols if c not in ('ai_timeline',)]
styled = top50_resist.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Top 50 AI-vulnerable
    nb.cells.append(new_markdown_cell("## Top 50 Most AI-Vulnerable Occupations (Lowest AI Resistance)"))
    nb.cells.append(new_code_cell("""top50_vuln = df.nsmallest(50, 'ai_resistance')[display_cols].reset_index(drop=True)
top50_vuln.index = top50_vuln.index + 1
top50_vuln.index.name = 'Rank'

styled = top50_vuln.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # AI resistance by major_category
    nb.cells.append(new_markdown_cell(
        "## AI Resistance by Major Category\n\n"
        "Mean AI resistance score and distribution summary per category."
    ))
    nb.cells.append(new_code_cell("""cat_ai = df.groupby('major_category')['ai_resistance'].agg(['mean', 'median', 'std', 'min', 'max']).round(2)
cat_ai = cat_ai.sort_values('mean', ascending=False)
cat_ai.columns = ['Mean', 'Median', 'Std', 'Min', 'Max']

styled = cat_ai.style \\
    .background_gradient(subset=['Mean', 'Median'], cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '12px'})
styled
"""))

    # Box description text
    nb.cells.append(new_code_cell("""print("=== AI Resistance Distribution by Major Category ===\\n")
for cat in cat_ai.index:
    row = cat_ai.loc[cat]
    q1 = df[df['major_category'] == cat]['ai_resistance'].quantile(0.25)
    q3 = df[df['major_category'] == cat]['ai_resistance'].quantile(0.75)
    print(f"{cat}:")
    print(f"  Mean={row['Mean']:.2f}, Median={row['Median']:.2f}, Std={row['Std']:.2f}")
    print(f"  Range=[{row['Min']:.1f}, {row['Max']:.1f}], IQR=[{q1:.1f}, {q3:.1f}]")
    print()
"""))

    # AI timeline distribution
    nb.cells.append(new_markdown_cell("## AI Timeline Distribution\n\nWhen will AI significantly impact each occupation?"))
    nb.cells.append(new_code_cell("""timeline_counts = df['ai_timeline'].value_counts().sort_index()
print("AI Impact Timeline Distribution:\\n")
print(timeline_counts.to_string())
print(f"\\nTotal: {timeline_counts.sum()}")

fig, ax = plt.subplots(figsize=(10, 5))
timeline_counts.plot(kind='bar', ax=ax, color='steelblue', edgecolor='white')
ax.set_title('AI Impact Timeline Distribution', fontsize=14)
ax.set_xlabel('Timeline')
ax.set_ylabel('Number of Occupations')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
"""))

    # Scatter: ai_resistance vs value_added
    nb.cells.append(new_markdown_cell(
        "## AI Resistance vs Value Added\n\n"
        "Are AI-safe jobs also well-paid? Scatter plot of ai_resistance vs value_added."
    ))
    nb.cells.append(new_code_cell("""fig, ax = plt.subplots(figsize=(10, 8))

categories = df['major_category'].unique()
colors = plt.cm.tab20(range(len(categories)))

for cat, color in zip(sorted(categories), colors):
    sub = df[df['major_category'] == cat]
    ax.scatter(sub['ai_resistance'], sub['value_added'],
               alpha=0.4, s=15, label=cat, color=color)

ax.set_xlabel('AI Resistance', fontsize=12)
ax.set_ylabel('Value Added', fontsize=12)
ax.set_title('AI Resistance vs Value Added by Category', fontsize=14)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axhline(y=5, color='gray', linestyle='--', alpha=0.3)
ax.axvline(x=5, color='gray', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()

# Correlation
corr = df[['ai_resistance', 'value_added']].corr().iloc[0, 1]
print(f"\\nCorrelation between AI Resistance and Value Added: {corr:.3f}")
"""))

    _write_nb(nb, "14_AI抗性排行.ipynb")


# ---------------------------------------------------------------------------
# Notebook 15: 职业性价比排行
# ---------------------------------------------------------------------------
def gen_nb15():
    nb = _make_nb()

    nb.cells.append(new_markdown_cell(
        "# 职业性价比排行\n\n"
        "Cost-Performance Rankings — Best return on investment for career choices.\n\n"
        "评分色阶：红色(低分0) → 黄色(中等5) → 绿色(高分10)"
    ))

    nb.cells.append(_loader_cell())

    nb.cells.append(new_code_cell("""# Key columns for cost-performance analysis
base_cols = ['sub_category', 'sub_category_en', 'country_or_region', 'major_category', 'major_code', 'region']
cp_cols = ['cost_performance', 'learning_cost', 'education_req', 'value_added',
           'growth_coeff', 'opportunity', 'stability', 'composite_index']
display_cols = base_cols + cp_cols
"""))

    # Global Top 50 cost_performance
    nb.cells.append(new_markdown_cell("## Global Top 50 Highest Cost-Performance"))
    nb.cells.append(new_code_cell("""top50_cp = df.nlargest(50, 'cost_performance')[display_cols].reset_index(drop=True)
top50_cp.index = top50_cp.index + 1
top50_cp.index.name = 'Rank'

score_gradient = [c for c in cp_cols if c in df.columns]
styled = top50_cp.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Best cost_performance by education level
    nb.cells.append(new_markdown_cell("## Best Cost-Performance by Education Level (typical_education)"))
    nb.cells.append(new_code_cell("""edu_levels = sorted(df['typical_education'].dropna().unique())
print(f"Education levels found: {len(edu_levels)}\\n")

for edu in edu_levels:
    sub = df[df['typical_education'] == edu].nlargest(10, 'cost_performance')[display_cols].reset_index(drop=True)
    sub.index = sub.index + 1
    sub.index.name = 'Rank'
    print(f"\\n{'='*60}")
    print(f"  {edu} (n={len(df[df['typical_education'] == edu])})")
    print(f"{'='*60}")
    styled = sub.style \\
        .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
        .set_properties(**{'font-size': '11px'})
    display(styled)
"""))

    # Best cost_performance per country (Top 5)
    nb.cells.append(new_markdown_cell("## Best Cost-Performance per Country (Top 5 per Country)"))
    nb.cells.append(new_code_cell("""countries = sorted(df['country_or_region'].unique())
print(f"Countries/regions: {len(countries)}\\n")

for country in countries:
    sub = df[df['country_or_region'] == country].nlargest(5, 'cost_performance')[display_cols].reset_index(drop=True)
    sub.index = sub.index + 1
    sub.index.name = 'Rank'
    print(f"\\n{'='*60}")
    print(f"  {country}")
    print(f"{'='*60}")
    styled = sub.style \\
        .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
        .set_properties(**{'font-size': '11px'})
    display(styled)
"""))

    # Scatter: cost_performance vs learning_cost
    nb.cells.append(new_markdown_cell(
        "## Cost-Performance vs Learning Cost\n\n"
        "Do low-cost-to-learn occupations have the best returns?"
    ))
    nb.cells.append(new_code_cell("""fig, ax = plt.subplots(figsize=(10, 8))

categories = sorted(df['major_category'].unique())
colors = plt.cm.tab20(range(len(categories)))

for cat, color in zip(categories, colors):
    sub = df[df['major_category'] == cat]
    ax.scatter(sub['learning_cost'], sub['cost_performance'],
               alpha=0.4, s=15, label=cat, color=color)

ax.set_xlabel('Learning Cost (higher = more expensive)', fontsize=12)
ax.set_ylabel('Cost-Performance (higher = better value)', fontsize=12)
ax.set_title('Cost-Performance vs Learning Cost', fontsize=14)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
plt.tight_layout()
plt.show()

corr = df[['cost_performance', 'learning_cost']].corr().iloc[0, 1]
print(f"\\nCorrelation between Cost-Performance and Learning Cost: {corr:.3f}")
"""))

    _write_nb(nb, "15_性价比排行.ipynb")


# ---------------------------------------------------------------------------
# Notebook 16: 稀缺度与移民价值排行
# ---------------------------------------------------------------------------
def gen_nb16():
    nb = _make_nb()

    nb.cells.append(new_markdown_cell(
        "# 稀缺度与移民价值排行\n\n"
        "Scarcity & Immigration Value Rankings — "
        "Which occupations are most needed in developed countries and most internationally mobile?\n\n"
        "评分色阶：红色(低分0) → 黄色(中等5) → 绿色(高分10)"
    ))

    nb.cells.append(_loader_cell())

    nb.cells.append(new_code_cell("""# Key columns for scarcity / immigration analysis
base_cols = ['sub_category', 'sub_category_en', 'country_or_region', 'major_category', 'major_code', 'region']
imm_cols = ['developed_scarcity', 'intl_mobility', 'value_added', 'growth_coeff',
            'license_barrier', 'supply_demand', 'stability', 'composite_index']
display_cols = base_cols + imm_cols
"""))

    # Top 50 developed_scarcity
    nb.cells.append(new_markdown_cell("## Top 50 Most Scarce Occupations in Developed Countries"))
    nb.cells.append(new_code_cell("""top50_scarce = df.nlargest(50, 'developed_scarcity')[display_cols].reset_index(drop=True)
top50_scarce.index = top50_scarce.index + 1
top50_scarce.index.name = 'Rank'

score_gradient = [c for c in imm_cols if c in df.columns]
styled = top50_scarce.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Top 50 intl_mobility
    nb.cells.append(new_markdown_cell("## Top 50 Highest International Mobility"))
    nb.cells.append(new_code_cell("""top50_mobile = df.nlargest(50, 'intl_mobility')[display_cols].reset_index(drop=True)
top50_mobile.index = top50_mobile.index + 1
top50_mobile.index.name = 'Rank'

styled = top50_mobile.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Cross-tab: developed_scarcity by major_category x region
    nb.cells.append(new_markdown_cell(
        "## Cross-Tab: Developed Scarcity by Major Category x Region\n\n"
        "Mean developed_scarcity score for each combination."
    ))
    nb.cells.append(new_code_cell("""cross = pd.pivot_table(df, values='developed_scarcity',
                        index='major_category', columns='region',
                        aggfunc='mean').round(2)
cross = cross.fillna(0)

styled = cross.style \\
    .background_gradient(cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Immigration-valuable occupations
    nb.cells.append(new_markdown_cell(
        "## Immigration-Valuable Occupations\n\n"
        "Occupations with BOTH high developed_scarcity (>= 7) AND high intl_mobility (>= 7) — "
        "the best candidates for skilled immigration pathways."
    ))
    nb.cells.append(new_code_cell("""imm_valuable = df[(df['developed_scarcity'] >= 7) & (df['intl_mobility'] >= 7)].copy()
imm_valuable = imm_valuable.sort_values('developed_scarcity', ascending=False)

print(f"Found {len(imm_valuable)} occupation-country combinations meeting criteria "
      f"(developed_scarcity >= 7 AND intl_mobility >= 7)\\n")
print(f"Unique occupations: {imm_valuable['sub_category'].nunique()}")
print(f"Unique countries: {imm_valuable['country_or_region'].nunique()}")

imm_display = imm_valuable[display_cols].reset_index(drop=True)
imm_display.index = imm_display.index + 1
imm_display.index.name = 'Rank'

styled = imm_display.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Summary by major_category
    nb.cells.append(new_markdown_cell("## Immigration Value Summary by Major Category"))
    nb.cells.append(new_code_cell("""imm_summary = imm_valuable.groupby('major_category').agg(
    count=('sub_category', 'size'),
    unique_occupations=('sub_category', 'nunique'),
    avg_scarcity=('developed_scarcity', 'mean'),
    avg_mobility=('intl_mobility', 'mean'),
    avg_composite=('composite_index', 'mean'),
).round(2).sort_values('count', ascending=False)

styled = imm_summary.style \\
    .background_gradient(subset=['avg_scarcity', 'avg_mobility', 'avg_composite'], cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '12px'})
styled
"""))

    _write_nb(nb, "16_稀缺度与移民价值.ipynb")


# ---------------------------------------------------------------------------
# Notebook 17: 职业生活质量排行
# ---------------------------------------------------------------------------
def gen_nb17():
    nb = _make_nb()

    nb.cells.append(new_markdown_cell(
        "# 职业生活质量排行\n\n"
        "Quality of Life Rankings — Which occupations offer the best work-life balance?\n\n"
        "评分色阶：红色(低分0) → 黄色(中等5) → 绿色(高分10)\n\n"
        "**Note:** Higher burnout score = less burnout (better)."
    ))

    nb.cells.append(_loader_cell())

    nb.cells.append(new_code_cell("""# Key columns for quality-of-life analysis
base_cols = ['sub_category', 'sub_category_en', 'country_or_region', 'major_category', 'major_code', 'region']
qol_cols = ['remote_friendly', 'family_friendly', 'burnout', 'autonomy',
            'fulfillment', 'value_added', 'stability', 'composite_index']
display_cols = base_cols + qol_cols
score_gradient = [c for c in qol_cols if c in df.columns]
"""))

    # Top 50 remote_friendly
    nb.cells.append(new_markdown_cell("## Top 50 Most Remote-Friendly Occupations"))
    nb.cells.append(new_code_cell("""top50 = df.nlargest(50, 'remote_friendly')[display_cols].reset_index(drop=True)
top50.index = top50.index + 1
top50.index.name = 'Rank'

styled = top50.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Top 50 family_friendly
    nb.cells.append(new_markdown_cell("## Top 50 Most Family-Friendly Occupations"))
    nb.cells.append(new_code_cell("""top50 = df.nlargest(50, 'family_friendly')[display_cols].reset_index(drop=True)
top50.index = top50.index + 1
top50.index.name = 'Rank'

styled = top50.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Top 50 lowest burnout (highest burnout score)
    nb.cells.append(new_markdown_cell("## Top 50 Lowest Burnout (Highest Burnout Score = Least Burnout)"))
    nb.cells.append(new_code_cell("""top50 = df.nlargest(50, 'burnout')[display_cols].reset_index(drop=True)
top50.index = top50.index + 1
top50.index.name = 'Rank'

styled = top50.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Top 50 highest autonomy
    nb.cells.append(new_markdown_cell("## Top 50 Highest Autonomy"))
    nb.cells.append(new_code_cell("""top50 = df.nlargest(50, 'autonomy')[display_cols].reset_index(drop=True)
top50.index = top50.index + 1
top50.index.name = 'Rank'

styled = top50.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Top 50 highest fulfillment
    nb.cells.append(new_markdown_cell("## Top 50 Highest Fulfillment"))
    nb.cells.append(new_code_cell("""top50 = df.nlargest(50, 'fulfillment')[display_cols].reset_index(drop=True)
top50.index = top50.index + 1
top50.index.name = 'Rank'

styled = top50.style \\
    .background_gradient(subset=score_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Dream jobs composite
    nb.cells.append(new_markdown_cell(
        "## Dream Jobs Composite\n\n"
        "Average of (remote_friendly + family_friendly + burnout + autonomy + fulfillment) / 5.\n\n"
        "The ultimate work-life balance occupations."
    ))
    nb.cells.append(new_code_cell("""dream_components = ['remote_friendly', 'family_friendly', 'burnout', 'autonomy', 'fulfillment']
df['dream_score'] = df[dream_components].mean(axis=1).round(2)

dream_cols = base_cols + dream_components + ['dream_score', 'value_added', 'composite_index']
dream_gradient = dream_components + ['dream_score', 'value_added', 'composite_index']

top50_dream = df.nlargest(50, 'dream_score')[dream_cols].reset_index(drop=True)
top50_dream.index = top50_dream.index + 1
top50_dream.index.name = 'Rank'

styled = top50_dream.style \\
    .background_gradient(subset=dream_gradient, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '11px'})
styled
"""))

    # Dream score by category
    nb.cells.append(new_markdown_cell("## Dream Score by Major Category"))
    nb.cells.append(new_code_cell("""dream_by_cat = df.groupby('major_category').agg(
    avg_dream=('dream_score', 'mean'),
    avg_remote=('remote_friendly', 'mean'),
    avg_family=('family_friendly', 'mean'),
    avg_burnout=('burnout', 'mean'),
    avg_autonomy=('autonomy', 'mean'),
    avg_fulfillment=('fulfillment', 'mean'),
    avg_composite=('composite_index', 'mean'),
).round(2).sort_values('avg_dream', ascending=False)

score_cols = ['avg_dream', 'avg_remote', 'avg_family', 'avg_burnout',
              'avg_autonomy', 'avg_fulfillment', 'avg_composite']
styled = dream_by_cat.style \\
    .background_gradient(subset=score_cols, cmap='RdYlGn', vmin=0, vmax=10) \\
    .set_properties(**{'font-size': '12px'})
styled
"""))

    _write_nb(nb, "17_生活质量排行.ipynb")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Generating 5 ranking notebooks ...\n")
    gen_nb13()
    gen_nb14()
    gen_nb15()
    gen_nb16()
    gen_nb17()
    print("\nDone! All 5 notebooks generated.")


if __name__ == "__main__":
    main()
