FROM docker.buddaphest.se/marwinfaiter/pyplanet AS base

COPY settings/apps.py /pyplanet/server/settings/apps.py
COPY . /src
WORKDIR /src
RUN pip install .
