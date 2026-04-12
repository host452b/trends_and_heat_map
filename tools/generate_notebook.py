"""Jupyter notebook generator for career development index data.

Creates .ipynb files with pandas styling (red-green heatmaps).
"""
import os
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from pathlib import Path

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

TREND_COLUMNS = ["trend_2000_2026", "trend_5yr"]


def create_data_notebook(csv_path, notebook_path, title="Data", description=""):
    """Create a 1:1 data notebook with red-green heatmap styling."""
    nb = new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }

    # Cell 1: Title
    md = f"# {title}\n"
    if description:
        md += f"\n{description}\n"
    md += "\n评分色阶：红色(低分0) → 黄色(中等5) → 绿色(高分10)  \n"
    md += "口碑方差：绿色(稳定0) → 红色(分化5)  \n"
    md += "趋势：红色(暴跌-5) → 白色(持平0) → 绿色(暴涨+5)"
    nb.cells.append(new_markdown_cell(md))

    # Cell 2: Imports + load data
    # Compute relative path from notebook to CSV
    nb_dir = Path(notebook_path).resolve().parent
    csv_abs = Path(csv_path).resolve()
    try:
        rel = os.path.relpath(csv_abs, nb_dir)
    except ValueError:
        rel = str(csv_abs)

    load_code = f"""import pandas as pd
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('{rel}')
print(f"记录数: {{len(df)}}")
print(f"国家/地区: {{df['country_or_region'].nunique() if 'country_or_region' in df.columns else 'N/A'}}")
print(f"职业细类: {{df['sub_category'].nunique() if 'sub_category' in df.columns else 'N/A'}}")
"""
    nb.cells.append(new_code_cell(load_code))

    # Cell 3: Styled full table
    score_cols_str = repr(SCORE_COLUMNS)
    trend_cols_str = repr(TREND_COLUMNS)

    style_code = f"""score_cols = {score_cols_str}
trend_cols = {trend_cols_str}

# Filter to columns that exist in this CSV
score_present = [c for c in score_cols if c in df.columns]
trend_present = [c for c in trend_cols if c in df.columns]

styled = df.style

# Score columns: red(0) → yellow(5) → green(10)
if score_present:
    non_var = [c for c in score_present if c != 'reputation_variance']
    if non_var:
        styled = styled.background_gradient(subset=non_var, cmap='RdYlGn', vmin=0, vmax=10)
    # Variance column: reversed (green=0=stable, red=5=polarized)
    if 'reputation_variance' in score_present:
        styled = styled.background_gradient(subset=['reputation_variance'], cmap='RdYlGn_r', vmin=0, vmax=5)

# Trend columns: red(-5) → white(0) → green(+5)
if trend_present:
    styled = styled.background_gradient(subset=trend_present, cmap='RdYlGn', vmin=-5, vmax=5)

# Composite index
if 'composite_index' in df.columns:
    styled = styled.background_gradient(subset=['composite_index'], cmap='RdYlGn', vmin=0, vmax=10)

styled.set_properties(**{{'font-size': '11px'}})
styled
"""
    nb.cells.append(new_code_cell(style_code))

    # Cell 4: Summary statistics
    summary_code = """# Summary statistics for score columns
if score_present:
    print("=== Score Summary ===")
    display(df[score_present].describe().round(2))
"""
    nb.cells.append(new_code_cell(summary_code))

    # Write notebook
    Path(notebook_path).parent.mkdir(parents=True, exist_ok=True)
    with open(notebook_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
