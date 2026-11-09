"""Unit test cho scripts/measure.py — chạy: python3 -m unittest discover -s scripts/tests -p 'test_*.py'."""
import contextlib
import io
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import measure  # noqa: E402

FIX = os.path.join(HERE, "fixtures", "metrics")


def run_json(*args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        measure.main(["--runs", os.path.join(FIX, "runs.jsonl"), "--feedback", os.path.join(FIX, "feedback.jsonl"),
                      "--json", *args])
    return json.loads(buf.getvalue())


class Stats(unittest.TestCase):
    def test_median_ignores_non_numbers(self):
        self.assertEqual(measure.median([3, None, "x", 1, 2]), 2)
        self.assertIsNone(measure.median([None]))

    def test_mad(self):
        self.assertEqual(measure.mad([1, 2, 3, 4, 100]), 1)

    def test_slope_sign(self):
        self.assertEqual(measure.slope_sign([1, 2, 3]), 1)
        self.assertEqual(measure.slope_sign([3, 2, 1]), -1)
        self.assertEqual(measure.slope_sign([2, 2, 2]), 0)
        self.assertEqual(measure.slope_sign([5]), 0)


class Scoring(unittest.TestCase):
    def test_slow_subject_scores_lower_and_is_anomalous(self):
        rows = {("agent:a", "M"): {"duration_s": 100, "turns": 10},
                ("agent:b", "M"): {"duration_s": 110, "turns": 11},
                ("agent:c", "M"): {"duration_s": 105, "turns": 10},
                ("agent:d", "M"): {"duration_s": 900, "turns": 50}}
        measure.score(rows)
        self.assertLess(rows[("agent:d", "M")]["score"], rows[("agent:a", "M")]["score"])
        self.assertIn("duration_s", rows[("agent:d", "M")]["anomalies"])
        self.assertEqual(rows[("agent:a", "M")]["anomalies"], [])

    def test_sizes_are_compared_separately(self):
        rows = {("agent:a", "S"): {"duration_s": 10}, ("agent:b", "S"): {"duration_s": 12},
                ("agent:a", "L"): {"duration_s": 1000}, ("agent:b", "L"): {"duration_s": 1100}}
        measure.score(rows)
        self.assertGreater(rows[("agent:a", "L")]["score"], rows[("agent:b", "L")]["score"])


class EndToEnd(unittest.TestCase):
    def test_ranking_puts_anomaly_first(self):
        top = run_json()["ranking"][0]
        self.assertEqual((top["subject"], top["size"]), ("agent:team:tech-lead", "M"))
        self.assertTrue(top["anomalies"])
        self.assertEqual(top["trend"], 1)
        self.assertEqual(top["feedback"], 2)

    def test_deterministic(self):
        self.assertEqual(run_json(), run_json())

    def test_since_filters_runs(self):
        subjects = {r["subject"] for r in run_json("--since", "2026-11-08")["ranking"]}
        self.assertNotIn("agent:team:tech-lead", subjects)

    def test_missing_inputs_do_not_crash(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = measure.main(["--runs", "/nonexistent", "--feedback", "/nonexistent", "--scorecard", "/nonexistent"])
        self.assertEqual(code, 0)
        self.assertIn("chưa có số liệu", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
