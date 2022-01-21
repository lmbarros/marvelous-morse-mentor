FROM balenalib/raspberry-pi-python:3-buster-build-20210705

WORKDIR /src

RUN apt-get update && apt-get install apt-transport-https ca-certificates
RUN echo "deb https://seeed-studio.github.io/pi_repo/ stretch main" | tee /etc/apt/sources.list.d/seeed.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BB8F40F3
RUN apt-get update && apt-get install python3-mraa python3-upm python3-rpi.gpio
RUN pip3 install rpi_ws281x
RUN git clone https://github.com/Seeed-Studio/grove.py && cd grove.py && pip3 install .

COPY src /src

CMD ["python", "-u", "main.py"]
