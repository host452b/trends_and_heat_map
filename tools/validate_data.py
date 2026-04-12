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

    # 2. Check score ranges (float columns with range)
    for col_name, col_def in col_defs.items():
        if col_def.get("type") == "float" and "range" in col_def:
            vmin, vmax = col_def["range"]
            out = df[(df[col_name] < vmin) | (df[col_name] > vmax)]
            if len(out) > 0:
                errors.append(f"{col_name}: {len(out)} values out of range [{vmin}, {vmax}]")

    # 3. Check integer ranges (trend columns)
    for col_name, col_def in col_defs.items():
        if col_def.get("type") == "integer" and "range" in col_def:
            vmin, vmax = col_def["range"]
            numeric = pd.to_numeric(df[col_name], errors="coerce")
            out = numeric[(numeric < vmin) | (numeric > vmax)]
            if len(out.dropna()) > 0:
                errors.append(f"{col_name}: {len(out.dropna())} values out of range [{vmin}, {vmax}]")

    # 4. Check enum values
    for col_name, col_def in col_defs.items():
        if "enum" in col_def:
            allowed = set(col_def["enum"])
            invalid = df[~df[col_name].isin(allowed)]
            if len(invalid) > 0:
                bad_vals = invalid[col_name].unique().tolist()
                errors.append(f"{col_name}: invalid values {bad_vals} (allowed: {sorted(allowed)})")

    return errors
