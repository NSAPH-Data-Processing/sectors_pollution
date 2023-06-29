# dockerfile from miniconda image copy local requirements.yaml and install
FROM continuumio/miniconda3:23.3.1-0

# install gcc and python3-dev
RUN apt-get update && apt-get install -y gcc python3-dev

# install requirements
COPY requirements.yaml .

# install dependencies
RUN conda env update -n base --file requirements.yaml

# make directories
RUN mkdir /in
RUN mkdir /out
RUN mkdir /shapefiles

# set working directory
WORKDIR /app

# copy code to /app
COPY ./conf .
COPY ./aggregate.py .
COPY ./utils.py .

# ENTRYPOINT
CMD ["hydra.run.dir=/out/${now:%Y-%m-%d}/${now:%H-%M-%S}"]
ENTRYPOINT ["python3", "aggregate.py"]
