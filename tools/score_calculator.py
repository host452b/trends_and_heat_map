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
