import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import plan


def row(h, patches, reboot="no"):
    return {"host": h, "critical_patches": str(patches), "reboot_required": reboot}


class TestPatchWindow(unittest.TestCase):
    def test_reboot_first(self):
        scheduled, _, _ = plan([row("a", 0), row("b", 0, "yes")], 120)
        self.assertEqual(scheduled[0], "b")

    def test_overflow_when_window_full(self):
        scheduled, overflow, used = plan([row("a", 50), row("b", 50)], 120)
        self.assertEqual(overflow, ["b"])
        self.assertEqual(used, 105)

    def test_cost_formula(self):
        _, _, used = plan([row("a", 5)], 120)
        self.assertEqual(used, 15)
