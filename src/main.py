import argparse
import pathlib


from src import logging_conf


logger = logging_conf.config("plot_temperature")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Polling data from the charger and write to database"
    )
    parser.add_argument(
        "--root-dir",
        default="/sys/devices",
        help="Dir where to search for sensor",
    )

    args = parser.parse_args()

    root_dir: pathlib.Path = pathlib.Path(args.root_dir)

    logger.info(f"hello {root_dir}")


