# Changelog

## [1.1.0] - 2026-04-13
### Added
- Time metadata on all data files: `generated_date`, `data_snapshot_date`, `source_period`
- SCHEMA.yaml v1.1.0: dataset-level time metadata + AI agent maintenance notes
- FLOW.md: update decision rules (6mo calibrate, 12mo full refresh, anchor triggers)
- China edition: `00_china_all_occupations.csv` + `00_china_vs_global.csv` + notebook
- Occupation master table: `00_all_occupations_by_career.csv` (1,200 rows, 34-dim global means + 12 regional indices)
- Full master table: `00_all_occupations.csv` (54,000 rows sorted by composite index)

### Changed
- All CSVs now 61 columns (was 58), adding 3 time metadata columns
- Notebook generator rewritten: pre-rendered HTML with inline rgba color scale (GitHub-renderable)

## [1.0.0] - 2026-04-13
### Added
- Complete data for all 12 categories: 54,000 rows × 61 columns × 45 countries
  - TECH (2,070) · MED (5,490) · FIN (4,995) · EDU (2,790) · ENG (6,030)
  - GOV (2,250) · LAW (3,240) · ART (9,000) · TRA (3,240) · SKL (4,680)
  - SVC (6,345) · AGR (3,870)
- 76 Jupyter notebooks with pre-rendered HTML color heatmaps:
  - 1 overview + 1 master table + 1 China edition
  - 12 category data notebooks (1:1)
  - 5 ranking notebooks (Top100, AI, cost-perf, scarcity, life quality)
  - 4 trend notebooks (winners/losers, AI wave, structure, supply-demand)
  - 45 country panorama notebooks
  - 7 special topic notebooks (new media, solo biz, KOL, streaming, sports, gig, culture)
  - 1 query tool notebook
- 12 JSON mirror files + 4 meta files
- Data generator scripts for all 12 categories (`tools/gen_*_data.py`)

## [0.1.0] - 2026-04-12
### Added
- Project infrastructure: schema (SCHEMA.yaml, weights.yaml, categories.yaml), mappings
- 1,200 occupations across 12 categories in taxonomy
- TECH category pilot: 2,070 rows × 58 columns × 45 countries
- Python tools: score_calculator, validate_data, csv_to_json, generate_notebook
- 30 automated tests
- Documentation: README (zh/en), FLOW.md
