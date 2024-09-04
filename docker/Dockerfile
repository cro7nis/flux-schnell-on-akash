FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime as build

LABEL maintainer="cro7 <cro7nis@gmail.com>"

ENV USER=cro7
ENV APP=text-2-image
ENV PORT=8051

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && useradd -m $USER

FROM build as runtime

RUN mkdir -p /opt/$APP \
  && chown $USER:$USER /opt/$APP

WORKDIR /opt/$APP
RUN pip install poetry
COPY --chown=$USER:$USER pyproject.toml pyproject.toml
#COPY --chown=$USER:$USER poetry.lock  poetry.lock
RUN  poetry config virtualenvs.create false \
    && poetry install --with=dev --no-root --no-interaction \
    && rm -rf /root/.cache/pypoetry

USER $USER

# Copy nesessary files to docker
COPY --chown=$USER:$USER src/app.py app.py
COPY --chown=$USER:$USER configs configs
# COPY --chown=$USER:$USER checkpoints checkpoints
COPY --chown=$USER:$USER docker/start.sh start.sh


ENTRYPOINT bash start.sh