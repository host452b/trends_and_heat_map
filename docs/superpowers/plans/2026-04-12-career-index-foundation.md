# Career Index Foundation & Tooling — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete infrastructure, Python tooling, and TECH pilot for the Global Career Development Index — validating the entire pipeline end-to-end before scaling to all 12 categories.

**Architecture:** YAML schemas define the data contract. Python utilities (score calculator, validator, JSON converter, notebook generator) form a reusable pipeline. The TECH category serves as the pilot: complete data for ~35 occupations × 45 countries, validated and rendered as notebook with red-green heatmaps.

**Tech Stack:** Python 3.10+, pandas, pyyaml, nbformat, jupyter, pytest

---

## Scope Note

This is **Plan 1 of 13** for the Global Career Development Index project.

| Plan | Scope | Depends On |
|------|-------|-----------|
| **1 (this)** | Foundation + Tooling + TECH pilot | — |
| 2-12 | Data generation, one per remaining category | Plan 1 |
| 13 | Rankings, trends, country panoramas, special topic notebooks | Plans 1-12 |

**Design spec:** `docs/superpowers/specs/2026-04-12-global-career-development-index-design.md`

---

## File Structure

Files created or modified in this plan:

```
trends_and_heat_map/
├── requirements.txt                          [CREATE]
├── README.md                                 [CREATE]
├── README_EN.md                              [CREATE]
├── FLOW.md                                   [CREATE]
├── CHANGELOG.md                              [CREATE]
├── schema/
│   ├── weights.yaml                          [CREATE]
│   ├── SCHEMA.yaml                           [CREATE]
│   └── categories.yaml                       [CREATE]
├── mapping/
│   └── country_meta.csv                      [CREATE]
├── data/
│   ├── csv/
│   │   └── tech_digital.csv                  [CREATE] (pilot)
│   └── json/
│       ├── tech_digital.json                 [CREATE]
│       └── meta/
│           ├── schema.json                   [CREATE]
│           ├── categories.json               [CREATE]
│           ├── countries.json                 [CREATE]
│           └── weights.json                  [CREATE]
├── tools/
│   ├── __init__.py                           [CREATE]
│   ├── score_calculator.py                   [CREATE]
│   ├── validate_data.py                      [CREATE]
│   ├── csv_to_json.py                        [CREATE]
│   └── generate_notebook.py                  [CREATE]
├── tests/
│   ├── __init__.py                           [CREATE]
│   ├── conftest.py                           [CREATE]
│   ├── test_score_calculator.py              [CREATE]
│   ├── test_validate_data.py                 [CREATE]
│   ├── test_csv_to_json.py                   [CREATE]
│   └── test_generate_notebook.py             [CREATE]
├── notebooks/
│   ├── 00_数据总览.ipynb                      [CREATE]
│   └── 01_tech_digital.ipynb                 [CREATE] (pilot)
└── archive/                                  [CREATE] (empty)
```

---

## Task 1: Project Scaffold & Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `tools/__init__.py`
- Create: `tests/__init__.py`
- Create: all directories

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p schema mapping data/csv data/json/meta tools tests notebooks archive
```

- [ ] **Step 2: Create requirements.txt**

```
pandas>=2.0.0
pyyaml>=6.0
nbformat>=5.9.0
jupyter>=1.0.0
nbconvert>=7.0.0
pytest>=7.0.0
openpyxl>=3.1.0
Jinja2>=3.1.0
```

- [ ] **Step 3: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: All packages install successfully.

- [ ] **Step 4: Create package init files**

Create `tools/__init__.py` — empty file.
Create `tests/__init__.py` — empty file.

- [ ] **Step 5: Commit scaffold**

```bash
git add requirements.txt tools/__init__.py tests/__init__.py
git commit -m "feat: project scaffold and dependencies"
```

---

## Task 2: Schema — weights.yaml

**Files:**
- Create: `schema/weights.yaml`

- [ ] **Step 1: Write weights.yaml**

```yaml
# Global Career Development Index — Weight Configuration
# All weights sum to 100%. Used by tools/score_calculator.py.

categories:
  入门门槛: 6
  发展空间: 10
  市场面: 10
  收入与回报: 9
  稳定与风险: 15
  口碑与转型: 9
  未来: 6
  生活质量: 15
  结构性与灵活性: 20

weights:
  # 入门门槛 (6%)
  learning_cost: 3
  education_req: 3
  # 发展空间 (10%)
  growth_coeff: 4
  career_lifespan: 3
  opportunity: 3
  # 市场面 (10%)
  market_size: 2
  supply_demand: 4
  developed_scarcity: 4
  # 收入与回报 (9%)
  value_added: 5
  cost_performance: 4
  # 稳定与风险 (15%)
  stability: 4
  safety: 3
  occupational_disease: 2
  overtime: 3
  burnout: 3
  # 口碑与转型 (9%)
  skill_versatility: 3
  career_switch: 3
  reputation_variance: 3
  # 未来 (6%)
  ai_resistance: 6
  # 生活质量 (15%)
  social_status: 3
  remote_friendly: 3
  autonomy: 3
  family_friendly: 3
  fulfillment: 3
  # 结构性与灵活性 (20%)
  entrepreneurship: 2
  gender_equality: 2
  age_flexibility: 2
  social_interaction: 2
  physical_demand: 1
  license_barrier: 2
  cycle_sensitivity: 2
  side_job_compat: 2
  intl_mobility: 3
  industry_monopoly: 2

# Reverse dimensions: higher raw value = worse for the individual.
# These are inverted (10 - raw) before weighting so all dimensions
# are "higher = better" in the composite index.
reverse_dimensions:
  - learning_cost
  - education_req
  - physical_demand
  - license_barrier
  - cycle_sensitivity
  - industry_monopoly

# Special case: reputation_variance is 0-5 scale.
# Normalized to 0-10 then reversed: (5 - raw) * 2
special_normalization:
  reputation_variance:
    raw_range: [0, 5]
    direction: reverse
```

- [ ] **Step 2: Validate weights sum to 100**

Run: `python3 -c "import yaml; d=yaml.safe_load(open('schema/weights.yaml')); print('Sum:', sum(d['weights'].values())); assert sum(d['weights'].values()) == 100"`
Expected: `Sum: 100`

- [ ] **Step 3: Commit**

```bash
git add schema/weights.yaml
git commit -m "feat: add weights.yaml — 34 dimensions, 9 categories, 100%"
```

---

## Task 3: Schema — SCHEMA.yaml

**Files:**
- Create: `schema/SCHEMA.yaml`

- [ ] **Step 1: Write SCHEMA.yaml**

```yaml
# Global Career Development Index — Column Schema
# Defines all 58 columns: name, type, range, description (zh/en), source.

dataset:
  name: "Global Career Development Index"
  name_zh: "全球职业发展指数"
  version: "1.0.0"
  score_range: [0, 10]
  total_columns: 58

columns:
  # === Basic Info (15 columns) ===
  id:
    index: 1
    type: string
    pattern: "{MAJOR}-{MMSS}-{ISO}-{EMPLOYER}"
    description_zh: "唯一标识符"
    description_en: "Unique identifier"
  major_category:
    index: 2
    type: string
    description_zh: "职业大类(中文)"
    description_en: "Major category"
  major_code:
    index: 3
    type: string
    enum: [TECH, MED, FIN, EDU, ENG, GOV, LAW, ART, TRA, SKL, SVC, AGR]
    description_zh: "大类代码"
    description_en: "Major category code"
  mid_category:
    index: 4
    type: string
    description_zh: "中类(中文)"
    description_en: "Mid-level category"
  sub_category:
    index: 5
    type: string
    description_zh: "细类(中文)"
    description_en: "Subcategory / specific occupation"
  sub_category_en:
    index: 6
    type: string
    description_zh: "细类(英文)"
    description_en: "Subcategory in English"
  isco_code:
    index: 7
    type: string
    nullable: true
    description_zh: "ISCO-08编码"
    description_en: "ISCO-08 code"
  onet_code:
    index: 8
    type: string
    nullable: true
    description_zh: "O*NET SOC编码"
    description_en: "O*NET SOC code"
  region:
    index: 9
    type: string
    description_zh: "地理区域"
    description_en: "Geographic region"
  country_or_region:
    index: 10
    type: string
    description_zh: "国家或地区"
    description_en: "Country or region"
  iso_code:
    index: 11
    type: string
    description_zh: "ISO 3166-1 alpha-2 代码"
    description_en: "ISO country/region code"
  type:
    index: 12
    type: string
    enum: [country, region]
    description_zh: "国家或地区类型"
    description_en: "Entity type"
  employer_type:
    index: 13
    type: string
    enum: [general, state_monopoly, state_owned, private_large, private_sme, startup, freelance]
    description_zh: "雇主类型"
    description_en: "Employer type"
  typical_education:
    index: 14
    type: string
    description_zh: "典型学历要求"
    description_en: "Typical education requirement"
  typical_entry_age:
    index: 15
    type: string
    description_zh: "典型入行年龄"
    description_en: "Typical entry age range"

  # === Locality Tag (1 column) ===
  locality:
    index: 16
    type: string
    enum: [global, regional, country_specific]
    description_zh: "职业地区性"
    description_en: "Occupation locality scope"

  # === Score Dimensions (34 columns, indices 17-50) ===
  # 入门门槛
  learning_cost:
    index: 17
    type: float
    range: [0, 10]
    weight: 3
    category: "入门门槛"
    reverse: true
    description_zh: "前置学习成本(0=无需培训, 10=10年+专业训练)"
    description_en: "Pre-career learning investment"
    source: "O*NET Education/Training, national qualification frameworks"
  education_req:
    index: 18
    type: float
    range: [0, 10]
    weight: 3
    category: "入门门槛"
    reverse: true
    description_zh: "学历要求(0=无要求, 10=博士必需)"
    description_en: "Education requirement level"
    source: "O*NET, ILO ISCED mapping"
  # 发展空间
  growth_coeff:
    index: 19
    type: float
    range: [0, 10]
    weight: 4
    category: "发展空间"
    description_zh: "职业成长系数(0=无晋升, 10=指数成长)"
    description_en: "Career growth coefficient"
    source: "LinkedIn Career Path, Glassdoor"
  career_lifespan:
    index: 20
    type: float
    range: [0, 10]
    weight: 3
    category: "发展空间"
    description_zh: "职业寿命(0=<5年淘汰, 10=越老越值钱)"
    description_en: "Career lifespan"
    source: "ILO age-employment stats, OECD Aging"
  opportunity:
    index: 21
    type: float
    range: [0, 10]
    weight: 3
    category: "发展空间"
    description_zh: "职业机遇(0=夕阳, 10=风口爆发)"
    description_en: "Career opportunity / momentum"
    source: "WEF Future of Jobs, McKinsey MGI"
  # 市场面
  market_size:
    index: 22
    type: float
    range: [0, 10]
    weight: 2
    category: "市场面"
    description_zh: "职业市场大小(0=极小众, 10=全球千万级)"
    description_en: "Market size"
    source: "ILO ILOSTAT, national labor statistics"
  supply_demand:
    index: 23
    type: float
    range: [0, 10]
    weight: 4
    category: "市场面"
    description_zh: "供需关系(0=严重过剩, 10=严重供不应求)"
    description_en: "Supply-demand balance"
    source: "Indeed/LinkedIn talent insights, OECD Skills for Jobs"
  developed_scarcity:
    index: 24
    type: float
    range: [0, 10]
    weight: 4
    category: "市场面"
    description_zh: "发达国家稀缺度(0=不缺, 10=移民快通道)"
    description_en: "Scarcity in developed countries"
    source: "OECD Shortage Lists, immigration agency lists"
  # 收入与回报
  value_added:
    index: 25
    type: float
    range: [0, 10]
    weight: 5
    category: "收入与回报"
    description_zh: "附加值水平(0=最低工资, 10=顶薪+股权)"
    description_en: "Value-added level"
    source: "ILO Global Wage Report, Glassdoor, PayScale"
  cost_performance:
    index: 26
    type: float
    range: [0, 10]
    weight: 4
    category: "收入与回报"
    description_zh: "性价比(0=高投入低回报, 10=低投入高回报)"
    description_en: "Cost-performance ratio"
    source: "Composite: value_added / (learning_cost + education_req)"
  # 稳定与风险
  stability:
    index: 27
    type: float
    range: [0, 10]
    weight: 4
    category: "稳定与风险"
    description_zh: "稳定性(0=极不稳定, 10=铁饭碗)"
    description_en: "Job stability"
    source: "OECD Employment Protection, ILO"
  safety:
    index: 28
    type: float
    range: [0, 10]
    weight: 3
    category: "稳定与风险"
    description_zh: "安全系数(0=致命高危, 10=零风险)"
    description_en: "Occupational safety"
    source: "ILO Safety & Health, OSHA, EU-OSHA"
  occupational_disease:
    index: 29
    type: float
    range: [0, 10]
    weight: 2
    category: "稳定与风险"
    description_zh: "职业病系数(0=高发, 10=几乎无)"
    description_en: "Occupational disease risk (inverted)"
    source: "WHO Occupational Health"
  overtime:
    index: 30
    type: float
    range: [0, 10]
    weight: 3
    category: "稳定与风险"
    description_zh: "加班程度(0=极端996, 10=准时下班)"
    description_en: "Overtime level (inverted)"
    source: "OECD Hours Worked, Glassdoor"
  burnout:
    index: 31
    type: float
    range: [0, 10]
    weight: 3
    category: "稳定与风险"
    description_zh: "倦怠水平(0=极度倦怠, 10=身心愉悦)"
    description_en: "Burnout level (inverted)"
    source: "Gallup Workplace, WHO Burnout research"
  # 口碑与转型
  skill_versatility:
    index: 32
    type: float
    range: [0, 10]
    weight: 3
    category: "口碑与转型"
    description_zh: "技能通用性(0=不可迁移, 10=万能技能)"
    description_en: "Skill versatility / transferability"
    source: "O*NET Skills Transferability, LinkedIn"
  career_switch:
    index: 33
    type: float
    range: [0, 10]
    weight: 3
    category: "口碑与转型"
    description_zh: "转行容易度(0=无法转行, 10=随时切换)"
    description_en: "Ease of career transition"
    source: "LinkedIn Career Transitions"
  reputation_variance:
    index: 34
    type: float
    range: [0, 5]
    weight: 3
    category: "口碑与转型"
    special_normalization: "reverse_0_5"
    description_zh: "口碑方差(0=稳定一致, 5=两极分化)"
    description_en: "Reputation variance"
    source: "Glassdoor/知乎/Reddit/Quora sentiment analysis"
  # 未来
  ai_resistance:
    index: 35
    type: float
    range: [0, 10]
    weight: 6
    category: "未来"
    description_zh: "AI抗性(0=即将替代, 10=完全不受影响)"
    description_en: "AI replacement resistance"
    source: "Oxford Frey-Osborne, WEF Future of Jobs 2025"
  # 生活质量
  social_status:
    index: 36
    type: float
    range: [0, 10]
    weight: 3
    category: "生活质量"
    description_zh: "社会地位(0=底层, 10=极高)"
    description_en: "Social status / prestige"
    source: "SIOPS/ISEI surveys, Gallup"
  remote_friendly:
    index: 37
    type: float
    range: [0, 10]
    weight: 3
    category: "生活质量"
    description_zh: "远程友好度(0=必须现场, 10=100%远程)"
    description_en: "Remote work friendliness"
    source: "McKinsey Remote Work, FlexJobs"
  autonomy:
    index: 38
    type: float
    range: [0, 10]
    weight: 3
    category: "生活质量"
    description_zh: "自由度(0=完全受控, 10=完全自主)"
    description_en: "Autonomy / independence"
    source: "O*NET Work Context, Gallup"
  family_friendly:
    index: 39
    type: float
    range: [0, 10]
    weight: 3
    category: "生活质量"
    description_zh: "家庭友好度(0=极不兼容, 10=完美兼顾)"
    description_en: "Family friendliness"
    source: "OECD Better Life Index, UNICEF"
  fulfillment:
    index: 40
    type: float
    range: [0, 10]
    weight: 3
    category: "生活质量"
    description_zh: "成就感(0=无意义, 10=极高使命感)"
    description_en: "Sense of fulfillment / purpose"
    source: "Gallup Employee Engagement"
  # 结构性与灵活性
  entrepreneurship:
    index: 41
    type: float
    range: [0, 10]
    weight: 2
    category: "结构性与灵活性"
    description_zh: "创业转化率(0=无人创业, 10=大量成功)"
    description_en: "Entrepreneurship conversion"
    source: "GEM Global Entrepreneurship, Crunchbase"
  gender_equality:
    index: 42
    type: float
    range: [0, 10]
    weight: 2
    category: "结构性与灵活性"
    description_zh: "性别平等度(0=极端失衡, 10=完全均衡)"
    description_en: "Gender equality"
    source: "ILO Gender Stats, WEF Gender Gap"
  age_flexibility:
    index: 43
    type: float
    range: [0, 10]
    weight: 2
    category: "结构性与灵活性"
    description_zh: "入行年龄弹性(0=只收应届, 10=任何年龄)"
    description_en: "Age flexibility for entry"
    source: "OECD Aging Worker data"
  social_interaction:
    index: 44
    type: float
    range: [0, 10]
    weight: 2
    category: "结构性与灵活性"
    description_zh: "社交属性(0=完全独立, 10=高频互动)"
    description_en: "Social interaction level"
    source: "O*NET Work Context: Social"
  physical_demand:
    index: 45
    type: float
    range: [0, 10]
    weight: 1
    category: "结构性与灵活性"
    reverse: true
    description_zh: "体力要求(0=纯脑力, 10=重体力)"
    description_en: "Physical demand"
    source: "O*NET Physical Demands"
  license_barrier:
    index: 46
    type: float
    range: [0, 10]
    weight: 2
    category: "结构性与灵活性"
    reverse: true
    description_zh: "政策壁垒(0=无门槛, 10=国家级执照)"
    description_en: "Licensing / regulatory barrier"
    source: "National occupational licensing laws"
  cycle_sensitivity:
    index: 47
    type: float
    range: [0, 10]
    weight: 2
    category: "结构性与灵活性"
    reverse: true
    description_zh: "周期敏感度(0=抗周期, 10=剧烈波动)"
    description_en: "Economic cycle sensitivity"
    source: "GDP-employment elasticity data"
  side_job_compat:
    index: 48
    type: float
    range: [0, 10]
    weight: 2
    category: "结构性与灵活性"
    description_zh: "副业兼容性(0=禁止, 10=自由斜杠)"
    description_en: "Side job / gig compatibility"
    source: "National labor laws, industry norms"
  intl_mobility:
    index: 49
    type: float
    range: [0, 10]
    weight: 3
    category: "结构性与灵活性"
    description_zh: "国际流动性(0=不互认, 10=全球通用)"
    description_en: "International mobility"
    source: "Mutual recognition agreements"
  industry_monopoly:
    index: 50
    type: float
    range: [0, 10]
    weight: 2
    category: "结构性与灵活性"
    reverse: true
    description_zh: "行业垄断度(0=自由竞争, 10=完全垄断)"
    description_en: "Industry monopoly level"
    source: "HHI concentration indices"

  # === Trend & Summary (8 columns, indices 51-58) ===
  trend_2000_2026:
    index: 51
    type: integer
    range: [-5, 5]
    description_zh: "2000-2026整体趋势(-5暴跌 → +5暴涨)"
    description_en: "Overall trend 2000-2026"
  trend_5yr:
    index: 52
    type: integer
    range: [-5, 5]
    description_zh: "近5年趋势(-5暴跌 → +5暴涨)"
    description_en: "Recent 5-year trend"
  demand_direction:
    index: 53
    type: string
    enum: ["↑↑", "↑", "→", "↓", "↓↓"]
    description_zh: "需求方向"
    description_en: "Demand direction"
  ai_timeline:
    index: 54
    type: string
    description_zh: "AI影响时间线"
    description_en: "AI impact timeline"
  composite_index:
    index: 55
    type: float
    range: [0, 10]
    description_zh: "综合加权发展指数"
    description_en: "Composite weighted development index"
  summary_zh:
    index: 56
    type: string
    description_zh: "中文一句话摘要"
    description_en: "Chinese one-line summary"
  summary_en:
    index: 57
    type: string
    description_zh: "英文一句话摘要"
    description_en: "English one-line summary"
  data_source:
    index: 58
    type: string
    description_zh: "数据来源"
    description_en: "Data source annotation"
```

- [ ] **Step 2: Validate column count**

Run: `python3 -c "import yaml; d=yaml.safe_load(open('schema/SCHEMA.yaml')); print('Columns:', len(d['columns'])); assert len(d['columns']) == 58"`
Expected: `Columns: 58`

- [ ] **Step 3: Commit**

```bash
git add schema/SCHEMA.yaml
git commit -m "feat: add SCHEMA.yaml — 58 columns fully defined"
```

---

## Task 4: Mapping — country_meta.csv

**Files:**
- Create: `mapping/country_meta.csv`

- [ ] **Step 1: Write country_meta.csv**

```csv
iso_code,country_or_region,country_en,region,region_en,type,development_stage,gdp_usd_trillion_2025,population_million_2025,labor_force_million_2025
CN,中国,China,东亚,East Asia,country,emerging,18.5,1412,785
JP,日本,Japan,东亚,East Asia,country,developed,4.2,124,69
KR,韩国,South Korea,东亚,East Asia,country,developed,1.7,52,28
TW,中国台湾地区,Taiwan (China),东亚,East Asia,region,developed,0.8,24,12
HK,中国香港地区,Hong Kong (China),东亚,East Asia,region,developed,0.4,7,4
SG,新加坡,Singapore,东南亚,Southeast Asia,country,developed,0.5,6,4
TH,泰国,Thailand,东南亚,Southeast Asia,country,emerging,0.5,72,39
VN,越南,Vietnam,东南亚,Southeast Asia,country,developing,0.4,100,56
ID,印度尼西亚,Indonesia,东南亚,Southeast Asia,country,emerging,1.4,278,140
MY,马来西亚,Malaysia,东南亚,Southeast Asia,country,emerging,0.4,34,16
PH,菲律宾,Philippines,东南亚,Southeast Asia,country,developing,0.4,117,49
IN,印度,India,南亚,South Asia,country,developing,3.9,1440,520
PK,巴基斯坦,Pakistan,南亚,South Asia,country,developing,0.4,240,77
BD,孟加拉国,Bangladesh,南亚,South Asia,country,developing,0.5,175,73
AE,阿联酋,UAE,中亚/西亚,Central/West Asia,country,developed,0.5,10,6
IL,以色列,Israel,中亚/西亚,Central/West Asia,country,developed,0.5,10,4
SA,沙特阿拉伯,Saudi Arabia,中亚/西亚,Central/West Asia,country,emerging,1.1,37,16
TR,土耳其,Turkey,中亚/西亚,Central/West Asia,country,emerging,1.1,86,34
GB,英国,United Kingdom,西欧,Western Europe,country,developed,3.4,68,34
FR,法国,France,西欧,Western Europe,country,developed,3.0,68,30
DE,德国,Germany,西欧,Western Europe,country,developed,4.5,84,45
NL,荷兰,Netherlands,西欧,Western Europe,country,developed,1.1,18,9
CH,瑞士,Switzerland,西欧,Western Europe,country,developed,0.9,9,5
SE,瑞典,Sweden,北欧,Northern Europe,country,developed,0.6,11,6
DK,丹麦,Denmark,北欧,Northern Europe,country,developed,0.4,6,3
FI,芬兰,Finland,北欧,Northern Europe,country,developed,0.3,6,3
IT,意大利,Italy,南欧,Southern Europe,country,developed,2.2,59,26
ES,西班牙,Spain,南欧,Southern Europe,country,developed,1.6,48,24
PT,葡萄牙,Portugal,南欧,Southern Europe,country,developed,0.3,10,5
PL,波兰,Poland,东欧,Eastern Europe,country,emerging,0.8,38,18
CZ,捷克,Czech Republic,东欧,Eastern Europe,country,developed,0.3,11,5
RU,俄罗斯,Russia,东欧,Eastern Europe,country,emerging,2.0,144,75
US,美国,United States,北美,North America,country,developed,28.8,340,165
CA,加拿大,Canada,北美,North America,country,developed,2.1,40,21
MX,墨西哥,Mexico,北美,North America,country,emerging,1.8,130,60
BR,巴西,Brazil,南美,South America,country,emerging,2.2,216,107
AR,阿根廷,Argentina,南美,South America,country,emerging,0.6,46,21
CL,智利,Chile,南美,South America,country,emerging,0.3,20,10
CO,哥伦比亚,Colombia,南美,South America,country,emerging,0.3,52,26
AU,澳大利亚,Australia,大洋洲,Oceania,country,developed,1.8,26,14
NZ,新西兰,New Zealand,大洋洲,Oceania,country,developed,0.3,5,3
ZA,南非,South Africa,非洲,Africa,country,emerging,0.4,62,24
NG,尼日利亚,Nigeria,非洲,Africa,country,developing,0.5,230,70
KE,肯尼亚,Kenya,非洲,Africa,country,developing,0.1,56,23
EG,埃及,Egypt,非洲,Africa,country,developing,0.4,110,30
```

- [ ] **Step 2: Validate row count**

Run: `python3 -c "import pandas as pd; df=pd.read_csv('mapping/country_meta.csv'); print('Countries:', len(df)); assert len(df) == 45"`
Expected: `Countries: 45`

- [ ] **Step 3: Commit**

```bash
git add mapping/country_meta.csv
git commit -m "feat: add country_meta.csv — 45 countries/regions"
```

---

## Task 5: Schema — categories.yaml (Complete Taxonomy)

**Files:**
- Create: `schema/categories.yaml`

This file defines ALL ~1,300 occupations across 12 major categories. The TECH and GOV categories are shown in full below as templates. The executing agent must complete the remaining 10 categories following the same structure.

- [ ] **Step 1: Write categories.yaml with TECH and GOV complete**

```yaml
# Global Career Development Index — Occupation Taxonomy
# 12 major categories → mid-level categories → subcategories (~1,300 total)
# Each subcategory has: id_suffix, name_zh, name_en, isco_code, onet_code, locality

TECH:
  name_zh: 信息技术与数字化
  name_en: Information Technology & Digital
  mid_categories:
    software_dev:
      name_zh: 软件开发
      name_en: Software Development
      occupations:
        - {id: "0101", zh: "前端工程师", en: "Front-end Engineer", isco: "2514", onet: "15-1254.00", locality: global}
        - {id: "0102", zh: "后端工程师", en: "Back-end Engineer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0103", zh: "全栈工程师", en: "Full-stack Engineer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0104", zh: "移动端工程师(iOS)", en: "iOS Engineer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0105", zh: "移动端工程师(Android)", en: "Android Engineer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0106", zh: "嵌入式软件工程师", en: "Embedded Software Engineer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0107", zh: "游戏开发工程师", en: "Game Developer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0108", zh: "DevOps工程师", en: "DevOps Engineer", isco: "2522", onet: "15-1244.00", locality: global}
        - {id: "0109", zh: "QA/测试工程师", en: "QA / Test Engineer", isco: "2519", onet: "15-1253.00", locality: global}
    ai_data:
      name_zh: 人工智能与数据
      name_en: Artificial Intelligence & Data
      occupations:
        - {id: "0201", zh: "机器学习工程师", en: "Machine Learning Engineer", isco: "2511", onet: "15-2051.00", locality: global}
        - {id: "0202", zh: "数据科学家", en: "Data Scientist", isco: "2120", onet: "15-2051.00", locality: global}
        - {id: "0203", zh: "数据分析师", en: "Data Analyst", isco: "2120", onet: "15-2051.01", locality: global}
        - {id: "0204", zh: "数据工程师", en: "Data Engineer", isco: "2523", onet: "15-1243.00", locality: global}
        - {id: "0205", zh: "NLP工程师", en: "NLP Engineer", isco: "2511", onet: "15-2051.00", locality: global}
        - {id: "0206", zh: "计算机视觉工程师", en: "Computer Vision Engineer", isco: "2511", onet: "15-2051.00", locality: global}
        - {id: "0207", zh: "AI研究员", en: "AI Researcher", isco: "2511", onet: "15-2051.00", locality: global}
        - {id: "0208", zh: "数据标注员", en: "Data Annotator", isco: "4132", onet: "43-9021.00", locality: global}
        - {id: "0209", zh: "AI Trainer/RLHF标注师", en: "AI Trainer / RLHF Annotator", isco: "4132", onet: "", locality: global}
        - {id: "0210", zh: "AI产品经理", en: "AI Product Manager", isco: "1330", onet: "11-2021.00", locality: global}
        - {id: "0211", zh: "Prompt Engineer", en: "Prompt Engineer", isco: "2511", onet: "", locality: global}
    network_security:
      name_zh: 网络与安全
      name_en: Network & Security
      occupations:
        - {id: "0301", zh: "网络安全工程师", en: "Cybersecurity Engineer", isco: "2529", onet: "15-1212.00", locality: global}
        - {id: "0302", zh: "渗透测试工程师", en: "Penetration Tester", isco: "2529", onet: "15-1212.00", locality: global}
        - {id: "0303", zh: "网络架构师", en: "Network Architect", isco: "2523", onet: "15-1241.00", locality: global}
        - {id: "0304", zh: "系统管理员", en: "System Administrator", isco: "2522", onet: "15-1244.00", locality: global}
        - {id: "0305", zh: "云计算工程师", en: "Cloud Engineer", isco: "2523", onet: "15-1244.00", locality: global}
        - {id: "0306", zh: "漏洞赏金猎人", en: "Bug Bounty Hunter", isco: "2529", onet: "15-1212.00", locality: global}
    product_design:
      name_zh: 产品与设计
      name_en: Product & Design
      occupations:
        - {id: "0401", zh: "产品经理", en: "Product Manager", isco: "1330", onet: "11-2021.00", locality: global}
        - {id: "0402", zh: "UI设计师", en: "UI Designer", isco: "2166", onet: "27-1024.00", locality: global}
        - {id: "0403", zh: "UX研究员", en: "UX Researcher", isco: "2166", onet: "27-1024.00", locality: global}
        - {id: "0404", zh: "交互设计师", en: "Interaction Designer", isco: "2166", onet: "27-1024.00", locality: global}
    emerging_digital:
      name_zh: 新兴数字职业
      name_en: Emerging Digital
      occupations:
        - {id: "0501", zh: "区块链开发者", en: "Blockchain Developer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0502", zh: "Web3工程师", en: "Web3 Engineer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0503", zh: "无人机软件工程师", en: "Drone Software Engineer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0504", zh: "AR/VR开发者", en: "AR/VR Developer", isco: "2514", onet: "15-1252.00", locality: global}
        - {id: "0505", zh: "量化交易开发者", en: "Quantitative Developer", isco: "2514", onet: "15-1252.00", locality: global}

GOV:
  name_zh: 公共管理与公务员
  name_en: Public Administration & Civil Service
  mid_categories:
    central_civil:
      name_zh: 中央/联邦公务员
      name_en: Central / Federal Civil Service
      occupations:
        - {id: "0101", zh: "行政管理官员", en: "Administrative Officer", isco: "1112", onet: "11-1011.00", locality: global}
        - {id: "0102", zh: "政策分析师", en: "Policy Analyst", isco: "2422", onet: "19-3094.00", locality: global}
        - {id: "0103", zh: "税务官员", en: "Tax Official", isco: "3352", onet: "13-2081.00", locality: global}
        - {id: "0104", zh: "海关关员", en: "Customs Officer", isco: "3351", onet: "33-3031.00", locality: global}
        - {id: "0105", zh: "外交官", en: "Diplomat", isco: "2422", onet: "19-3094.00", locality: global}
        - {id: "0106", zh: "审计官员", en: "Government Auditor", isco: "2411", onet: "13-2011.01", locality: global}
        - {id: "0107", zh: "监察/反腐官员", en: "Anti-corruption Inspector", isco: "2422", onet: "", locality: global}
        - {id: "0108", zh: "统计官员", en: "Government Statistician", isco: "2120", onet: "15-2041.00", locality: global}
        - {id: "0109", zh: "气象官员", en: "Meteorological Officer", isco: "2112", onet: "19-2021.00", locality: global}
        - {id: "0110", zh: "国会/议会工作人员", en: "Parliamentary Staff", isco: "3343", onet: "43-4171.00", locality: global}
    local_civil:
      name_zh: 地方公务员
      name_en: Local / State Civil Service
      occupations:
        - {id: "0201", zh: "地方行政官员", en: "Local Government Officer", isco: "1112", onet: "11-1011.00", locality: global}
        - {id: "0202", zh: "城市规划师(政府)", en: "Government Urban Planner", isco: "2164", onet: "19-3051.00", locality: global}
        - {id: "0203", zh: "社区干部/基层治理", en: "Community Administrator", isco: "1112", onet: "", locality: regional}
        - {id: "0204", zh: "城管执法人员", en: "Urban Management Officer", isco: "3355", onet: "", locality: country_specific}
    judicial_admin:
      name_zh: 司法行政
      name_en: Judicial Administration
      occupations:
        - {id: "0301", zh: "法院书记员", en: "Court Clerk", isco: "3343", onet: "43-4031.00", locality: global}
        - {id: "0302", zh: "法警", en: "Court Bailiff", isco: "5412", onet: "33-3011.00", locality: global}
        - {id: "0303", zh: "司法行政人员", en: "Judicial Administrator", isco: "3343", onet: "43-4031.00", locality: global}
    public_institutions:
      name_zh: 事业单位/公共机构
      name_en: Public Institutions
      occupations:
        - {id: "0401", zh: "公立学校教师(事业编)", en: "Public School Teacher (tenured)", isco: "2330", onet: "25-2021.00", locality: regional}
        - {id: "0402", zh: "公立医院医生(事业编)", en: "Public Hospital Doctor (tenured)", isco: "2211", onet: "29-1216.00", locality: regional}
        - {id: "0403", zh: "科研院所研究员", en: "Public Research Institute Scientist", isco: "2111", onet: "19-1042.00", locality: global}
        - {id: "0404", zh: "公共图书馆/博物馆(事业编)", en: "Public Library/Museum Staff (tenured)", isco: "2622", onet: "25-4022.00", locality: regional}
    international_org:
      name_zh: 国际组织
      name_en: International Organizations
      occupations:
        - {id: "0501", zh: "联合国职员", en: "United Nations Staff", isco: "2422", onet: "", locality: global}
        - {id: "0502", zh: "WHO/世卫职员", en: "WHO Staff", isco: "2422", onet: "", locality: global}
        - {id: "0503", zh: "世界银行/IMF职员", en: "World Bank / IMF Staff", isco: "2413", onet: "", locality: global}
        - {id: "0504", zh: "其他国际组织(OECD/WTO/ILO)", en: "Other Intl Org Staff", isco: "2422", onet: "", locality: global}
    military:
      name_zh: 军事
      name_en: Military
      occupations:
        - {id: "0601", zh: "陆军军官/士兵", en: "Army Officer / Soldier", isco: "0110", onet: "55-1011.00", locality: global}
        - {id: "0602", zh: "海军军官/士兵", en: "Navy Officer / Sailor", isco: "0110", onet: "55-1012.00", locality: global}
        - {id: "0603", zh: "空军军官/士兵", en: "Air Force Officer / Airman", isco: "0110", onet: "55-1013.00", locality: global}
        - {id: "0604", zh: "特种部队", en: "Special Forces", isco: "0110", onet: "55-3019.00", locality: global}
        - {id: "0605", zh: "军事工程师/技术军官", en: "Military Engineer / Technical Officer", isco: "0210", onet: "55-3019.00", locality: global}
    police_law_enforcement:
      name_zh: 警察与执法
      name_en: Police & Law Enforcement
      occupations:
        - {id: "0701", zh: "警察(正式编制)", en: "Police Officer", isco: "5412", onet: "33-3051.00", locality: global}
        - {id: "0702", zh: "辅警/协警", en: "Auxiliary Police", isco: "5412", onet: "", locality: regional}
        - {id: "0703", zh: "刑事侦查员", en: "Criminal Investigator / Detective", isco: "5412", onet: "33-3021.00", locality: global}
        - {id: "0704", zh: "交通警察", en: "Traffic Police", isco: "5412", onet: "33-3051.01", locality: global}
        - {id: "0705", zh: "网络警察", en: "Cyber Police", isco: "5412", onet: "", locality: regional}
        - {id: "0706", zh: "私人侦探", en: "Private Investigator", isco: "5414", onet: "33-9021.00", locality: global}
    fire_emergency:
      name_zh: 消防与应急
      name_en: Fire & Emergency
      occupations:
        - {id: "0801", zh: "消防员", en: "Firefighter", isco: "5411", onet: "33-2011.00", locality: global}
        - {id: "0802", zh: "急救医护(EMT/Paramedic)", en: "EMT / Paramedic", isco: "3258", onet: "29-2040.00", locality: global}
        - {id: "0803", zh: "灾害应急管理员", en: "Emergency Management Specialist", isco: "1344", onet: "13-1061.00", locality: global}
        - {id: "0804", zh: "海岸警卫队", en: "Coast Guard", isco: "0110", onet: "55-3019.00", locality: regional}
    intelligence_security:
      name_zh: 情报与安全
      name_en: Intelligence & Security
      occupations:
        - {id: "0901", zh: "情报分析员", en: "Intelligence Analyst", isco: "2422", onet: "33-3021.06", locality: global}
        - {id: "0902", zh: "安全官员", en: "Security Officer (Government)", isco: "5414", onet: "33-9032.00", locality: global}
        - {id: "0903", zh: "安保人员(民间)", en: "Private Security Guard", isco: "5414", onet: "33-9032.00", locality: global}

# === REMAINING 10 CATEGORIES — MUST BE COMPLETED BY EXECUTING AGENT ===
# Follow the exact structure above: major → mid_categories → occupations
# Each occupation: {id, zh, en, isco, onet, locality}
# Target occupation counts per category (approximate):

MED:
  name_zh: 医疗与健康
  name_en: Medical & Health
  target_count: 120
  mid_categories: {}
  # Expected mid-categories: 临床医学, 护理, 药学, 康复与治疗, 公共卫生,
  # 传统/替代医学(中医/阿育吠陀/脊椎指压), 口腔, 眼科, 心理健康,
  # 医学影像/检验, 医疗管理

FIN:
  name_zh: 金融与商业
  name_en: Finance & Business
  target_count: 110
  mid_categories: {}
  # Expected: 银行, 证券投资, 保险, 会计审计, 管理咨询, 房地产,
  # 伊斯兰金融, 精算, 企业管理, 人力资源, 供应链

EDU:
  name_zh: 教育与学术
  name_en: Education & Academia
  target_count: 60
  mid_categories: {}
  # Expected: K12教育, 高等教育, 职业培训, 在线教育, 学术研究,
  # 教育管理, 特殊教育, 早教

ENG:
  name_zh: 工程与制造
  name_en: Engineering & Manufacturing
  target_count: 130
  mid_categories: {}
  # Expected: 机械工程, 电气工程, 化学工程, 土木/建筑, 航空航天,
  # 汽车, 半导体, 核工程, 制造管理, 质量控制, 工业设计

LAW:
  name_zh: 法律与社会服务
  name_en: Legal & Social Services
  target_count: 70
  mid_categories: {}
  # Expected: 律师(各专业), 法官, 公证人, 社工, NGO, 宗教,
  # 人道主义, 调解/仲裁

ART:
  name_zh: 文化、艺术与传媒
  name_en: Culture, Arts & Media
  target_count: 200
  mid_categories: {}
  # Expected: 影视制作, 音乐产业, 出版写作, 舞台表演, 博物馆文化遗产,
  # 设计创意, 动画游戏, 广告公关, 新闻传媒, 新媒体内容,
  # 体育竞技, 会展, 图书馆信息, 文化产业管理

TRA:
  name_zh: 交通运输与物流
  name_en: Transport & Logistics
  target_count: 70
  mid_categories: {}
  # Expected: 航空, 航海, 铁路, 公路, 物流管理, 仓储,
  # 快递/最后一公里

SKL:
  name_zh: 技术工种与手工业
  name_en: Skilled Trades & Crafts
  target_count: 100
  mid_categories: {}
  # Expected: 电气, 管道暖通, 焊接, 机械加工(CNC), 汽车维修,
  # 建筑工, 传统手工艺(木工/裁缝/陶艺/制表), 美发美容技术

SVC:
  name_zh: 服务业与消费
  name_en: Service & Consumer
  target_count: 130
  mid_categories: {}
  # Expected: 餐饮, 酒店旅游, 零售, 美容养生, 家政照护,
  # 平台零工(网约车/外卖/跑腿), 殡葬, 特殊合法职业(性工作/大麻/博彩)

AGR:
  name_zh: 农业、资源与环境
  name_en: Agriculture, Resources & Environment
  target_count: 80
  mid_categories: {}
  # Expected: 种植, 畜牧, 渔业, 采矿, 石油天然气, 新能源(太阳能/风电),
  # 环保, 林业, 海水淡化
```

> **For executing agent:** Complete each remaining category with full occupation entries following the TECH/GOV template. Use the `target_count` as a guide (±10%). Each occupation must have: id, zh, en, isco (use closest match, "" if none), onet (use closest, "" if none), locality (global/regional/country_specific). Verify total across all 12 categories is between 1,200-1,400.

- [ ] **Step 2: Validate TECH and GOV counts**

Run: `python3 -c "
import yaml
d = yaml.safe_load(open('schema/categories.yaml'))
for cat in ['TECH', 'GOV']:
    total = sum(len(m['occupations']) for m in d[cat]['mid_categories'].values())
    print(f'{cat}: {total} occupations')
"`
Expected:
```
TECH: 35 occupations
GOV: 42 occupations
```

- [ ] **Step 3: Complete remaining 10 categories**

Fill in all `mid_categories: {}` sections with full occupation entries. Follow the TECH/GOV template exactly. After completion, validate:

Run: `python3 -c "
import yaml
d = yaml.safe_load(open('schema/categories.yaml'))
total = 0
for cat_key, cat in d.items():
    if 'mid_categories' not in cat or not cat['mid_categories']:
        print(f'INCOMPLETE: {cat_key}')
        continue
    n = sum(len(m['occupations']) for m in cat['mid_categories'].values())
    total += n
    print(f'{cat_key}: {n}')
print(f'TOTAL: {total}')
assert 1200 <= total <= 1400, f'Expected 1200-1400, got {total}'
"`
Expected: Each category shows a count, TOTAL between 1200-1400. No INCOMPLETE lines.

- [ ] **Step 4: Commit**

```bash
git add schema/categories.yaml
git commit -m "feat: add categories.yaml — complete occupation taxonomy (~1,300 occupations)"
```

---

## Task 6: Tool — score_calculator.py (TDD)

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_score_calculator.py`
- Create: `tools/score_calculator.py`

- [ ] **Step 1: Write conftest.py with shared fixtures**

```python
"""Shared test fixtures."""
import os
import pytest

@pytest.fixture
def project_root():
    """Return the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture
def weights_path(project_root):
    return os.path.join(project_root, "schema", "weights.yaml")

@pytest.fixture
def schema_path(project_root):
    return os.path.join(project_root, "schema", "SCHEMA.yaml")
```

- [ ] **Step 2: Write failing tests**

```python
"""Tests for score_calculator.py."""
import pytest
from tools.score_calculator import load_weights, normalize_variance, calculate_composite


class TestLoadWeights:
    def test_loads_34_weights(self, weights_path):
        weights = load_weights(weights_path)
        assert len(weights) == 34

    def test_weights_sum_to_100(self, weights_path):
        weights = load_weights(weights_path)
        assert sum(weights.values()) == 100

    def test_returns_dict(self, weights_path):
        weights = load_weights(weights_path)
        assert isinstance(weights, dict)
        assert "learning_cost" in weights
        assert "ai_resistance" in weights


class TestNormalizeVariance:
    def test_zero_variance_returns_10(self):
        assert normalize_variance(0) == 10.0

    def test_max_variance_returns_0(self):
        assert normalize_variance(5) == 0.0

    def test_mid_variance(self):
        assert normalize_variance(2.5) == 5.0


class TestCalculateComposite:
    def test_all_tens_returns_ten(self, weights_path):
        weights = load_weights(weights_path)
        scores = {dim: 10.0 for dim in weights}
        scores["reputation_variance"] = 0  # 0 variance = best = 10 after normalization
        result = calculate_composite(scores, weights)
        assert result == 10.0

    def test_all_zeros_returns_zero(self, weights_path):
        weights = load_weights(weights_path)
        scores = {dim: 0.0 for dim in weights}
        scores["reputation_variance"] = 5  # 5 variance = worst = 0 after normalization
        result = calculate_composite(scores, weights)
        assert result == 0.0

    def test_reverse_dimensions_are_inverted(self, weights_path):
        weights = load_weights(weights_path)
        # learning_cost is reverse: raw 10 means hard to enter = bad = 0 after inversion
        scores = {dim: 5.0 for dim in weights}
        scores["reputation_variance"] = 2.5
        result_baseline = calculate_composite(scores, weights)

        scores["learning_cost"] = 10.0  # worse raw score
        result_high_cost = calculate_composite(scores, weights)

        assert result_high_cost < result_baseline

    def test_result_in_valid_range(self, weights_path):
        weights = load_weights(weights_path)
        scores = {dim: 7.0 for dim in weights}
        scores["reputation_variance"] = 1.5
        result = calculate_composite(scores, weights)
        assert 0 <= result <= 10
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd . && python3 -m pytest tests/test_score_calculator.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'tools.score_calculator'`

- [ ] **Step 4: Write implementation**

```python
"""Composite score calculator for the Global Career Development Index.

Loads weights from schema/weights.yaml, handles reverse dimensions,
normalizes reputation_variance (0-5 → 0-10 reversed), and computes
the weighted composite index (0-10).
"""
import yaml
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

REVERSE_DIMENSIONS = {
    "learning_cost",
    "education_req",
    "physical_demand",
    "license_barrier",
    "cycle_sensitivity",
    "industry_monopoly",
}


def load_weights(weights_path=None):
    """Load dimension weights from YAML. Returns dict {dimension: weight_int}."""
    if weights_path is None:
        weights_path = _PROJECT_ROOT / "schema" / "weights.yaml"
    with open(weights_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["weights"]


def load_reverse_dimensions(weights_path=None):
    """Load the list of reverse dimensions from YAML."""
    if weights_path is None:
        weights_path = _PROJECT_ROOT / "schema" / "weights.yaml"
    with open(weights_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return set(data.get("reverse_dimensions", []))


def normalize_variance(raw_variance):
    """Convert 0-5 reputation_variance to 0-10 reversed score.

    0 (stable) → 10 (best), 5 (polarized) → 0 (worst).
    """
    return (5 - raw_variance) * 2


def calculate_composite(scores, weights, reverse_dims=None):
    """Calculate weighted composite index (0-10).

    Args:
        scores: dict {dimension_name: raw_score}
        weights: dict {dimension_name: weight_int} (weights sum to 100)
        reverse_dims: set of dimension names to invert. If None, uses module default.

    Returns:
        float: composite index rounded to 2 decimal places.
    """
    if reverse_dims is None:
        reverse_dims = REVERSE_DIMENSIONS

    total = 0.0
    weight_sum = sum(weights.values())

    for dim, weight_int in weights.items():
        raw = scores.get(dim, 0.0)

        if dim == "reputation_variance":
            adjusted = normalize_variance(raw)
        elif dim in reverse_dims:
            adjusted = 10.0 - raw
        else:
            adjusted = raw

        total += adjusted * (weight_int / weight_sum)

    return round(total, 2)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd . && python3 -m pytest tests/test_score_calculator.py -v`
Expected: All 7 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add tools/score_calculator.py tests/conftest.py tests/test_score_calculator.py
git commit -m "feat: add score_calculator.py with TDD — composite index calculation"
```

---

## Task 7: Tool — validate_data.py (TDD)

**Files:**
- Create: `tests/test_validate_data.py`
- Create: `tools/validate_data.py`

- [ ] **Step 1: Write failing tests**

```python
"""Tests for validate_data.py."""
import os
import tempfile
import pytest
import pandas as pd
from tools.validate_data import validate_csv, load_schema


class TestLoadSchema:
    def test_loads_schema(self, schema_path):
        schema = load_schema(schema_path)
        assert "columns" in schema
        assert len(schema["columns"]) == 58


class TestValidateCsv:
    def _make_csv(self, rows, tmpdir):
        """Helper: write rows to a temp CSV and return path."""
        path = os.path.join(tmpdir, "test.csv")
        df = pd.DataFrame(rows)
        df.to_csv(path, index=False)
        return path

    def test_valid_row_no_errors(self, schema_path, tmp_path):
        row = {
            "id": "TECH-0101-CN-general",
            "major_category": "信息技术与数字化",
            "major_code": "TECH",
            "mid_category": "软件开发",
            "sub_category": "前端工程师",
            "sub_category_en": "Front-end Engineer",
            "isco_code": "2514",
            "onet_code": "15-1254.00",
            "region": "东亚",
            "country_or_region": "中国",
            "iso_code": "CN",
            "type": "country",
            "employer_type": "general",
            "typical_education": "本科",
            "typical_entry_age": "22-26岁",
            "locality": "global",
        }
        # Add 34 score columns with valid values
        score_cols = [
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
        for col in score_cols:
            row[col] = 5.0 if col != "reputation_variance" else 2.5
        # Trend & summary columns
        row.update({
            "trend_2000_2026": 3, "trend_5yr": 1,
            "demand_direction": "↑", "ai_timeline": "2030-2035",
            "composite_index": 6.5, "summary_zh": "测试",
            "summary_en": "Test", "data_source": "test",
        })
        path = self._make_csv([row], tmp_path)
        errors = validate_csv(path, schema_path)
        assert errors == []

    def test_missing_column_reports_error(self, schema_path, tmp_path):
        row = {"id": "TECH-0101-CN-general"}  # missing most columns
        path = self._make_csv([row], tmp_path)
        errors = validate_csv(path, schema_path)
        assert any("Missing column" in e for e in errors)

    def test_score_out_of_range_reports_error(self, schema_path, tmp_path):
        row = {"id": "TEST", "major_code": "TECH"}
        # Fill all required columns
        for col_name in ["major_category", "mid_category", "sub_category",
                         "sub_category_en", "isco_code", "onet_code", "region",
                         "country_or_region", "iso_code", "type", "employer_type",
                         "typical_education", "typical_entry_age", "locality"]:
            row[col_name] = "test"
        score_cols = [
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
        for col in score_cols:
            row[col] = 5.0
        row["learning_cost"] = 15.0  # out of range!
        row.update({
            "trend_2000_2026": 3, "trend_5yr": 1,
            "demand_direction": "↑", "ai_timeline": "2030",
            "composite_index": 5.0, "summary_zh": "t",
            "summary_en": "t", "data_source": "t",
        })
        path = self._make_csv([row], tmp_path)
        errors = validate_csv(path, schema_path)
        assert any("learning_cost" in e and "out of range" in e for e in errors)

    def test_invalid_enum_reports_error(self, schema_path, tmp_path):
        row = {"id": "TEST", "major_code": "INVALID_CODE"}
        for col_name in ["major_category", "mid_category", "sub_category",
                         "sub_category_en", "isco_code", "onet_code", "region",
                         "country_or_region", "iso_code", "typical_education",
                         "typical_entry_age"]:
            row[col_name] = "test"
        row["type"] = "invalid_type"
        row["employer_type"] = "general"
        row["locality"] = "global"
        score_cols = [
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
        for col in score_cols:
            row[col] = 5.0
        row.update({
            "trend_2000_2026": 3, "trend_5yr": 1,
            "demand_direction": "↑", "ai_timeline": "2030",
            "composite_index": 5.0, "summary_zh": "t",
            "summary_en": "t", "data_source": "t",
        })
        path = self._make_csv([row], tmp_path)
        errors = validate_csv(path, schema_path)
        assert any("type" in e and "invalid" in e.lower() for e in errors)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_validate_data.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write implementation**

```python
"""CSV validation against SCHEMA.yaml.

Checks: required columns present, score ranges, enum values, row count.
"""
import pandas as pd
import yaml
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_schema(schema_path=None):
    """Load SCHEMA.yaml."""
    if schema_path is None:
        schema_path = _PROJECT_ROOT / "schema" / "SCHEMA.yaml"
    with open(schema_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_csv(csv_path, schema_path=None):
    """Validate a CSV file against the schema. Returns list of error strings."""
    schema = load_schema(schema_path)
    df = pd.read_csv(csv_path)
    errors = []

    col_defs = schema["columns"]

    # 1. Check required columns
    for col_name in col_defs:
        if col_name not in df.columns:
            errors.append(f"Missing column: {col_name}")

    if errors:
        return errors  # Can't do further checks with missing columns

    # 2. Check score ranges
    for col_name, col_def in col_defs.items():
        if col_def.get("type") == "float" and "range" in col_def:
            vmin, vmax = col_def["range"]
            out = df[(df[col_name] < vmin) | (df[col_name] > vmax)]
            if len(out) > 0:
                errors.append(
                    f"{col_name}: {len(out)} values out of range [{vmin}, {vmax}]"
                )

    # 3. Check integer ranges (trend columns)
    for col_name, col_def in col_defs.items():
        if col_def.get("type") == "integer" and "range" in col_def:
            vmin, vmax = col_def["range"]
            numeric = pd.to_numeric(df[col_name], errors="coerce")
            out = numeric[(numeric < vmin) | (numeric > vmax)]
            if len(out.dropna()) > 0:
                errors.append(
                    f"{col_name}: {len(out.dropna())} values out of range [{vmin}, {vmax}]"
                )

    # 4. Check enum values
    for col_name, col_def in col_defs.items():
        if "enum" in col_def:
            allowed = set(col_def["enum"])
            invalid = df[~df[col_name].isin(allowed)]
            if len(invalid) > 0:
                bad_vals = invalid[col_name].unique().tolist()
                errors.append(
                    f"{col_name}: invalid values {bad_vals} (allowed: {sorted(allowed)})"
                )

    return errors
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_validate_data.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/validate_data.py tests/test_validate_data.py
git commit -m "feat: add validate_data.py with TDD — CSV schema validation"
```

---

## Task 8: Tool — csv_to_json.py (TDD)

**Files:**
- Create: `tests/test_csv_to_json.py`
- Create: `tools/csv_to_json.py`

- [ ] **Step 1: Write failing tests**

```python
"""Tests for csv_to_json.py."""
import json
import os
import pytest
import pandas as pd
from tools.csv_to_json import convert_csv_to_json, generate_meta_files


class TestConvertCsvToJson:
    def _make_csv(self, rows, path):
        pd.DataFrame(rows).to_csv(path, index=False)

    def test_produces_valid_json(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        json_path = tmp_path / "test.json"
        self._make_csv([
            {"id": "TECH-0101-CN-general", "major_code": "TECH", "sub_category": "前端工程师"},
        ], csv_path)
        convert_csv_to_json(str(csv_path), str(json_path))
        assert json_path.exists()
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert "meta" in data
        assert "records" in data
        assert data["meta"]["record_count"] == 1
        assert data["meta"]["category"] == "TECH"

    def test_chinese_chars_preserved(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        json_path = tmp_path / "test.json"
        self._make_csv([
            {"id": "TECH-0101-CN-general", "major_code": "TECH", "sub_category": "前端工程师"},
        ], csv_path)
        convert_csv_to_json(str(csv_path), str(json_path))
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["records"][0]["sub_category"] == "前端工程师"

    def test_nested_score_structure(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        json_path = tmp_path / "test.json"
        self._make_csv([
            {"id": "T-01-CN", "major_code": "TECH", "learning_cost": 6.0, "ai_resistance": 4.0},
        ], csv_path)
        convert_csv_to_json(str(csv_path), str(json_path))
        data = json.loads(json_path.read_text(encoding="utf-8"))
        rec = data["records"][0]
        assert rec["learning_cost"] == 6.0


class TestGenerateMetaFiles:
    def test_creates_meta_directory(self, tmp_path, project_root):
        meta_dir = tmp_path / "meta"
        generate_meta_files(str(meta_dir), project_root)
        assert (meta_dir / "weights.json").exists()
        assert (meta_dir / "countries.json").exists()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_csv_to_json.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write implementation**

```python
"""Convert CSV data files to JSON mirror format.

Produces:
  - Per-category JSON: {meta: {...}, records: [...]}
  - Meta files: schema.json, categories.json, countries.json, weights.json
"""
import json
import pandas as pd
import yaml
from datetime import date
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def convert_csv_to_json(csv_path, json_path):
    """Convert a single CSV to structured JSON."""
    df = pd.read_csv(csv_path)

    meta = {
        "category": df["major_code"].iloc[0] if len(df) > 0 else "",
        "record_count": len(df),
        "updated": str(date.today()),
    }

    # Convert NaN to None for clean JSON
    records = df.where(df.notna(), None).to_dict(orient="records")

    output = {"meta": meta, "records": records}

    Path(json_path).parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


def generate_meta_files(meta_dir, project_root=None):
    """Generate JSON meta files from YAML sources."""
    if project_root is None:
        project_root = str(_PROJECT_ROOT)
    root = Path(project_root)
    meta = Path(meta_dir)
    meta.mkdir(parents=True, exist_ok=True)

    # weights.json
    with open(root / "schema" / "weights.yaml", encoding="utf-8") as f:
        weights = yaml.safe_load(f)
    with open(meta / "weights.json", "w", encoding="utf-8") as f:
        json.dump(weights, f, ensure_ascii=False, indent=2)

    # countries.json
    countries_csv = root / "mapping" / "country_meta.csv"
    if countries_csv.exists():
        df = pd.read_csv(countries_csv)
        countries = df.to_dict(orient="records")
        with open(meta / "countries.json", "w", encoding="utf-8") as f:
            json.dump(countries, f, ensure_ascii=False, indent=2)

    # schema.json
    schema_yaml = root / "schema" / "SCHEMA.yaml"
    if schema_yaml.exists():
        with open(schema_yaml, encoding="utf-8") as f:
            schema = yaml.safe_load(f)
        with open(meta / "schema.json", "w", encoding="utf-8") as f:
            json.dump(schema, f, ensure_ascii=False, indent=2)

    # categories.json
    cat_yaml = root / "schema" / "categories.yaml"
    if cat_yaml.exists():
        with open(cat_yaml, encoding="utf-8") as f:
            categories = yaml.safe_load(f)
        with open(meta / "categories.json", "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_csv_to_json.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/csv_to_json.py tests/test_csv_to_json.py
git commit -m "feat: add csv_to_json.py with TDD — JSON mirror generation"
```

---

## Task 9: Tool — generate_notebook.py (TDD)

**Files:**
- Create: `tests/test_generate_notebook.py`
- Create: `tools/generate_notebook.py`

- [ ] **Step 1: Write failing tests**

```python
"""Tests for generate_notebook.py."""
import json
import os
import pytest
import pandas as pd
from tools.generate_notebook import create_data_notebook, SCORE_COLUMNS


class TestCreateDataNotebook:
    def _make_csv(self, rows, path):
        pd.DataFrame(rows).to_csv(path, index=False)

    def test_creates_ipynb_file(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        self._make_csv([
            {"id": "TECH-0101-CN", "major_code": "TECH", "sub_category": "前端工程师",
             "learning_cost": 6.0, "ai_resistance": 4.0, "reputation_variance": 1.5,
             "composite_index": 6.5},
        ], csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="Test Notebook")
        assert nb_path.exists()

    def test_ipynb_is_valid_json(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        self._make_csv([
            {"id": "TECH-0101-CN", "major_code": "TECH", "sub_category": "前端工程师",
             "learning_cost": 6.0, "composite_index": 6.5},
        ], csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="Test")
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        assert data["nbformat"] == 4
        assert len(data["cells"]) >= 2  # at least markdown header + code cell

    def test_contains_styling_code(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        self._make_csv([
            {"id": "T-01-CN", "major_code": "TECH", "learning_cost": 6.0},
        ], csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="Test")
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        code_cells = [c for c in data["cells"] if c["cell_type"] == "code"]
        all_code = "\n".join("".join(c["source"]) for c in code_cells)
        assert "background_gradient" in all_code
        assert "RdYlGn" in all_code


class TestScoreColumns:
    def test_has_34_score_columns(self):
        assert len(SCORE_COLUMNS) == 34

    def test_includes_key_columns(self):
        assert "learning_cost" in SCORE_COLUMNS
        assert "ai_resistance" in SCORE_COLUMNS
        assert "reputation_variance" in SCORE_COLUMNS
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_generate_notebook.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write implementation**

```python
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
    """Create a 1:1 data notebook with red-green heatmap styling.

    Args:
        csv_path: path to source CSV (relative from notebook location)
        notebook_path: output .ipynb path
        title: notebook title
        description: optional description markdown
    """
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
    md += "\n评分色阶：🔴 低分(0) → 🟡 中等(5) → 🟢 高分(10)  \n"
    md += "口碑方差：🟢 稳定(0) → 🔴 分化(5)  \n"
    md += "趋势：🔴 暴跌(-5) → ⚪ 持平(0) → 🟢 暴涨(+5)"
    nb.cells.append(new_markdown_cell(md))

    # Cell 2: Imports + load
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_generate_notebook.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/generate_notebook.py tests/test_generate_notebook.py
git commit -m "feat: add generate_notebook.py with TDD — styled notebook generation"
```

---

## Task 10: Pilot Data — tech_digital.csv

**Files:**
- Create: `data/csv/tech_digital.csv`

This is the core data generation task. The executing agent generates scored data for all TECH occupations across all 45 countries.

- [ ] **Step 1: Generate tech_digital.csv**

Read `schema/categories.yaml` to get the full list of TECH occupations (~35).
Read `mapping/country_meta.csv` for the 45 countries.

For each occupation × each country (where `locality` applies):
- `global` occupations: generate row for all 45 countries
- `regional` occupations: generate row for countries where the occupation has meaningful presence
- `country_specific`: generate row only for relevant countries

Score each dimension 0-10 based on:
1. **Authority data anchors** where available (O*NET for US, ILO for global, OECD for developed countries)
2. **AI calibration** for remaining dimensions and countries
3. **Cross-check**: scores should be consistent — e.g., a country with higher GDP should generally have higher `value_added` for the same occupation

Calculate `composite_index` using `tools/score_calculator.py`.
Generate `summary_zh` and `summary_en` for each row.
Set `data_source` to appropriate annotation.

CSV format — first row must be the 58 column headers exactly matching SCHEMA.yaml column order:
```
id,major_category,major_code,mid_category,sub_category,sub_category_en,isco_code,onet_code,region,country_or_region,iso_code,type,employer_type,typical_education,typical_entry_age,locality,learning_cost,education_req,...,composite_index,summary_zh,summary_en,data_source
```

Example rows (for format reference):
```
TECH-0101-CN-general,信息技术与数字化,TECH,软件开发,前端工程师,Front-end Engineer,2514,15-1254.00,东亚,中国,CN,country,general,本科,22-26岁,global,6.5,5.5,7.0,5.0,6.5,8.0,5.5,4.0,7.0,7.5,4.5,9.5,9.0,3.0,4.0,7.5,7.0,2.0,3.5,6.0,9.0,7.5,5.0,6.5,8.0,4.5,6.5,7.0,1.0,3.0,5.5,8.0,7.0,4.0,3,1,↑,2028-2032,6.21,中国前端工程师供过于求但远程友好度高 AI冲击临近,China front-end engineer: oversupply but high remote-friendliness; AI impact imminent,AI综合评估 + O*NET/ILO/OECD锚点校准
TECH-0101-US-general,信息技术与数字化,TECH,软件开发,前端工程师,Front-end Engineer,2514,15-1254.00,北美,美国,US,country,general,本科,22-26岁,global,6.0,5.0,7.5,5.0,6.0,8.5,6.0,5.0,8.5,8.0,5.0,9.5,9.5,4.0,4.5,7.5,7.5,1.8,3.5,7.0,9.5,8.0,5.5,7.0,8.5,6.0,7.0,7.0,0.5,2.5,6.0,8.5,8.0,3.5,3,-1,→,2027-2030,6.78,美国前端高薪但AI替代压力大 远程文化成熟,US front-end: high pay but strong AI replacement pressure; mature remote culture,AI综合评估 + O*NET/BLS/OECD锚点校准
```

Generate in batches by mid_category (software_dev, ai_data, network_security, product_design, emerging_digital), validating each batch before proceeding.

- [ ] **Step 2: Validate with tools**

Run: `python3 -c "
from tools.validate_data import validate_csv
errors = validate_csv('data/csv/tech_digital.csv')
if errors:
    for e in errors:
        print(f'ERROR: {e}')
else:
    print('VALID: No errors found')

import pandas as pd
df = pd.read_csv('data/csv/tech_digital.csv')
print(f'Rows: {len(df)}')
print(f'Countries: {df[\"iso_code\"].nunique()}')
print(f'Occupations: {df[\"sub_category\"].nunique()}')
print(f'Composite range: {df[\"composite_index\"].min():.2f} - {df[\"composite_index\"].max():.2f}')
"`
Expected: `VALID: No errors found`, Rows ~1400-1600, Countries ~45, Occupations ~35, Composite range within 2.0-9.0.

- [ ] **Step 3: Spot-check composite scores**

Run: `python3 -c "
import pandas as pd
from tools.score_calculator import load_weights, calculate_composite

df = pd.read_csv('data/csv/tech_digital.csv')
weights = load_weights()

# Verify 5 random rows
sample = df.sample(5, random_state=42)
for _, row in sample.iterrows():
    scores = {dim: row[dim] for dim in weights}
    calc = calculate_composite(scores, weights)
    csv_val = row['composite_index']
    diff = abs(calc - csv_val)
    status = 'OK' if diff < 0.05 else 'MISMATCH'
    print(f'{status}: {row[\"id\"]} csv={csv_val} calc={calc} diff={diff:.3f}')
"`
Expected: All 5 rows show `OK`.

- [ ] **Step 4: Commit**

```bash
git add data/csv/tech_digital.csv
git commit -m "feat: add tech_digital.csv — TECH pilot data (~1500 rows × 58 cols)"
```

---

## Task 11: Pilot Pipeline — JSON Mirror + Meta Files

**Files:**
- Create: `data/json/tech_digital.json`
- Create: `data/json/meta/schema.json`
- Create: `data/json/meta/categories.json`
- Create: `data/json/meta/countries.json`
- Create: `data/json/meta/weights.json`

- [ ] **Step 1: Generate JSON mirror and meta files**

Run: `python3 -c "
from tools.csv_to_json import convert_csv_to_json, generate_meta_files

convert_csv_to_json('data/csv/tech_digital.csv', 'data/json/tech_digital.json')
generate_meta_files('data/json/meta')

import json
with open('data/json/tech_digital.json', encoding='utf-8') as f:
    d = json.load(f)
print(f'JSON records: {d[\"meta\"][\"record_count\"]}')
print(f'Meta files generated')
"`
Expected: JSON record count matches CSV row count. No errors.

- [ ] **Step 2: Verify meta files exist**

Run: `ls -la data/json/meta/`
Expected: 4 files — schema.json, categories.json, countries.json, weights.json

- [ ] **Step 3: Commit**

```bash
git add data/json/
git commit -m "feat: add JSON mirror + meta files for TECH pilot"
```

---

## Task 12: Pilot Notebooks — 00_overview + 01_tech

**Files:**
- Create: `notebooks/00_数据总览.ipynb`
- Create: `notebooks/01_tech_digital.ipynb`

- [ ] **Step 1: Generate 01_tech_digital.ipynb**

Run: `python3 -c "
from tools.generate_notebook import create_data_notebook
create_data_notebook(
    csv_path='data/csv/tech_digital.csv',
    notebook_path='notebooks/01_tech_digital.ipynb',
    title='信息技术与数字化 (TECH) — 完整数据',
    description='全部TECH类职业 × 45国/地区，红绿色阶评分表。'
)
print('Created 01_tech_digital.ipynb')
"`
Expected: File created, no errors.

- [ ] **Step 2: Create 00_数据总览.ipynb manually**

This overview notebook is unique — it's not auto-generated from a single CSV. Create it with these cells:

**Cell 1 (Markdown):**
```markdown
# 🌍 全球职业发展指数 — 数据总览

**Global Career Development Index**

~1,300 职业 · 45 国家/地区 · 34 评分维度 · 权威数据+AI校准
```

**Cell 2 (Code):** Load and summarize all available CSV files:
```python
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

csv_dir = Path('../data/csv')
all_dfs = []
for f in sorted(csv_dir.glob('*.csv')):
    df = pd.read_csv(f)
    all_dfs.append(df)
    print(f"{f.name}: {len(df)} rows, {df['sub_category'].nunique()} occupations, {df['iso_code'].nunique()} countries")

if all_dfs:
    full = pd.concat(all_dfs, ignore_index=True)
    print(f"\n总计: {len(full)} rows, {full['sub_category'].nunique()} occupations, {full['iso_code'].nunique()} countries")
```

**Cell 3 (Markdown):** Weight table
```markdown
## 权重体系 (34维度 = 100%)

| 类别 | 权重 | 维度 |
|------|------|------|
| 入门门槛 | 6% | 学习成本(3%) + 学历要求(3%) |
| 发展空间 | 10% | 成长系数(4%) + 寿命(3%) + 机遇(3%) |
| 市场面 | 10% | 市场大小(2%) + 供需(4%) + 发达国家稀缺(4%) |
| 收入与回报 | 9% | 附加值(5%) + 性价比(4%) |
| 稳定与风险 | 15% | 稳定性(4%) + 安全(3%) + 职业病(2%) + 加班(3%) + 倦怠(3%) |
| 口碑与转型 | 9% | 技能通用(3%) + 转行(3%) + 口碑方差(3%) |
| 未来 | 6% | AI抗性(6%) |
| 生活质量 | 15% | 地位(3%) + 远程(3%) + 自由(3%) + 家庭(3%) + 成就感(3%) |
| 结构性与灵活性 | 20% | 创业(2%) + 性别(2%) + 年龄弹性(2%) + 社交(2%) + 体力(1%) + 执照(2%) + 周期(2%) + 副业(2%) + 国际流动(3%) + 垄断(2%) |
```

**Cell 4 (Code):** Composite index distribution:
```python
if all_dfs:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 4))
    full['composite_index'].hist(bins=50, ax=ax, color='steelblue', edgecolor='white')
    ax.set_xlabel('综合加权发展指数')
    ax.set_ylabel('频数')
    ax.set_title('Composite Index Distribution')
    plt.tight_layout()
    plt.show()
```

Write this notebook using nbformat (same pattern as generate_notebook.py).

- [ ] **Step 3: Verify notebooks are valid**

Run: `python3 -c "
import nbformat
for nb_path in ['notebooks/00_数据总览.ipynb', 'notebooks/01_tech_digital.ipynb']:
    with open(nb_path, encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    print(f'{nb_path}: {len(nb.cells)} cells, valid')
"`
Expected: Both notebooks report valid with reasonable cell counts.

- [ ] **Step 4: Commit**

```bash
git add notebooks/
git commit -m "feat: add pilot notebooks — 00_overview + 01_tech_digital"
```

---

## Task 13: Documentation — README, FLOW, CHANGELOG

**Files:**
- Create: `README.md`
- Create: `README_EN.md`
- Create: `FLOW.md`
- Create: `CHANGELOG.md`

- [ ] **Step 1: Write README.md**

Follow the reference repo (host452b/travel_with_family) structure:
- Project title and one-line description
- Table of notebook links (Notebook | 内容)
- Data files table (文件 | 记录 | 覆盖)
- 量化指标表 (指标 | 0分 | 10分 | 权重) — all 34 dimensions
- 口碑方差解读
- 数据来源表

For the current state (Plan 1 = TECH pilot only), mark other categories as "即将上线" in the tables.

- [ ] **Step 2: Write README_EN.md**

English translation of README.md. Same structure, English content.

- [ ] **Step 3: Write FLOW.md**

Follow the reference repo pattern:
```markdown
# 数据维护流程 (Flow)

## 扩展数据
1. 新职业 → 先更新 schema/categories.yaml
2. 每条记录必须包含: 58列完整数据
3. 评分0-10统一制，综合加权按weights.yaml计算
4. 用 tools/validate_data.py 验证后再提交

## 校准数据
1. O*NET → 校准美国职业评分
2. ILO ILOSTAT → 校准全球就业/安全/工时
3. OECD → 校准发达国家数据
4. Glassdoor/LinkedIn → 校准口碑和供需
5. 实际薪资数据 → 校准附加值

## 生成产出
1. 每个CSV对应一个.ipynb (红绿色阶完整数据)
2. 排行榜notebooks (13-17)
3. 国家全景notebooks (22-66)
4. JSON镜像: python3 -c "from tools.csv_to_json import ..."
5. README含完整权重表和列说明

## 58列统一结构
id/大类/代码/中类/细类/英文/ISCO/O*NET/区域/国家/ISO/类型/雇主/学历/年龄/地区性
34个评分维度
趋势(2个)/需求方向/AI时间线/综合指数/摘要中/摘要英/来源
```

- [ ] **Step 4: Write CHANGELOG.md**

```markdown
# Changelog

## [0.1.0] - 2026-04-12
### Added
- Project infrastructure: schema, mappings, Python tools
- TECH category pilot: ~1,500 rows × 58 columns × 45 countries
- 2 pilot notebooks (overview + TECH data)
- JSON mirror + meta files
- Tools: score_calculator, validate_data, csv_to_json, generate_notebook
- Documentation: README (zh/en), FLOW.md
```

- [ ] **Step 5: Commit**

```bash
git add README.md README_EN.md FLOW.md CHANGELOG.md
git commit -m "docs: add README (zh/en), FLOW.md, CHANGELOG.md"
```

---

## Task 14: End-to-End Validation & Final Commit

**Files:** None new — validation only.

- [ ] **Step 1: Run full test suite**

Run: `python3 -m pytest tests/ -v`
Expected: All tests PASS (across all 4 test files).

- [ ] **Step 2: Validate data pipeline end-to-end**

Run: `python3 -c "
print('=== 1. Schema validation ===')
import yaml
schema = yaml.safe_load(open('schema/SCHEMA.yaml'))
print(f'Columns defined: {len(schema[\"columns\"])}')

weights = yaml.safe_load(open('schema/weights.yaml'))
print(f'Weights sum: {sum(weights[\"weights\"].values())}')

print('\n=== 2. CSV validation ===')
from tools.validate_data import validate_csv
errors = validate_csv('data/csv/tech_digital.csv')
print(f'Errors: {len(errors)}')
for e in errors[:5]:
    print(f'  {e}')

print('\n=== 3. JSON mirror ===')
import json
with open('data/json/tech_digital.json', encoding='utf-8') as f:
    d = json.load(f)
print(f'JSON records: {d[\"meta\"][\"record_count\"]}')

print('\n=== 4. Notebooks ===')
import nbformat
for p in ['notebooks/00_数据总览.ipynb', 'notebooks/01_tech_digital.ipynb']:
    with open(p, encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    print(f'{p}: {len(nb.cells)} cells OK')

print('\n=== 5. Categories ===')
cats = yaml.safe_load(open('schema/categories.yaml'))
total = 0
for k, v in cats.items():
    if isinstance(v, dict) and 'mid_categories' in v and v['mid_categories']:
        n = sum(len(m['occupations']) for m in v['mid_categories'].values())
        total += n
        print(f'{k}: {n}')
print(f'Total occupations: {total}')

print('\nALL CHECKS PASSED' if len(errors) == 0 else 'ERRORS FOUND')
"`
Expected: All checks pass. Total occupations between 1,200-1,400. No validation errors.

- [ ] **Step 3: Final commit (if any unstaged changes)**

```bash
git status
# If any unstaged files:
git add -A
git commit -m "chore: final validation pass — Plan 1 complete"
```

---

## Next Plans

After Plan 1 is complete, proceed with:

| Plan | Task | Command |
|------|------|---------|
| 2 | Generate `medical_health.csv` (MED, ~120 occupations × 45 countries) | Same pipeline as Task 10 |
| 3 | Generate `finance_business.csv` (FIN) | Same pipeline |
| 4 | Generate `education_academia.csv` (EDU) | Same pipeline |
| 5 | Generate `engineering_manufacturing.csv` (ENG) | Same pipeline |
| 6 | Generate `gov_public.csv` (GOV) | Same pipeline |
| 7 | Generate `legal_social.csv` (LAW) | Same pipeline |
| 8 | Generate `culture_arts_media.csv` (ART, ~200 occupations — largest) | Same pipeline |
| 9 | Generate `transport_logistics.csv` (TRA) | Same pipeline |
| 10 | Generate `skilled_trades.csv` (SKL) | Same pipeline |
| 11 | Generate `service_consumer.csv` (SVC) | Same pipeline |
| 12 | Generate `agriculture_resources.csv` (AGR) | Same pipeline |
| 13 | Generate remaining 73 notebooks (rankings, trends, country panoramas, special topics) | Uses generate_notebook.py |

Each plan follows the same pattern: generate CSV → validate → JSON mirror → notebook → commit.

## Deferred to Future Plans

The following items from the design spec are intentionally deferred from Plan 1:

- **mapping_isco.csv** — ISCO-08 cross-reference mapping (ISCO codes are already in each CSV row and categories.yaml; the dedicated mapping file enables bulk external joins but is not needed for the pilot)
- **mapping_onet.csv** — O*NET SOC cross-reference mapping (same reasoning)
- **mapping_isced.csv** — ISCED education level mapping
- **Remaining 11 CSV data files** — Plans 2-12
- **Remaining 73 notebooks** — Plan 13
- **query_tool.ipynb** — Plan 13
