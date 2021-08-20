FROM balenalib/raspberry-pi-python:3-buster-build-20210705

WORKDIR /src

RUN git clone https://github.com/Seeed-Studio/grove.py && cd grove.py && sudo pip3 install .
RUN pip3 install RPi.GPIO

COPY src /src

CMD ["python", "-u", "main.py"]
