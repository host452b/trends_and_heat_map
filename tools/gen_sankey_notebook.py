"""Generate a Jupyter notebook with 50-year career prediction Sankey diagrams.

Creates notebooks/75_50年职业变化预测_桑基图.ipynb with:
  - 4 Sankey diagrams (one per region: CN, Asia, Europe, Africa)
  - Narrative markdown cells per region with decade-by-decade analysis
  - Pre-rendered PNG images embedded as base64 for GitHub rendering

Requires: plotly, kaleido (with Chrome), pandas, nbformat
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import base64
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PRED_CSV = BASE_DIR / "data" / "csv" / "predictions_50yr.csv"
OUT_NB = BASE_DIR / "notebooks" / "75_50年职业变化预测_桑基图.ipynb"

DECADES = [2026, 2035, 2045, 2055, 2065, 2076]
DECADE_LABELS = ["2026", "2035", "2045", "2055", "2065", "2076"]

CATEGORY_ORDER = [
    "TECH", "MED", "FIN", "EDU", "ENG", "GOV",
    "LAW", "ART", "TRA", "SKL", "SVC", "AGR",
]

CATEGORY_ZH_SHORT = {
    "TECH": "IT/数字", "MED": "医疗", "FIN": "金融",
    "EDU": "教育", "ENG": "工程", "GOV": "公务",
    "LAW": "法律", "ART": "文艺", "TRA": "交通",
    "SKL": "技工", "SVC": "服务", "AGR": "农业",
}

# Distinct colors for 12 categories
CATEGORY_COLORS = {
    "TECH": "#4285F4",  # Google Blue
    "MED":  "#EA4335",  # Red
    "FIN":  "#FBBC04",  # Yellow/Gold
    "EDU":  "#34A853",  # Green
    "ENG":  "#FF6D01",  # Orange
    "GOV":  "#46BDC6",  # Teal
    "LAW":  "#7B61FF",  # Purple
    "ART":  "#FF4081",  # Pink
    "TRA":  "#795548",  # Brown
    "SKL":  "#607D8B",  # Blue Grey
    "SVC":  "#00BCD4",  # Cyan
    "AGR":  "#8BC34A",  # Light Green
}


def _hex_to_rgba(hex_color, alpha=0.4):
    """Convert hex color to rgba string."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def build_sankey_data(pred_df, region_zh):
    """Build Sankey node/link data for a given region.

    Returns (node_labels, node_colors, node_x, node_y, sources, targets, values, link_colors).

    Node layout: 6 columns (decades) x 12 rows (categories).
    Node index = decade_idx * 12 + category_idx.

    Links: For each transition (decade_i -> decade_i+1):
      - Each source category sends flow to target categories
      - Self-flow (same category) = min(source_share, target_share)
      - Surplus is redistributed to growing categories proportionally
    """
    region_data = pred_df[pred_df["region"] == region_zh].copy()

    # Build a lookup: (decade, major_code) -> recommendation_share
    share_lookup = {}
    for _, row in region_data.iterrows():
        share_lookup[(row["decade"], row["major_code"])] = row["recommendation_share"]

    # Sort categories by average share descending so largest appear first
    avg_shares = {}
    for cat in CATEGORY_ORDER:
        total = sum(share_lookup.get((d, cat), 0) for d in DECADES)
        avg_shares[cat] = total / len(DECADES)
    CATEGORY_ORDER_BY_SIZE = sorted(CATEGORY_ORDER, key=lambda c: avg_shares[c], reverse=True)

    n_cats = len(CATEGORY_ORDER)
    n_decades = len(DECADES)

    # Node labels, colors, positions
    node_labels = []
    node_colors = []
    node_x = []
    node_y = []

    # We need to map (decade_idx, cat) -> node_index for link building
    node_index_map = {}

    def clamp(v):
        return max(0.001, min(0.999, v))

    for d_idx, decade in enumerate(DECADES):
        x_pos = d_idx / max(1, n_decades - 1)
        # Stack categories by their share (proportional y-positions)
        cumulative = 0.0
        for cat in CATEGORY_ORDER_BY_SIZE:
            share = share_lookup.get((decade, cat), 0)
            y_center = (cumulative + share / 2) / 100.0
            cumulative += share

            node_idx = len(node_labels)
            node_index_map[(d_idx, cat)] = node_idx

            label = f"{CATEGORY_ZH_SHORT[cat]} {share:.1f}%"
            node_labels.append(label)
            node_colors.append(CATEGORY_COLORS[cat])
            node_x.append(clamp(x_pos))
            node_y.append(clamp(y_center))

    # Scale factor: multiply all values by 10 so plotly renders thicker links
    SCALE = 10

    # Links between consecutive decades
    sources = []
    targets = []
    values = []
    link_colors = []

    for d_idx in range(n_decades - 1):
        decade_from = DECADES[d_idx]
        decade_to = DECADES[d_idx + 1]

        # Get shares for this transition
        shares_from = {}
        shares_to = {}
        for cat in CATEGORY_ORDER:
            shares_from[cat] = share_lookup.get((decade_from, cat), 0)
            shares_to[cat] = share_lookup.get((decade_to, cat), 0)

        # For each source category, compute flows to target categories
        # Method: each category retains what it can (self-flow),
        # and any decrease is redistributed to growing categories
        for src_cat in CATEGORY_ORDER:
            src_share = shares_from[src_cat]
            if src_share <= 0.01:
                continue

            src_node = node_index_map[(d_idx, src_cat)]
            tgt_share = shares_to[src_cat]

            # Self-flow: minimum of source and target share
            self_flow = min(src_share, tgt_share)

            # Surplus to redistribute (if source > target)
            surplus = max(0, src_share - tgt_share)

            # Add self-flow (more opaque — continuity)
            if self_flow > 0.01:
                tgt_node = node_index_map[(d_idx + 1, src_cat)]
                sources.append(src_node)
                targets.append(tgt_node)
                values.append(round(self_flow * SCALE, 3))
                link_colors.append(_hex_to_rgba(CATEGORY_COLORS[src_cat], 0.5))

            # Distribute surplus to growing categories (less opaque — shift)
            if surplus > 0.01:
                # Find categories that grew (target > source)
                growers = {}
                total_growth = 0
                for tgt_cat in CATEGORY_ORDER:
                    if tgt_cat == src_cat:
                        continue
                    growth = shares_to[tgt_cat] - shares_from[tgt_cat]
                    if growth > 0:
                        growers[tgt_cat] = growth
                        total_growth += growth

                if total_growth > 0:
                    for tgt_cat, growth in growers.items():
                        flow = surplus * (growth / total_growth)
                        if flow > 0.01:
                            tgt_node = node_index_map[(d_idx + 1, tgt_cat)]
                            sources.append(src_node)
                            targets.append(tgt_node)
                            values.append(round(flow * SCALE, 3))
                            link_colors.append(_hex_to_rgba(CATEGORY_COLORS[src_cat], 0.15))
                else:
                    # No growers: add surplus as self-flow
                    tgt_node = node_index_map[(d_idx + 1, src_cat)]
                    # Find existing self-flow and add to it
                    found = False
                    for i in range(len(sources) - 1, -1, -1):
                        if sources[i] == src_node and targets[i] == tgt_node:
                            values[i] += round(surplus * SCALE, 3)
                            found = True
                            break
                    if not found:
                        sources.append(src_node)
                        targets.append(tgt_node)
                        values.append(round(surplus * SCALE, 3))
                        link_colors.append(_hex_to_rgba(CATEGORY_COLORS[src_cat], 0.5))

    return (node_labels, node_colors, node_x, node_y,
            sources, targets, values, link_colors)


def create_sankey_figure(pred_df, region_zh, title):
    """Create a plotly Sankey figure for a region."""
    (node_labels, node_colors, node_x, node_y,
     sources, targets, values, link_colors) = build_sankey_data(pred_df, region_zh)

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=18,
            thickness=28,
            line=dict(color="rgba(0,0,0,0.3)", width=0.5),
            label=node_labels,
            color=node_colors,
            x=node_x,
            y=node_y,
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
        ),
    )])

    # Add decade labels as annotations
    for d_idx, label in enumerate(DECADE_LABELS):
        x_pos = d_idx / max(1, len(DECADES) - 1)
        fig.add_annotation(
            x=x_pos,
            y=1.08,
            text=f"<b>{label}</b>",
            showarrow=False,
            font=dict(size=14, color="#333"),
            xref="paper",
            yref="paper",
        )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18),
            x=0.5,
            xanchor="center",
        ),
        font=dict(size=10, family="Arial, sans-serif"),
        width=1800,
        height=1100,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return fig


def fig_to_base64_html(fig):
    """Convert plotly figure to base64-encoded PNG wrapped in HTML img tag."""
    img_bytes = pio.to_image(fig, format="png", width=1800, height=1100, scale=2)
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    return f'<img src="data:image/png;base64,{img_b64}" style="max-width: 100%;" />'


def build_narrative_md(pred_df, region_zh, region_en):
    """Build a markdown narrative for a region."""
    region_data = pred_df[pred_df["region"] == region_zh].copy()

    lines = [f"### {region_zh} ({region_en}) 50年职业推荐指数演变", ""]

    for d_idx in range(len(DECADES)):
        decade = DECADES[d_idx]
        dec_data = region_data[region_data["decade"] == decade].sort_values(
            "recommendation_index", ascending=False
        )

        if d_idx == 0:
            lines.append(f"**{decade} (基线)**")
        elif d_idx < len(DECADES) - 1:
            prev = DECADES[d_idx - 1]
            lines.append(f"**{prev} → {decade}**")
        else:
            prev = DECADES[d_idx - 1]
            lines.append(f"**{prev} → {decade}**")

        # Top 3 and bottom 3
        top3 = dec_data.head(3)
        bot3 = dec_data.tail(3)

        lines.append("")
        for _, row in top3.iterrows():
            change_str = f" ({row['change_vs_2026']:+.2f})" if row['change_vs_2026'] != 0 else ""
            lines.append(
                f"> **{row['major_category']}** ({row['major_code']}): "
                f"推荐指数 {row['recommendation_index']:.2f}{change_str} | "
                f"占比 {row['recommendation_share']:.1f}%  "
            )
            if row["narrative_zh"]:
                lines.append(f"> _{row['narrative_zh']}_  ")
            lines.append(">")

        # Key narrative bullets
        narr_rows = dec_data[dec_data["narrative_zh"] != ""]
        if len(narr_rows) > 3:
            lines.append("")
            lines.append("要点：")
            # Biggest gainer
            if decade > 2026:
                gainer = dec_data.nlargest(1, "change_vs_2026").iloc[0]
                loser = dec_data.nsmallest(1, "change_vs_2026").iloc[0]
                lines.append(
                    f"- 最大赢家: {gainer['major_category']} "
                    f"(vs 2026: {gainer['change_vs_2026']:+.2f})"
                )
                lines.append(
                    f"- 最大输家: {loser['major_category']} "
                    f"(vs 2026: {loser['change_vs_2026']:+.2f})"
                )

        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    print("Loading prediction data...")
    pred_df = pd.read_csv(PRED_CSV)
    print(f"  Loaded {len(pred_df)} rows")

    nb = new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }

    # Title cell
    title_md = """# 50年职业变化预测 — 桑基图 (2026-2076)

## Global Career Development Index: 50-Year Career Prediction Sankey Diagrams

本笔记本展示4个宏观区域（中国、亚洲、欧洲、非洲）在2026-2076年间，
12大职业门类的推荐指数演变趋势。

桑基图（Sankey Diagram）展示了各职业门类的推荐比重如何在50年间发生转移：
- **节点宽度** = 该门类推荐指数占比（%）
- **连线** = 推荐比重的延续与转移
- **颜色** = 职业门类

### 职业门类色标

| 代码 | 门类 | 颜色 |
|------|------|------|
| TECH | 信息技术与数字化 | 🔵 蓝色 |
| MED  | 医疗与健康 | 🔴 红色 |
| FIN  | 金融与商业 | 🟡 金色 |
| EDU  | 教育与学术 | 🟢 绿色 |
| ENG  | 工程与制造 | 🟠 橙色 |
| GOV  | 公共管理与公务员 | 🟦 青色 |
| LAW  | 法律与社会服务 | 🟣 紫色 |
| ART  | 文化、艺术与传媒 | 🩷 粉色 |
| TRA  | 交通运输与物流 | 🟤 棕色 |
| SKL  | 技术工种与手工业 | ⬜ 蓝灰 |
| SVC  | 服务业与消费 | 🔷 青绿 |
| AGR  | 农业、资源与环境 | 🥬 浅绿 |

### 预测模型说明

预测基于以下因素综合计算：
1. **2026基线**：54,000条现有数据的composite_index均值
2. **AI冲击衰减**：低AI抗性职业随时间推移推荐指数下降
3. **趋势外推**：2000-2026历史趋势带阻尼延伸
4. **结构性转型**：分区域的产业转型因子（老龄化/绿色转型/数字化等）
"""
    nb.cells.append(new_markdown_cell(title_md))

    # Region configs
    regions = [
        ("中国", "China", "中国 50年职业推荐演变 (2026-2076)"),
        ("亚洲", "Asia (East+SE+South+Central-West)", "亚洲 50年职业推荐演变 (2026-2076)"),
        ("欧洲", "Europe (West+North+South+East)", "欧洲 50年职业推荐演变 (2026-2076)"),
        ("非洲", "Africa (ZA+NG+KE+EG)", "非洲 50年职业推荐演变 (2026-2076)"),
    ]

    for region_zh, region_en, title in regions:
        print(f"  Generating Sankey for {region_zh}...")

        # Markdown separator
        nb.cells.append(new_markdown_cell(f"---\n\n## {title}"))

        # Generate Sankey figure and embed as image
        fig = create_sankey_figure(pred_df, region_zh, title)
        html_img = fig_to_base64_html(fig)

        # Create code cell with pre-rendered output
        code_cell = new_code_cell(
            f"# {title}\n"
            f"# Sankey diagram: recommendation share flow across 6 decades\n"
            f"# (pre-rendered as static image for GitHub compatibility)"
        )
        code_cell.outputs = [
            nbformat.v4.new_output(
                output_type="display_data",
                data={"text/html": html_img},
            )
        ]
        nb.cells.append(code_cell)

        # Add narrative markdown
        narrative = build_narrative_md(pred_df, region_zh, region_en)
        nb.cells.append(new_markdown_cell(narrative))

    # Summary comparison cell
    summary_md = """---

## 四大区域对比总结

### 共同趋势
1. **医疗健康**在所有区域均为长期赢家，老龄化是全球性趋势
2. **信息技术**短期（2026-2035）强势增长，长期（2045+）趋于平稳
3. **交通运输**因自动驾驶在所有区域均大幅下降
4. **服务业**在所有区域长期增长，护理经济+体验经济驱动
5. **公共管理**在所有区域趋于缩减，AI替代行政功能

### 区域差异
| 趋势 | 中国 | 亚洲 | 欧洲 | 非洲 |
|------|------|------|------|------|
| 最强增长 | 医疗+服务 | 科技+医疗 | 医疗+技工 | 科技+教育 |
| 最大衰退 | 交通+公务 | 交通+公务 | 交通+公务 | 交通(较慢)+公务 |
| 转型节奏 | 最快(2035已显著) | 快(2035-2045) | 渐进(2035-2055) | 最慢(2045-2065) |
| 特色 | AI/半导体→老龄化 | 制造→数字化 | 绿色转型+老龄化 | 基建+教育扩张 |
| 技工趋势 | 稀缺→精英化 | 短缺但改善 | 极度稀缺→高薪 | 需求旺盛→高端化 |

### 方法论说明
- 推荐指数 = composite_index基线 - AI冲击衰减 + 趋势外推 + 结构性因子
- 占比 = 各门类推荐指数 / 该区域×年代总推荐指数 × 100%
- 预测为基于当前数据的模型推演，非精确预测，仅供趋势参考
"""
    nb.cells.append(new_markdown_cell(summary_md))

    # Write notebook
    OUT_NB.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_NB, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"  Saved notebook to {OUT_NB}")


if __name__ == "__main__":
    main()
