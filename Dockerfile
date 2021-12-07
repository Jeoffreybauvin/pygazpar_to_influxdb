
FROM python:3.9.9-slim

RUN  apt update \
    && apt install python3 python3-pip python3-setuptools apt-utils -y \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* /tmp/*

WORKDIR /data

COPY . /data

RUN pip3 install -r requirements.txt

CMD ["python3", "./pygazpar_to_influxdb.py", "-vvv"]