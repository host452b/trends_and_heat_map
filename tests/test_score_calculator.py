"""Tests for score_calculator.py."""
import pytest
from tools.score_calculator import (
    load_weights, normalize_variance, calculate_composite, REVERSE_DIMENSIONS
)


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
        # All dims at their optimal (best) raw value.
        # Regular dims: 10 (higher=better). Reverse dims: 0 (lower=better).
        scores = {dim: 10.0 for dim in weights}
        for dim in REVERSE_DIMENSIONS:
            scores[dim] = 0.0
        scores["reputation_variance"] = 0
        result = calculate_composite(scores, weights)
        assert result == 10.0

    def test_all_zeros_returns_zero(self, weights_path):
        weights = load_weights(weights_path)
        # All dims at their worst raw value.
        # Regular dims: 0 (lower=worse). Reverse dims: 10 (higher=worse).
        scores = {dim: 0.0 for dim in weights}
        for dim in REVERSE_DIMENSIONS:
            scores[dim] = 10.0
        scores["reputation_variance"] = 5
        result = calculate_composite(scores, weights)
        assert result == 0.0

    def test_reverse_dimensions_are_inverted(self, weights_path):
        weights = load_weights(weights_path)
        scores = {dim: 5.0 for dim in weights}
        scores["reputation_variance"] = 2.5
        result_baseline = calculate_composite(scores, weights)

        scores["learning_cost"] = 10.0
        result_high_cost = calculate_composite(scores, weights)
        assert result_high_cost < result_baseline

    def test_result_in_valid_range(self, weights_path):
        weights = load_weights(weights_path)
        scores = {dim: 7.0 for dim in weights}
        scores["reputation_variance"] = 1.5
        result = calculate_composite(scores, weights)
        assert 0 <= result <= 10
