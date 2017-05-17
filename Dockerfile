FROM python:alpine

WORKDIR /build

ADD setup.* /build/
ADD rgc /build/rgc

RUN \
python setup.py install
