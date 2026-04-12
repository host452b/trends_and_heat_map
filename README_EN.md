# Global Career Development Index

A multi-dimensional career scoring database. **1,200 occupations · 45 countries/regions · 34 quantitative metrics · 58 columns · multi-source calibrated**

## Visual Reports (Click to View)

| Notebook | Contents |
|----------|----------|
| [00_数据总览.ipynb](notebooks/00_数据总览.ipynb) | Dataset overview · metric explanations · weight system |
| [01_tech_digital.ipynb](notebooks/01_tech_digital.ipynb) | IT & Digital · 46 occupations × 45 countries · red-green heatmap |

> 11 remaining categories, leaderboards, trend topics, and 45-country panoramic notebooks coming soon.

## Data Files

### Completed

| File | Records | Coverage |
|------|---------|----------|
| `data/csv/tech_digital.csv` | 2,070 | 46 TECH occupations × 45 countries |
| `data/json/tech_digital.json` | 2,070 | JSON mirror |

### Coming Soon (Plans 2-12)

| File | Est. Records | Coverage |
|------|-------------|----------|
| `medical_health.csv` | ~5,400 | MED 122 occupations × 45 countries |
| `finance_business.csv` | ~4,950 | FIN 111 occupations × 45 countries |
| `education_academia.csv` | ~2,790 | EDU 62 occupations × 45 countries |
| `engineering_manufacturing.csv` | ~6,030 | ENG 134 occupations × 45 countries |
| `gov_public.csv` | ~2,250 | GOV 50 occupations × 45 countries |
| `legal_social.csv` | ~3,240 | LAW 72 occupations × 45 countries |
| `culture_arts_media.csv` | ~9,000 | ART 200 occupations × 45 countries |
| `transport_logistics.csv` | ~3,240 | TRA 72 occupations × 45 countries |
| `skilled_trades.csv` | ~4,680 | SKL 104 occupations × 45 countries |
| `service_consumer.csv` | ~6,345 | SVC 141 occupations × 45 countries |
| `agriculture_resources.csv` | ~3,870 | AGR 86 occupations × 45 countries |

## Quantitative Metrics (0-10 Scale)

### Entry Barrier (6%)

| Metric | Score 0 | Score 10 | Weight |
|--------|---------|---------|--------|
| Prior learning cost | No training needed | 10+ years specialized training | 3% |
| Education requirement | No degree required | PhD required | 3% |

### Growth Potential (10%)

| Metric | Score 0 | Score 10 | Weight |
|--------|---------|---------|--------|
| Career growth coefficient | No advancement path | Extremely high ceiling | 4% |
| Career longevity | Obsolete in <5 years | More valuable with age | 3% |
| Career opportunity | Sunset industry | Explosive growth sector | 3% |

### Market Landscape (10%)

| Metric | Score 0 | Score 10 | Weight |
|--------|---------|---------|--------|
| Market size | Extremely niche | Tens of millions globally | 2% |
| Supply-demand balance | Severe oversupply | Severe shortage | 4% |
| Developed-country scarcity | No shortage | Fast-track immigration path | 4% |

### Income & Returns (9%)

| Metric | Score 0 | Score 10 | Weight |
|--------|---------|---------|--------|
| Value-added level | Minimum wage | Top salary + equity | 5% |
| Cost-effectiveness | High input, low return | Low input, high return | 4% |

### Stability & Risk (15%)

| Metric | Score 0 | Score 10 | Weight |
|--------|---------|---------|--------|
| Job stability | Layoffs anytime | Iron rice bowl | 4% |
| Safety factor | Lethal hazards | Zero risk | 3% |
| Occupational disease risk | High incidence | Virtually none | 2% |
| Overtime intensity | Extreme 996 | On time every day | 3% |
| Burnout level | Extreme burnout | Fulfilling and joyful | 3% |

### Reputation & Transferability (9%)

| Metric | Score 0 | Score 10 | Weight |
|--------|---------|---------|--------|
| Skill transferability | Non-transferable | Universal skills | 3% |
| Career-switching ease | Cannot change careers | Switch anytime | 3% |
| Reputation variance | Polarized (5) | Consistently positive (0) | 3% |

### Future Outlook (6%)

| Metric | Score 0 | Score 10 | Weight |
|--------|---------|---------|--------|
| AI displacement risk | Imminent replacement | Completely unaffected | 6% |

### Quality of Life (15%)

| Metric | Score 0 | Score 10 | Weight |
|--------|---------|---------|--------|
| Social status | Bottom tier | Extremely high | 3% |
| Remote-work friendliness | Must be on-site | 100% remote | 3% |
| Autonomy | Fully controlled | Fully autonomous | 3% |
| Family friendliness | Incompatible | Perfect balance | 3% |
| Sense of achievement | No meaning | Extremely high mission | 3% |

### Structural Flexibility (20%)

| Metric | Score 0 | Score 10 | Weight |
|--------|---------|---------|--------|
| Entrepreneurship rate | Nobody starts businesses | Many successful startups | 2% |
| Gender equality | Extreme imbalance | Fully equal | 2% |
| Age entry flexibility | Fresh graduates only | Any age welcome | 2% |
| Social interaction | Completely solo | High-frequency collaboration | 2% |
| Physical demand | Pure cognitive | Heavy physical labor | 1% |
| Policy/licensing barriers | No barrier | National-level license | 2% |
| Economic cycle sensitivity | Recession-proof | Highly volatile | 2% |
| Side-job compatibility | Prohibited | Freely moonlightable | 2% |
| International mobility | Not mutually recognized | Globally portable | 3% |
| Industry monopolization | Free competition | Complete monopoly | 2% |

### Reputation Variance Interpretation

- **0-1.5 (Green)** = Stable ratings; experience in this country is predictable
- **1.5-2.5 (Yellow)** = Mostly positive; some differing views
- **2.5-5 (Red)** = Polarized; experience depends on employer/city/individual

## Tools

| Tool | Purpose |
|------|---------|
| `tools/score_calculator.py` | Weighted composite career index calculation |
| `tools/validate_data.py` | CSV data validation |
| `tools/csv_to_json.py` | CSV → JSON mirror conversion |
| `tools/generate_notebook.py` | Auto-generate red-green heatmap notebooks |

## Data Sources

| Source | Usage |
|--------|-------|
| ILO ILOSTAT | Employment stats, working hours, safety, gender, wages |
| OECD Employment Outlook | Employment protection, skill supply/demand, hours |
| O*NET | Education requirements, skill transferability, work environment |
| WEF Future of Jobs | AI displacement, emerging skills |
| McKinsey Global Institute | Automation potential, remote work |
| Glassdoor / Indeed | Reputation, salaries, satisfaction |
| LinkedIn Economic Graph | Career paths, talent mobility |
| National labor statistics bureaus | Country-specific data |

## Machine-Readable

- `schema/SCHEMA.yaml` — Full 58-column definitions
- `schema/categories.yaml` — 1,200 occupation taxonomy tree
- `schema/weights.yaml` — Weight configuration
- `data/json/` — JSON mirror + meta/
- `mapping/country_meta.csv` — 45-country metadata
