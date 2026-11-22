import unittest
import studio as S
import workspace_model as WM


class NumericLimits(unittest.TestCase):
    def test_values_beyond_screen_are_kept(self):
        l = S.normalize_layer({"kind": "text", "x": -3, "y": 7.5, "w": 4, "h": 2.5, "size": 1.2})
        self.assertEqual((l["x"], l["y"], l["w"], l["h"], l["size"]), (-3, 7.5, 4, 2.5, 1.2))

    def test_garbage_falls_back(self):
        l = S.normalize_layer({"kind": "text", "x": float("inf"), "w": "abc", "h": float("nan")})
        self.assertEqual((l["x"], l["w"], l["h"]), (0.1, 0.8, 0.2))

    def test_video_box_and_layers_only_cells_exist(self):
        self.assertIn("media.box", WM.panel_items("group:media"))
        self.assertIn("text.sendonly", WM.panel_items("group:text"))
        self.assertTrue(WM.is_valid("action:send_layers")); self.assertIn("project.rbg", WM.panel_items("group:project"))


if __name__ == "__main__":
    unittest.main()


class FitLayer(unittest.TestCase):
    def test_layer_is_pulled_inside_the_screen(self):
        l = S.fit_layer({"x": 0.9, "y": -0.3, "w": 0.5, "h": 4})
        self.assertEqual((l["w"], l["h"]), (0.5, 1.0))
        self.assertAlmostEqual(l["x"], 0.5); self.assertEqual(l["y"], 0.0)

    def test_inside_layer_is_untouched(self):
        l = S.fit_layer({"x": 0.1, "y": 0.2, "w": 0.3, "h": 0.4})
        self.assertEqual((l["x"], l["y"], l["w"], l["h"]), (0.1, 0.2, 0.3, 0.4))


class Timing(unittest.TestCase):
    def test_delay_and_exit_speed(self):
        l = S.normalize_layer({"kind": "text", "delay": 5, "dur_out": 2.5, "dur": 12})
        self.assertEqual((l["delay"], l["dur_out"], l["dur"]), (5.0, 2.5, 12.0))
        l = S.normalize_layer({"kind": "text", "delay": -3, "dur_out": 99})
        self.assertEqual((l["delay"], l["dur_out"]), (0.0, 30.0))
