import os
import requests
import pathlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from typing import List, Dict
import io

from src import logging_conf
from src.dto.temperature_dto import TemperatureDto

logger = logging_conf.config("air_temperature")


def download(url: str, dst_dir: pathlib.Path):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all <a> links that start with "10minuten"
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("10minuten"):
            file_url = urljoin(url, href)
            file_path = os.path.join(dst_dir.as_posix(), href)

            logger.info(f"Downloading {file_url} ...")
            with requests.get(file_url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            logger.info(f"Saved to {file_path}")

def parse_csv_from_file(file_path: pathlib.Path):
    return parse_csv(read_file(file_path))

def read_file(file_path: pathlib.Path) -> str:
    """Read a semicolon-delimited CSV file into a list of row dicts."""
    with open(file_path, newline="", encoding="utf-8") as f:
        return f.read()


def parse_csv(input: str) -> List[Dict[str, str]]:
    """Read a semicolon-delimited CSV file into a list of row dicts."""
    reader = csv.DictReader(io.StringIO(input), delimiter=";")
    return parse_rows(list(reader))


def parse_rows(rows: List[Dict[str, str]]) -> List[TemperatureDto]:
    """Convert CSV row dicts into TemperatureDto objects."""
    dtos = []
    for row in rows:
        dto = TemperatureDto(
            stations_id=int(row["STATIONS_ID"]),
            mess_datum=int(row["MESS_DATUM"]),
            qn=int(row["  QN"].strip()),  # space in header
            pp_10=float(row["PP_10"]),
            tt_10=float(row["TT_10"]),
            rf_10=float(row["RF_10"]),
            td_10=float(row["TD_10"]),
        )
        dtos.append(dto)
    return dtos
