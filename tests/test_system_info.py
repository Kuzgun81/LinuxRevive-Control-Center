import unittest

from linuxrevive.system_info import _bytes, _uptime


class FormattingTests(unittest.TestCase):
    def test_bytes_uses_human_readable_units(self):
        self.assertEqual(_bytes(1024), "1.0 KB")

    def test_uptime_includes_hours_and_minutes(self):
        self.assertEqual(_uptime(3660), "1 saat, 1 dakika")


if __name__ == "__main__":
    unittest.main()
