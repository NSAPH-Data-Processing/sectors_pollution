# sectors_pollution
Spatial aggregation from 1-kilometer grid to zcta of sectors pollution

## Run

The easiest way is to use the docker image. For this, you will need to add a local job file at the path `conf/job/<job_name>.yaml` (see below for the contents). Then run

```bash
docker run -v $(pwd)/data/input/<symlink_lab>:/in -v $(pwd)/data/output/<symlink_lab>:/out -v $(pwd)/data/shapefiles/<symlink_lab>:/shapefiles <nsaph_accout>/sectors_pollution
```

* shapefiles are downloaded into a filesystem (TODO: they could only reside in the container?)
* `$(pwd)/in` volume to input
* `$(pwd)/out` volume to output

**Note**: On a Windows machine with powershell, replace `$(pwd)` with `${pwd}`.

It is also possible to clone the repository and use it via the conda environment. 

```bash
git clone <https://github.com/<user>/repo>
cd <repo>
conda env create -f requirements.yaml
conda activate sectors_pollution_env
python aggregate.py job=test_job job.dir="./data/input/US_Sectors_2013" shapefiles.dir="./data/shapefiles" output.dir="./data/output/zcta_sectors_pollution"
python aggregate.py job=zcta_sectors_pollution job.dir="./data/input/US_Sectors_2013" shapefiles.dir="./data/shapefiles" output.dir="./data/output/zcta_sectors_pollution"
```

An example output will look like this

```
File: outputs/2023-06-17/04-45-10/2013.Sectors.US.PM25_Total.1km.csv
```

```
ZCTA5CE10,AFFGEOID10,GEOID10,ALAND10,AWATER10,min,max,mean,count
36522,8600000US36522,36522,570006940,3241962,8.108333587646484,9.22499942779541,8.543976070374017,635
35586,8600000US35586,35586,472580465,892816,8.550000190734863,10.15000057220459,9.187298794450431,580
85634,8600000US85634,85634,7443310770,98313,4.866666793823242,11.049999237060547,7.613444465236194,7515
71854,8600000US71854,71854,721235775,14713194,7.7166666984558105,8.916666030883789,8.255185475938257,826
19963,8600000US19963,19963,276242161,21115750,,,,0
[...]
```


