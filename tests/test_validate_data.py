"""Tests for validate_data.py."""
import os
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
        path = os.path.join(str(tmpdir), "test.csv")
        pd.DataFrame(rows).to_csv(path, index=False)
        return path

    def _full_row(self):
        """Create a valid row with all 58 columns."""
        row = {
            "id": "TECH-0101-CN-general", "major_category": "信息技术与数字化",
            "major_code": "TECH", "mid_category": "软件开发",
            "sub_category": "前端工程师", "sub_category_en": "Front-end Engineer",
            "isco_code": "2514", "onet_code": "15-1254.00",
            "region": "东亚", "country_or_region": "中国",
            "iso_code": "CN", "type": "country", "employer_type": "general",
            "typical_education": "本科", "typical_entry_age": "22-26岁",
            "locality": "global",
        }
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
        row.update({
            "trend_2000_2026": 3, "trend_5yr": 1,
            "demand_direction": "↑", "ai_timeline": "2030-2035",
            "composite_index": 6.5, "summary_zh": "测试",
            "summary_en": "Test", "data_source": "test",
        })
        return row

    def test_valid_row_no_errors(self, schema_path, tmp_path):
        row = self._full_row()
        path = self._make_csv([row], tmp_path)
        errors = validate_csv(path, schema_path)
        assert errors == []

    def test_missing_column_reports_error(self, schema_path, tmp_path):
        path = self._make_csv([{"id": "TECH-0101-CN-general"}], tmp_path)
        errors = validate_csv(path, schema_path)
        assert any("Missing column" in e for e in errors)

    def test_score_out_of_range_reports_error(self, schema_path, tmp_path):
        row = self._full_row()
        row["learning_cost"] = 15.0  # out of range!
        path = self._make_csv([row], tmp_path)
        errors = validate_csv(path, schema_path)
        assert any("learning_cost" in e and "out of range" in e for e in errors)

    def test_invalid_enum_reports_error(self, schema_path, tmp_path):
        row = self._full_row()
        row["type"] = "invalid_type"  # not in enum
        path = self._make_csv([row], tmp_path)
        errors = validate_csv(path, schema_path)
        assert any("type" in e and "invalid" in e.lower() for e in errors)
