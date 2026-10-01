import unittest

from linuxrevive.maintenance import temporary_locations


class MaintenanceTests(unittest.TestCase):
    def test_temporary_locations_contains_system_tmp(self):
        self.assertIn("/tmp", {str(path) for path in temporary_locations()})


if __name__ == "__main__":
    unittest.main()
