# Global Career Development Index

A comprehensive multi-dimensional career scoring database. **54,000 records · 1,200 occupations · 45 countries/regions · 34 quantitative metrics · multi-source calibrated**

## Visual Reports (Click to View)

All tables feature **red-green color scale**: low scores red → medium yellow → high scores green. Variance column reversed: green = stable, red = polarized.

### Master Tables

| Notebook | Contents |
|----------|----------|
| [00_全部职业总表.ipynb](notebooks/00_全部职业总表.ipynb) | **1,200 occupations ranked by composite index** · 34-dim global means · 12 regional comparisons |
| [00_CN_中国职业发展指数完整版.ipynb](notebooks/00_CN_中国职业发展指数完整版.ipynb) | **China edition** · 1,200 occupations · China vs global comparison |
| [00_数据总览.ipynb](notebooks/00_数据总览.ipynb) | Dataset overview · metric definitions · weight system |

### Complete Data Tables (every record, every column)

| Notebook | Records |
|----------|---------|
| [01_tech_digital.ipynb](notebooks/01_tech_digital.ipynb) | 2,070 · IT & Digital · 46 occupations × 45 countries |
| [02_medical_health.ipynb](notebooks/02_medical_health.ipynb) | 5,490 · Medical & Health · 122 occupations × 45 countries |
| [03_finance_business.ipynb](notebooks/03_finance_business.ipynb) | 4,995 · Finance & Business · 111 occupations × 45 countries |
| [04_education_academia.ipynb](notebooks/04_education_academia.ipynb) | 2,790 · Education & Academia · 62 occupations × 45 countries |
| [05_engineering_manufacturing.ipynb](notebooks/05_engineering_manufacturing.ipynb) | 6,030 · Engineering & Manufacturing · 134 occupations × 45 countries |
| [06_gov_public.ipynb](notebooks/06_gov_public.ipynb) | 2,250 · Public Admin & Civil Service · 50 occupations × 45 countries |
| [07_legal_social.ipynb](notebooks/07_legal_social.ipynb) | 3,240 · Legal & Social Services · 72 occupations × 45 countries |
| [08_culture_arts_media.ipynb](notebooks/08_culture_arts_media.ipynb) | 9,000 · Culture, Arts & Media · 200 occupations × 45 countries |
| [09_transport_logistics.ipynb](notebooks/09_transport_logistics.ipynb) | 3,240 · Transport & Logistics · 72 occupations × 45 countries |
| [10_skilled_trades.ipynb](notebooks/10_skilled_trades.ipynb) | 4,680 · Skilled Trades & Crafts · 104 occupations × 45 countries |
| [11_service_consumer.ipynb](notebooks/11_service_consumer.ipynb) | 6,345 · Service & Consumer · 141 occupations × 45 countries |
| [12_agriculture_resources.ipynb](notebooks/12_agriculture_resources.ipynb) | 3,870 · Agriculture, Resources & Environment · 86 occupations × 45 countries |

### Rankings

| Notebook | Contents |
|----------|----------|
| [13_综合发展指数Top100.ipynb](notebooks/13_综合发展指数Top100.ipynb) | Global Top 100 · Top 10 per category · Top 10 per region · Bottom 50 |
| [14_AI抗性排行.ipynb](notebooks/14_AI抗性排行.ipynb) | Most AI-resistant Top 50 · Most vulnerable Top 50 · Timeline distribution |
| [15_性价比排行.ipynb](notebooks/15_性价比排行.ipynb) | Best ROI · By education level · By country |
| [16_稀缺度与移民价值.ipynb](notebooks/16_稀缺度与移民价值.ipynb) | Scarcest in developed countries · Highest mobility · Immigration fast-track |
| [17_生活质量排行.ipynb](notebooks/17_生活质量排行.ipynb) | Remote · Family · Low burnout · High autonomy · High fulfillment · Dream jobs |

### Trend Analysis

| Notebook | Contents |
|----------|----------|
| [18_2000-2026赢家与输家.ipynb](notebooks/18_2000-2026赢家与输家.ipynb) | Fastest rising vs declining careers |
| [19_AI冲击波分析.ipynb](notebooks/19_AI冲击波分析.ipynb) | AI replacement timelines · Category vulnerability |
| [20_各国职业结构演变.ipynb](notebooks/20_各国职业结构演变.ipynb) | Country trend comparisons · Industrial structure shifts |
| [21_供需失衡预警.ipynb](notebooks/21_供需失衡预警.ipynb) | Global oversupply vs shortage · Country labor gap alerts |

### 45 Country/Region Panoramas

[22_CN_中国职业全景.ipynb](notebooks/22_CN_中国职业全景.ipynb) ~ [66_EG_埃及职业全景.ipynb](notebooks/66_EG_埃及职业全景.ipynb) — China, USA, Japan, South Korea, Taiwan (China), Hong Kong (China), Singapore, Thailand, Vietnam, Indonesia, Malaysia, Philippines, India, Pakistan, Bangladesh, UAE, Israel, Saudi Arabia, Turkey, UK, France, Germany, Netherlands, Switzerland, Sweden, Denmark, Finland, Italy, Spain, Portugal, Poland, Czech Republic, Russia, Canada, Mexico, Brazil, Argentina, Chile, Colombia, Australia, New Zealand, South Africa, Nigeria, Kenya, Egypt

### Special Topics

| Notebook | Contents |
|----------|----------|
| [67_自媒体与内容创作者生态.ipynb](notebooks/67_自媒体与内容创作者生态.ipynb) | YouTuber · Blogger · Podcaster · Newsletter |
| [68_一人公司与自由职业.ipynb](notebooks/68_一人公司与自由职业.ipynb) | Indie developers · Freelance consultants · Solo founders |
| [69_网红与影响力经济.ipynb](notebooks/69_网红与影响力经济.ipynb) | KOL · Live commerce · Brand ambassadors |
| [70_直播产业全景.ipynb](notebooks/70_直播产业全景.ipynb) | Game streaming · E-commerce live · VTubers |
| [71_运动员与体育产业.ipynb](notebooks/71_运动员与体育产业.ipynb) | Professional athletes · Esports · Coaches |
| [72_平台零工与新型雇佣.ipynb](notebooks/72_平台零工与新型雇佣.ipynb) | Ride-hailing · Delivery · Fiverr / Upwork |
| [73_文化产业生态.ipynb](notebooks/73_文化产业生态.ipynb) | Film · Music · Publishing · Cultural creative |
| [74_query_tool.ipynb](notebooks/74_query_tool.ipynb) | Interactive query: find_jobs / compare / top_n / country_overview |

## Data Files

### Master Tables

| File | Records | Description |
|------|---------|-------------|
| `00_all_occupations.csv` | 54,000 | All occupations × all countries, sorted by composite index |
| `00_all_occupations_by_career.csv` | 1,200 | **By occupation**: 34-dim global means + 12 regional indices + best/worst country |
| `00_china_all_occupations.csv` | 1,200 | China edition |
| `00_china_vs_global.csv` | 1,200 | China scores vs global average + regional comparison |

### Category Data (in `data/csv/`)

| File | Records | Coverage |
|------|---------|----------|
| `tech_digital.csv` | 2,070 | TECH 46 × 45 |
| `medical_health.csv` | 5,490 | MED 122 × 45 |
| `finance_business.csv` | 4,995 | FIN 111 × 45 |
| `education_academia.csv` | 2,790 | EDU 62 × 45 |
| `engineering_manufacturing.csv` | 6,030 | ENG 134 × 45 |
| `gov_public.csv` | 2,250 | GOV 50 × 45 |
| `legal_social.csv` | 3,240 | LAW 72 × 45 |
| `culture_arts_media.csv` | 9,000 | ART 200 × 45 |
| `transport_logistics.csv` | 3,240 | TRA 72 × 45 |
| `skilled_trades.csv` | 4,680 | SKL 104 × 45 |
| `service_consumer.csv` | 6,345 | SVC 141 × 45 |
| `agriculture_resources.csv` | 3,870 | AGR 86 × 45 |

## Time Metadata

Every data record includes 3 time columns for AI agent maintenance:

| Column | Description | AI Agent Usage |
|--------|-------------|---------------|
| `generated_date` | When this data was generated | Data freshness; >6 months triggers calibration |
| `data_snapshot_date` | Scores reflect market state as of this date | Compare with current date for refresh decisions |
| `source_period` | Time span covered by source data | Understanding trend column semantics |

See `FLOW.md` for update decision rules.

## Color Scale

Score columns (0-10): `ratio = max(0, min(1, (score - 3) / 7))` → red → yellow → green, `rgba(r,g,b, 0.35)`

Reputation variance (0-5): Reversed — 0 = green (stable) → 5 = red (polarized)

## Machine-Readable

- `schema/SCHEMA.yaml` — 61-column schema with full definitions (AI agents: read this first)
- `schema/categories.yaml` — 1,200 occupation taxonomy tree
- `schema/weights.yaml` — Weight configuration
- `data/json/` — JSON mirror + meta/
- `mapping/country_meta.csv` — 45 country metadata

## Data Sources

| Source | Usage |
|--------|-------|
| ILO ILOSTAT | Employment stats, working hours, safety, gender, wages |
| OECD Employment Outlook | Employment protection, skills supply-demand |
| O*NET | Education requirements, skill transferability, work context |
| WEF Future of Jobs | AI replacement, emerging skills |
| McKinsey Global Institute | Automation potential, remote work |
| Oxford/Frey & Osborne | AI replacement probability |
| Glassdoor / Indeed | Reviews, salary, satisfaction |
| LinkedIn Economic Graph | Career paths, talent flows |
| Gallup World Poll | Job satisfaction, burnout |
| National labor statistics bureaus | Country-specific data |
| National immigration shortage lists | Developed country scarcity |
