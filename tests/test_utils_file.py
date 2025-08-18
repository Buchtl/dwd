import unittest
from pathlib import Path

from src import utils_file

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_PATH: Path = PROJECT_ROOT / "tests" / "fixtures" 


class TestUtilsFile(unittest.TestCase):
    def test_parse_csv_from_file(self):
        actual = utils_file.read_file(FIXTURES_PATH / "produkt_zehn_min_tu_20200101_20241231_00191.txt")[:22]
        expected = "STATIONS_ID;MESS_DATUM"
        self.assertEqual(actual, expected)
