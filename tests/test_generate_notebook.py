"""Tests for generate_notebook.py."""
import json
import re
import pytest
import pandas as pd
from tools.generate_notebook import (
    create_data_notebook,
    score_to_style,
    variance_to_style,
    trend_to_style,
    render_html_table,
    SCORE_COLUMNS,
    TREND_COLUMNS,
)


# ---------------------------------------------------------------------------
# Color function tests
# ---------------------------------------------------------------------------

class TestScoreToStyle:
    def test_returns_rgba_string(self):
        result = score_to_style(5.0)
        assert result.startswith("background-color: rgba(")
        assert result.endswith(")")

    def test_valid_rgba_format(self):
        result = score_to_style(7.0)
        match = re.search(r"rgba\((\d+),(\d+),(\d+), 0\.35\)", result)
        assert match, f"Invalid rgba format: {result}"
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255

    def test_low_score_reddish(self):
        """Score 0 should produce a red-ish color (high R, low G)."""
        result = score_to_style(0)
        match = re.search(r"rgba\((\d+),(\d+),(\d+)", result)
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        assert r > g, f"Expected red > green for score 0, got r={r} g={g}"

    def test_high_score_greenish(self):
        """Score 10 should produce a green-ish color (low R, high G)."""
        result = score_to_style(10)
        match = re.search(r"rgba\((\d+),(\d+),(\d+)", result)
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        assert g > r, f"Expected green > red for score 10, got r={r} g={g}"

    def test_clamps_below_zero(self):
        """Scores below vmin should still return valid rgba."""
        result = score_to_style(-2)
        assert "rgba(" in result

    def test_clamps_above_max(self):
        """Scores above vmax should still return valid rgba."""
        result = score_to_style(15)
        assert "rgba(" in result


class TestVarianceToStyle:
    def test_zero_variance_greenish(self):
        """Variance 0 (stable) should be green-ish."""
        result = variance_to_style(0)
        match = re.search(r"rgba\((\d+),(\d+),(\d+)", result)
        r, g = int(match.group(1)), int(match.group(2))
        assert g > r, f"Variance 0 should be green, got r={r} g={g}"

    def test_high_variance_reddish(self):
        """Variance 5 (polarized) should be red-ish."""
        result = variance_to_style(5)
        match = re.search(r"rgba\((\d+),(\d+),(\d+)", result)
        r, g = int(match.group(1)), int(match.group(2))
        assert r > g, f"Variance 5 should be red, got r={r} g={g}"

    def test_returns_valid_rgba(self):
        result = variance_to_style(2.5)
        assert "background-color: rgba(" in result


class TestTrendToStyle:
    def test_negative_trend_reddish(self):
        """Trend -5 should be red-ish."""
        result = trend_to_style(-5)
        match = re.search(r"rgba\((\d+),(\d+),(\d+)", result)
        r, g = int(match.group(1)), int(match.group(2))
        assert r > g, f"Trend -5 should be red, got r={r} g={g}"

    def test_positive_trend_greenish(self):
        """Trend +5 should be green-ish."""
        result = trend_to_style(5)
        match = re.search(r"rgba\((\d+),(\d+),(\d+)", result)
        r, g = int(match.group(1)), int(match.group(2))
        assert g > r, f"Trend +5 should be green, got r={r} g={g}"

    def test_returns_valid_rgba(self):
        result = trend_to_style(0)
        assert "background-color: rgba(" in result


# ---------------------------------------------------------------------------
# HTML table rendering tests
# ---------------------------------------------------------------------------

class TestRenderHtmlTable:
    def _sample_df(self, n_rows=5):
        rows = []
        for i in range(n_rows):
            rows.append({
                "id": f"TEST-{i:04d}",
                "sub_category": f"Job {i}",
                "learning_cost": round(2 + i * 1.5, 1),
                "ai_resistance": round(3 + i * 0.8, 1),
                "reputation_variance": round(i * 0.5, 1),
                "trend_2000_2026": round(-2 + i * 1.0, 1),
                "trend_5yr": round(-1 + i * 0.5, 1),
                "composite_index": round(4 + i * 0.7, 1),
            })
        return pd.DataFrame(rows)

    def test_returns_list(self):
        df = self._sample_df(5)
        pages = render_html_table(df)
        assert isinstance(pages, list)
        assert len(pages) == 1

    def test_html_contains_table_tag(self):
        df = self._sample_df(3)
        pages = render_html_table(df)
        assert "<table" in pages[0]
        assert "</table>" in pages[0]

    def test_html_contains_header(self):
        df = self._sample_df(3)
        pages = render_html_table(df)
        assert "<th" in pages[0]
        assert "learning_cost" in pages[0]

    def test_html_contains_colored_cells(self):
        df = self._sample_df(3)
        pages = render_html_table(df)
        assert "rgba(" in pages[0]

    def test_pagination_splits_correctly(self):
        df = self._sample_df(150)
        pages = render_html_table(df, page_size=60)
        assert len(pages) == 3  # 60 + 60 + 30

    def test_pagination_single_page(self):
        df = self._sample_df(10)
        pages = render_html_table(df, page_size=60)
        assert len(pages) == 1

    def test_each_page_has_header_row(self):
        df = self._sample_df(80)
        pages = render_html_table(df, page_size=60)
        for page in pages:
            assert "<th" in page

    def test_no_color_on_text_columns(self):
        """Text columns like 'id' should not get rgba coloring."""
        df = self._sample_df(3)
        pages = render_html_table(df)
        html = pages[0]
        # Find all <td> cells for the 'id' column (first data column)
        # The id values like TEST-0000 should not have rgba
        for i in range(3):
            marker = f"TEST-{i:04d}"
            idx = html.index(marker)
            # Check the <td preceding this value
            td_start = html.rfind("<td", 0, idx)
            td_snippet = html[td_start:idx]
            assert "rgba(" not in td_snippet


# ---------------------------------------------------------------------------
# Notebook structure tests
# ---------------------------------------------------------------------------

class TestCreateDataNotebook:
    def _make_csv(self, rows, path):
        pd.DataFrame(rows).to_csv(path, index=False)

    def _sample_rows(self, n=3):
        rows = []
        for i in range(n):
            row = {
                "id": f"TECH-{i:04d}-CN",
                "major_code": "TECH",
                "sub_category": f"Job{i}",
                "country_or_region": "China" if i % 2 == 0 else "Japan",
                "composite_index": round(5 + i * 0.5, 1),
                "reputation_variance": round(1 + i * 0.3, 1),
                "trend_2000_2026": round(-1 + i, 1),
                "trend_5yr": round(0.5 * i, 1),
            }
            for col in SCORE_COLUMNS:
                if col not in row:
                    row[col] = round(3 + i * 0.5, 1)
            rows.append(row)
        return rows

    def test_creates_ipynb_file(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        self._make_csv(self._sample_rows(), csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="Test Notebook")
        assert nb_path.exists()

    def test_ipynb_is_valid_json(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        self._make_csv(self._sample_rows(), csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="Test")
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        assert data["nbformat"] == 4

    def _source_text(self, cell):
        """Join cell source (may be str or list of str)."""
        src = cell["source"]
        return "".join(src) if isinstance(src, list) else src

    def _output_text(self, cell, idx=0):
        """Join output text (may be str or list of str)."""
        out = cell["outputs"][idx]
        text = out.get("text", "") or out.get("data", {}).get("text/html", "")
        return "".join(text) if isinstance(text, list) else text

    def test_first_cell_is_markdown_title(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        self._make_csv(self._sample_rows(), csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="My Title")
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        first = data["cells"][0]
        assert first["cell_type"] == "markdown"
        assert "My Title" in self._source_text(first)

    def test_second_cell_has_record_count(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        rows = self._sample_rows(5)
        self._make_csv(rows, csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="Test")
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        second = data["cells"][1]
        assert second["cell_type"] == "code"
        output_text = self._output_text(second)
        assert "5" in output_text  # 5 records

    def test_page_cells_have_html_output(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        self._make_csv(self._sample_rows(), csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="Test")
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        # Cell index 2 should be first page
        page_cell = data["cells"][2]
        assert page_cell["cell_type"] == "code"
        assert page_cell["outputs"][0]["output_type"] == "display_data"
        html = self._output_text(page_cell)
        assert "<table" in html
        assert "rgba(" in html

    def test_last_cell_has_summary(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        self._make_csv(self._sample_rows(), csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="Test")
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        last = data["cells"][-1]
        assert last["cell_type"] == "code"
        output_text = self._output_text(last)
        assert "Score Summary" in output_text

    def test_pagination_many_rows(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        rows = self._sample_rows(130)
        self._make_csv(rows, csv_path)
        create_data_notebook(str(csv_path), str(nb_path), title="Test")
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        # 1 markdown + 1 stats + 3 pages (60+60+10) + 1 summary = 6
        code_cells = [c for c in data["cells"] if c["cell_type"] == "code"]
        page_cells = [
            c for c in code_cells
            if c["outputs"]
            and c["outputs"][0].get("output_type") == "display_data"
        ]
        assert len(page_cells) == 3

    def test_description_in_markdown(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        nb_path = tmp_path / "test.ipynb"
        self._make_csv(self._sample_rows(), csv_path)
        create_data_notebook(
            str(csv_path), str(nb_path),
            title="T", description="Custom description here"
        )
        data = json.loads(nb_path.read_text(encoding="utf-8"))
        assert "Custom description here" in self._source_text(data["cells"][0])


# ---------------------------------------------------------------------------
# SCORE_COLUMNS sanity
# ---------------------------------------------------------------------------

class TestScoreColumns:
    def test_has_34_score_columns(self):
        assert len(SCORE_COLUMNS) == 34

    def test_includes_key_columns(self):
        assert "learning_cost" in SCORE_COLUMNS
        assert "ai_resistance" in SCORE_COLUMNS
        assert "reputation_variance" in SCORE_COLUMNS
