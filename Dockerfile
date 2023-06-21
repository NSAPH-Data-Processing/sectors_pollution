# dockerfile from miniconda image copy local requirements.yaml and install
FROM continuumio/miniconda3:23.3.1-0

# install gcc and python3-dev
RUN apt-get update && apt-get install -y gcc python3-dev

# install requirements
COPY requirements.yaml .

# install dependencies
RUN conda env update -n base --file requirements.yaml

# set working directory
WORKDIR /app

# copy all code to /app
COPY . .

# make out directory
RUN mkdir /out

# workdir /out/
WORKDIR /out

# ENTRYPOINT
ENTRYPOINT ["python3", "/app/aggregate.py", "hydra.run.dir=/out/outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}", "hydra.searchpath=[file:///out/conf,file://out]"]
