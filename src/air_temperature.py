import os
import requests
import pathlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from src import logging_conf

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