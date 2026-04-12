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
