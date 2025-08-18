import argparse
import pathlib
import os


from src import logging_conf


logger = logging_conf.config("plot_temperature")

base_url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Polling data from the charger and write to database"
    )
    parser.add_argument(
        "--dst-dir",
        default="./data",
        help="Dir where to search for sensor",
    )

    args = parser.parse_args()

    dst_dir: pathlib.Path = pathlib.Path(args.dst_dir)

    logger.info(f"hello {dst_dir}")

    os.makedirs(dst_dir.as_posix(), exist_ok=True)


