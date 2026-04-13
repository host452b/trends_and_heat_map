# 数据维护流程 (Flow)

## 时间元数据（AI Agent 必读）

每条数据记录包含 3 个时间标记列，用于判断数据新鲜度和触发更新：

| 列 | 含义 | 示例 | AI Agent 用途 |
|----|------|------|-------------|
| `generated_date` | 该行数据的生成日期 | 2026-04-13 | 判断数据年龄，超过 6 个月应触发校准 |
| `data_snapshot_date` | 评分基于此日期的市场状态 | 2026-04-13 | 与当前日期比较，判断是否需要刷新 |
| `source_period` | 数据源覆盖的时间跨度 | 2000-2026 | 理解趋势列(trend_2000_2026)的含义 |

### 数据源锚点截止日期

| 数据源 | 最新数据截止 | 下次预期更新 |
|--------|------------|------------|
| ILO ILOSTAT | 2025-Q4 | 2026-Q2 |
| OECD Employment Outlook | 2025 | 2026-07 |
| O*NET | 2025.1 | 2026-01 |
| WEF Future of Jobs | 2025 | 2027 |
| McKinsey MGI | 2025 | 持续 |
| Glassdoor / Indeed | 实时 | 持续 |
| LinkedIn Economic Graph | 实时 | 持续 |

### AI Agent 更新决策规则

```
IF current_date - data_snapshot_date > 180 days:
    → 触发"校准数据"流程
    → 重点校准: 实时数据源(Glassdoor/LinkedIn/Indeed)
    → 更新 generated_date 和 data_snapshot_date

IF current_date - data_snapshot_date > 365 days:
    → 触发"全量校准"流程
    → 所有数据源重新校准
    → 检查 source_period 是否需要扩展(如 2000-2027)

IF 新的 WEF/OECD/ILO 年度报告发布:
    → 触发"锚点更新"流程
    → 用新报告数据重新校准相关维度
    → 更新 source_anchors 截止日期
```

## 扩展数据
1. 新职业 → 先更新 schema/categories.yaml
2. 每条记录必须包含 61 列完整数据（58 原始列 + 3 时间元数据列）
3. 评分 0-10 统一制，综合加权按 weights.yaml 计算
4. 时间列必填：generated_date=当天, data_snapshot_date=当天, source_period=覆盖范围
5. 用 tools/validate_data.py 验证后再提交

## 校准数据
1. O*NET → 校准美国职业评分
2. ILO ILOSTAT → 校准全球就业/安全/工时
3. OECD → 校准发达国家数据
4. Glassdoor/LinkedIn → 校准口碑和供需
5. 实际薪资数据 → 校准附加值
6. 校准后更新 data_snapshot_date 为当天
7. 如果锚点数据源更新，同步更新 schema/SCHEMA.yaml 中的 source_anchors

## 生成产出
1. 每个 CSV 对应一个 .ipynb (红绿色阶完整数据)
2. JSON 镜像: `from tools.csv_to_json import convert_csv_to_json`
3. Notebook: `from tools.generate_notebook import create_data_notebook`
4. 总表: 重新运行聚合脚本更新 00_all_occupations*.csv
5. README 含完整权重表和列说明
6. CHANGELOG.md 记录每次更新

## 61 列统一结构
id/大类/代码/中类/细类/英文/ISCO/O*NET/区域/国家/ISO/类型/雇主/学历/年龄/地区性
34 个评分维度
趋势(2)/需求方向/AI时间线/综合指数/摘要中/摘要英/来源
**generated_date/data_snapshot_date/source_period**
