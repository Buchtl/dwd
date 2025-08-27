import argparse
import pathlib
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import PendingRollbackError

from src import logging_conf
from src import air_temperature
from src import utils_file

from src.temperature_db_session import TemperatureDbSession
from src.dto.temperature_dto import TemperatureDto

logger = logging_conf.config("plot_temperature")

base_url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/historical/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Polling data from the charger and write to database"
    )
    parser.add_argument(
        "--dst-dir",
        default=os.environ.get("DIR_DST") or "./data",
        help="Dir where to search for sensor",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download files",
    )
    parser.add_argument(
        "--src-dir",
        default=os.environ.get("DIR_SRC") or "./tests/fixtures/produkt_zehn_min_tu_20200101_20241231_00191.txt",
        help="Dir where to search for sensor",
    )
    parser.add_argument(
        "--db-url",
        default=os.environ.get("DB_URL") or "localhost",
        help="db url",
    )
    parser.add_argument(
        "--db-port",
        default=os.environ.get("DB_PORT") or "5432",
        help="db url",
    )
    parser.add_argument(
        "--db-name",
        default=os.environ.get("DB_NAME") or "dwd",
        help="db name",
    )
    parser.add_argument(
        "--db-user",
        default=os.environ.get("DB_USER") or "dwd",
        help="db username",
    )
    parser.add_argument(
        "--db-pass",
        default=os.environ.get("DB_PASS") or "dwd",
        help="db password",
    )

    args = parser.parse_args()

    dst_dir: pathlib.Path = pathlib.Path(args.dst_dir)
    src_dir: pathlib.Path = pathlib.Path(args.src_dir)

    if args.download:
        logger.info(f"Downloading files to {dst_dir}")
        os.makedirs(dst_dir.as_posix(), exist_ok=True)
        air_temperature.download(url=base_url, dst_dir=dst_dir)
    else:
        logger.info(f"Parsing files from {src_dir}")
        db_session = TemperatureDbSession(db_url=args.db_url, db_port=args.db_port, db_name=args.db_name,
                                          db_user=args.db_user, db_pass=args.db_pass)
        with db_session as db:
            for file_path in src_dir.iterdir():
                if file_path.is_file():
                    logger.debug(file_path.name)
                    files_str = utils_file.read_zip_as_strings(file_path)
                    for file_str in files_str.values():
                        csv: list[TemperatureDto] = air_temperature.parse_csv(file_str)
                        for row in csv:
                            logger.debug(row.mess_datum)
                            try:
                                db.write(row.to_entity())
                            except (IntegrityError, PendingRollbackError):
                                logger.info(f"Skipping duplicate row {row.mess_datum}")
