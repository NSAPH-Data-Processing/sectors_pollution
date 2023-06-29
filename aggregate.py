import os

import logging
from omegaconf import DictConfig
import hydra

import numpy as np
import geopandas as gpd
import xarray
import rasterio
import rasterstats

import utils

def run_task(task: DictConfig, cfg: DictConfig):
    # aliases
    shp = cfg.shapefiles

    # == get output filename ==
    f = os.path.splitext(task.file)[0] + ".csv"
    if os.path.exists(f"{cfg.output.dir}/{f}"):
        logging.info(f"Output file {f} already exists, skipping")
        return

    #  == get shapefile if necessary ==
    if task.shapefile not in shp.files:
        logging.info("config shapefile is not in dict, assuming its a filename")
        shp_path = f"{shp.dir}/{task.shapefile}"
    else:
        # check if task_shp is url and zipped shapefile ------
        shp_val = shp.files[task.shapefile]
        if shp_val.startswith("http") and shp_val.endswith(".zip"):
            logging.info("config shapefile is a url.")
            shp_path = f"{shp.dir}/{task.shapefile}"
            # already downloaded?
            if not os.path.exists(f"{shp.dir}/{task.shapefile}"):
                logging.info(f"Downloading from {shp_val}")
                utils.download_and_unzip(shp_val, task.shapefile, shp.dir)
            shp_val = f"{task.shapefile}/shapefile.shp"
        else:
            raise ValueError("invalid shapefile value")
        shp_path = f"{shp.dir}/{shp_val}"

    # == read netcdf ===
    logging.info(f"Reading netcdf {cfg.job.dir}/{task.file}")
    ds = xarray.open_dataset(f"{cfg.job.dir}/{task.file}")
    layer = getattr(ds, task.layer)

    # == compute zonal stats of layer

    # obtain affine transform/boundaries
    dims = layer.dims
    assert len(dims) == 2, "netcdf coordinates must be 2d"
    lon = layer[cfg.job.lon].values
    lat = layer[cfg.job.lat].values
    transform = rasterio.transform.from_origin(
        lon[0], lat[-1], lon[1] - lon[0], lat[1] - lat[0]
    )

    # compute zonal stats
    logging.info(f"Computing zonal stats")
    stats = rasterstats.zonal_stats(
        shp_path,
        layer.values[::-1],
        stats=cfg.job.stats,
        affine=transform,
        all_touched=cfg.all_touched,
        geojson_out=True,
        nodata=np.nan if cfg.job.nodata == "nan" else cfg.job.nodata,
    )
    gdf = gpd.GeoDataFrame.from_features(stats)

    # == save stats to file ==
    # save shapefile
    if cfg.output.save_shp:
        logging.info(f"Saving stats to {cfg.output.dir}/{f}")
        f = os.path.splitext(task.file)[0] + ".shp"
        gdf.to_file(f"{cfg.output.dir}/{f}")

    # save csv
    logging.info(f"Saving stats to {cfg.output.dir}/{f}")
    if not cfg.output.save_feats:
        gdf = gdf[cfg.job.stats]
    gdf.drop(columns=["geometry"]).to_csv(f"{cfg.output.dir}/{f}", index=False)
    logging.info(f"Task complete")

@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg: DictConfig):
    tasks = cfg.job.tasks
    logging.info(f"Running {len(tasks)} task(s)")
    for i, task in enumerate(tasks):  # TODO: could support some parallelization here for large jobs
        logging.info(f"Running task {i + 1}/{len(tasks)}: {task}")
        try:
            run_task(task, cfg)
        except Exception as e:
            logging.error(f"Error running task {task}")
            logging.error(e)

    logging.info(f"Done")

if __name__ == "__main__":
    main()
