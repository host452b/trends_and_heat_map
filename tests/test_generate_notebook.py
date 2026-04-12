"""Tests for generate_notebook.py."""
import json
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
        assert len(data["cells"]) >= 2

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
