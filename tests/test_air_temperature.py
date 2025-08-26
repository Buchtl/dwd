import unittest
from pathlib import Path

from src import air_temperature

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_PATH: Path = PROJECT_ROOT / "tests" / "fixtures" 


class TestAirTemperature(unittest.TestCase):
    def test_parse_csv_from_file(self):
        expected = "TemperatureDto(STATIONS_ID=191, MESS_DATUM=202001010000, QN=3, PP_10=-999.0, TT_10=-4.0, RF_10=96.9, TD_10=-4.4)"
        actual = str(air_temperature.parse_csv_from_file(FIXTURES_PATH / "produkt_zehn_min_tu_20200101_20241231_00191.txt")[0])
        self.assertEqual(actual, expected)
