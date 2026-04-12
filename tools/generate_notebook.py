"""Jupyter notebook generator for career development index data.

Creates .ipynb files with pre-rendered HTML tables (inline color styles)
so GitHub can display heatmaps without executing the notebook.
"""
import pandas as pd
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


def score_to_style(score, vmin=0, vmax=10):
    """Generate inline CSS background-color for a score."""
    ratio = max(0, min(1, (score - 3) / 7))
    if ratio < 0.5:
        r, g, b = 220, int(60 + ratio * 2 * 180), 60
    else:
        r, g, b = int(220 - (ratio - 0.5) * 2 * 180), 200, int(60 + (ratio - 0.5) * 2 * 40)
    return f"background-color: rgba({r},{g},{b}, 0.35)"


def variance_to_style(score):
    """Reversed color for reputation_variance: 0=green, 5=red."""
    inverted = 10 - score * 2  # map 0-5 to 10-0
    return score_to_style(inverted)


def trend_to_style(score):
    """Color for trend columns: -5=red, 0=neutral, +5=green."""
    mapped = (score + 5) / 10 * 10  # map -5..+5 to 0..10
    return score_to_style(mapped)


def _cell_style(col, value):
    """Return the inline style string for a given column and value."""
    try:
        v = float(value)
    except (ValueError, TypeError):
        return ""
    if col == "reputation_variance":
        return variance_to_style(v)
    if col in TREND_COLUMNS:
        return trend_to_style(v)
    if col == "composite_index" or col in SCORE_COLUMNS:
        return score_to_style(v)
    return ""


def render_html_table(df, page_size=60):
    """Render a DataFrame as a list of HTML table strings, one per page."""
    pages = []
    total_rows = len(df)
    columns = list(df.columns)

    for start in range(0, total_rows, page_size):
        end = min(start + page_size, total_rows)
        chunk = df.iloc[start:end]

        rows_html = []
        # Header row
        header_cells = []
        for col in columns:
            header_cells.append(
                f'<th style="border: 1px solid #ddd; padding: 4px 6px;">{col}</th>'
            )
        rows_html.append("<tr>" + "".join(header_cells) + "</tr>")

        # Data rows
        for _, row in chunk.iterrows():
            data_cells = []
            for col in columns:
                val = row[col]
                style = _cell_style(col, val)
                if style:
                    style_attr = f' style="border: 1px solid #ddd; padding: 4px 6px; {style}"'
                else:
                    style_attr = ' style="border: 1px solid #ddd; padding: 4px 6px;"'
                display_val = val if pd.notna(val) else ""
                data_cells.append(f"<td{style_attr}>{display_val}</td>")
            rows_html.append("<tr>" + "".join(data_cells) + "</tr>")

        html = (
            '<table style="border-collapse: collapse; font-size: 12px;">\n'
            + "\n".join(rows_html)
            + "\n</table>"
        )
        pages.append(html)

    return pages


def create_data_notebook(csv_path, notebook_path, title="Data", description=""):
    """Create a data notebook with pre-rendered HTML heatmap tables."""
    df = pd.read_csv(csv_path)

    nb = new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }

    # Cell 1: Markdown title
    md = f"# {title}\n"
    if description:
        md += f"\n{description}\n"
    md += "\n评分色阶：红色(低分0) → 黄色(中等5) → 绿色(高分10)  \n"
    md += "口碑方差：绿色(稳定0) → 红色(分化5)  \n"
    md += "趋势：红色(暴跌-5) → 白色(持平0) → 绿色(暴涨+5)"
    nb.cells.append(new_markdown_cell(md))

    # Cell 2: Record counts (pre-rendered text output)
    record_count = len(df)
    country_count = (
        df["country_or_region"].nunique()
        if "country_or_region" in df.columns
        else "N/A"
    )
    occupation_count = (
        df["sub_category"].nunique() if "sub_category" in df.columns else "N/A"
    )
    stats_text = (
        f"记录数: {record_count}\n"
        f"国家/地区: {country_count}\n"
        f"职业细类: {occupation_count}"
    )
    stats_cell = new_code_cell("# Dataset overview")
    stats_cell.outputs = [
        nbformat.v4.new_output(output_type="stream", name="stdout", text=stats_text)
    ]
    nb.cells.append(stats_cell)

    # Cells 3+: Paginated HTML tables
    pages = render_html_table(df, page_size=60)
    for i, html in enumerate(pages, 1):
        page_cell = new_code_cell(f"# Page {i} of {len(pages)}")
        page_cell.outputs = [
            nbformat.v4.new_output(
                output_type="display_data",
                data={"text/html": html},
            )
        ]
        nb.cells.append(page_cell)

    # Last cell: Summary statistics (pre-rendered text)
    score_present = [c for c in SCORE_COLUMNS if c in df.columns]
    if score_present:
        summary_lines = ["=== Score Summary ==="]
        desc = df[score_present].describe().round(2)
        summary_lines.append(desc.to_string())
        summary_text = "\n".join(summary_lines)
    else:
        summary_text = "No score columns found."

    summary_cell = new_code_cell("# Summary statistics")
    summary_cell.outputs = [
        nbformat.v4.new_output(
            output_type="stream", name="stdout", text=summary_text
        )
    ]
    nb.cells.append(summary_cell)

    # Write notebook
    Path(notebook_path).parent.mkdir(parents=True, exist_ok=True)
    with open(notebook_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
