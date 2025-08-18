import argparse
import pathlib
import os

from src import logging_conf
from src import air_temperature


logger = logging_conf.config("plot_temperature")

base_url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/historical/"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Polling data from the charger and write to database"
    )
    parser.add_argument(
        "--dst-dir",
        default="./data",
        help="Dir where to search for sensor",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download files",
    )
    parser.add_argument(
        "--src-dir",
        default="./tests/fixtures/produkt_zehn_min_tu_20200101_20241231_00191.txt",
        help="Dir where to search for sensor",
    )

    args = parser.parse_args()

    dst_dir: pathlib.Path = pathlib.Path(args.dst_dir)
    src_dir: pathlib.Path = pathlib.Path(args.src_dir)

    if(args.download):
      logger.info(f"Downloading files to {dst_dir}")
      os.makedirs(dst_dir.as_posix(), exist_ok=True)
      air_temperature.download(url=base_url, dst_dir=dst_dir)
    else:
       records = air_temperature.parse_csv_from_file(src_dir)
       for r in records:
          print(r)
