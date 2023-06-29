import os
import zipfile
from urllib import request
import logging


logger = logging.getLogger(__name__)


def download_and_unzip(url: str, filename: str, dir: str = "."):
    # make sure output directory exists
    os.makedirs(dir, exist_ok=True)

    # if targer folder exists, and not overwrite, return and exit
    if os.path.exists(f"{dir}/{filename}"):
        logger.info(f"Shapefiles already downloaded. Exiting.")
        return

    # download, if can't download, or folder, log error and exit
    tgt = f"{dir}/{filename}"
    request.urlretrieve(url, f"{tgt}.zip")
    logger.info(f"Downloaded {url}")

    # unzip with unzip library
    with zipfile.ZipFile(f"{tgt}.zip", "r") as zip_ref:
        zip_ref.extractall(tgt)
    logger.info(f"Unzipped {tgt}")

    # remove dirty zip file
    os.remove(f"{tgt}.zip")
    logger.info(f"Removed {tgt}")

    # rename shapefiles to standardize name by
    # changing all files names in tgt/
    logging.info(f"Rename file from shapefile to shapefile.*")
    files = os.listdir(tgt)
    for f in files:
        base, ext = os.path.splitext(f)
        os.rename(f"{tgt}/{f}", f"{tgt}/shapefile{ext}")
