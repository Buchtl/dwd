import unittest
from pathlib import Path

from src import utils_file

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_PATH: Path = PROJECT_ROOT / "tests" / "fixtures" 


class TestUtilsFile(unittest.TestCase):
    def test_read_file(self):
        actual = utils_file.read_file(FIXTURES_PATH / "produkt_zehn_min_tu_20200101_20241231_00191.txt")[:22]
        expected = "STATIONS_ID;MESS_DATUM"
        self.assertEqual(actual, expected)

    def test_read_zip(self):
        actual = next(iter(utils_file.read_zip_as_strings(FIXTURES_PATH / "10minutenwerte_TU_00191_20200101_20241231_hist.zip")), None)
        expected = "produkt_zehn_min_tu_20200101_20241231_00191.txt"
        self.assertEqual(actual, expected)

    def test_read_zip_content(self):
        zip_content = utils_file.read_zip_as_strings(FIXTURES_PATH / "10minutenwerte_TU_00191_20200101_20241231_hist.zip")
        actual = next(iter(zip_content.values()), None)[:22]
        expected = "STATIONS_ID;MESS_DATUM"
        self.assertEqual(actual, expected)
