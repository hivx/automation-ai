"""Unit tests for scripts/check-claude-md.py — run: python3 -m unittest discover -s scripts/tests -p 'test_*.py'."""
import contextlib
import importlib.util
import io
import os
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location("check_claude_md", os.path.join(KIT, "scripts", "check-claude-md.py"))
ccm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ccm)

PROJECT = "<!-- project:start -->\n# Shop\nOrders and invoices.\n## Layout\n- `src/orders/` — order flow\n- `src/app.py` — entry\n<!-- project:end -->\n"
TEAM = "<!-- team:start -->\n## Working with the AI team\n- `/team:status`\n<!-- team:end -->\n"


class CheckClaudeMd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        os.makedirs(os.path.join(self.root, "src", "orders"))
        open(os.path.join(self.root, "src", "app.py"), "w").close()

    def tearDown(self):
        self.tmp.cleanup()

    def run_on(self, text):
        if text is not None:
            with open(os.path.join(self.root, "CLAUDE.md"), "w", encoding="utf-8") as fh:
                fh.write(text)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = ccm.main(["--root", self.root])
        return rc, buf.getvalue()

    def test_good_file_passes(self):
        rc, out = self.run_on("# notes kept by the human\n\n" + PROJECT + "\n" + TEAM)
        self.assertEqual(rc, 0, out)
        self.assertIn("project 5/150, team 2/25", out)

    def test_missing_file(self):
        rc, out = self.run_on(None)
        self.assertEqual(rc, 1)
        self.assertIn("missing", out)

    def test_team_block_only_fails(self):
        rc, out = self.run_on(TEAM)
        self.assertEqual(rc, 1)
        self.assertIn("project block: expected one", out)

    def test_stale_path_is_reported(self):
        rc, out = self.run_on(PROJECT.replace("src/orders/", "src/legacy_orders/") + TEAM)
        self.assertEqual(rc, 1)
        self.assertIn("`src/legacy_orders/` does not exist", out)

    def test_non_paths_are_ignored(self):
        body = PROJECT.replace("Orders and invoices.", "Branch `origin/main`, version `1.2.0`, flag `--fast`, key `cmd.test`.")
        rc, out = self.run_on(body + TEAM)
        self.assertEqual(rc, 0, out)

    def test_placeholder_left(self):
        rc, out = self.run_on(PROJECT.replace("# Shop", "# <fill: project name>") + TEAM)
        self.assertEqual(rc, 1)
        self.assertIn("placeholder left", out)

    def test_order_and_budget(self):
        rc, out = self.run_on(TEAM + PROJECT)
        self.assertIn("project block must come before", out)
        big = PROJECT.replace("Orders and invoices.\n", "x\n" * 151)
        rc, out = self.run_on(big + TEAM)
        self.assertEqual(rc, 1)
        self.assertIn("lines > 150", out)


if __name__ == "__main__":
    unittest.main()
