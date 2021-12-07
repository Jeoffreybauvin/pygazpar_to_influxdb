
#FROM instrumentisto/geckodriver:latest
FROM python:3.9.9-slim

RUN  apt update \
    && apt install python3 python3-pip python3-setuptools -y \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* /tmp/*


WORKDIR /data

COPY . /data

RUN pip3 install -r requirements.txt

#RUN ln -s /opt/firefox/firefox /usr/bin/firefox

#ENTRYPOINT [ "python3" ]
#CMD ["python3", "./pygazpar_to_influxdb.py", "--schedule", "06:00"]
CMD ["python3", "./pygazpar_to_influxdb.py", "-vvv"]