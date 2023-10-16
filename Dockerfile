FROM jupyter/base-notebook:latest

RUN mamba install -c conda-forge geopandas localtileserver -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir ./pages
COPY /pages ./pages

ENV PROJ_LIB='/opt/conda/share/proj'

USER root
RUN chown -R ${NB_UID} ${HOME}
RUN apt-get update && apt-get install -y git
RUN pip install -U git+https://github.com/giswqs/ipyleaflet.git@pmtiles
RUN pip install -U git+https://github.com/opengeos/leafmap.git
USER ${NB_USER}

EXPOSE 8765

CMD ["solara", "run", "./pages", "--host=0.0.0.0"]
