import os
import sys
import unittest


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DISCOVERY_DIR = os.path.join(ROOT, "descubrimiento")
if DISCOVERY_DIR not in sys.path:
    sys.path.insert(0, DISCOVERY_DIR)

import run_discovery  # noqa: E402


class RunDiscoveryHelpersTests(unittest.TestCase):
    def test_parse_date_valid_formats(self):
        d1 = run_discovery._parse_date("2026-05-22")
        d2 = run_discovery._parse_date("2026/05/22")
        self.assertIsNotNone(d1)
        self.assertEqual(d1, d2)

    def test_parse_date_invalid(self):
        self.assertIsNone(run_discovery._parse_date("22-05-2026"))
        self.assertIsNone(run_discovery._parse_date(""))
        self.assertIsNone(run_discovery._parse_date(None))

    def test_safe_slug_normaliza_acentos_y_espacios(self):
        self.assertEqual(run_discovery._safe_slug("México Centro"), "mexico_centro")
        self.assertEqual(run_discovery._safe_slug("  "), "__")

    def test_dedupe_rows_por_id_y_permalink(self):
        rows = [
            {"id": "abc", "permalink": "u/1", "name": "A"},
            {"id": "abc", "permalink": "u/1", "name": "A duplicado"},
            {"id": "def", "permalink": "u/2", "name": "B"},
        ]
        deduped = run_discovery._dedupe_rows(rows)
        self.assertEqual(len(deduped), 2)
        self.assertEqual(deduped[0]["name"], "A")
        self.assertEqual(deduped[1]["id"], "def")

    def test_filter_by_publication_date(self):
        rows = [
            {"id": "1", "publication_date": "2024-01-15T10:00:00"},
            {"id": "2", "publication_date": "2023-12-31T23:59:59"},
            {"id": "3", "publication_date": "2024-05-20T00:00:00Z"},
        ]
        filtered = run_discovery._filter_by_publication_date(rows, "2024-01-01", "2024-12-31")
        ids = [r["id"] for r in filtered]
        self.assertEqual(ids, ["1", "3"])


if __name__ == "__main__":
    unittest.main()
