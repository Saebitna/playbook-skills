import unittest

from src.tags import primary_tag


class PrimaryTagTest(unittest.TestCase):
    def test_primary_tag_picks_highest(self):
        self.assertEqual(primary_tag(["pri:high", "pri:low", "other"]), "pri:high")
