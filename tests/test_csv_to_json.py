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
