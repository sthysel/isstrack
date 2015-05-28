FROM python:3.4-onbuild
MAINTAINER sthysel <sthyse@gmail.com>

ENV REFRESHED_AT 2015-05-27

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN env --unset=DEBIAN_FRONTEND

CMD ["python", "isstrack.py"]
