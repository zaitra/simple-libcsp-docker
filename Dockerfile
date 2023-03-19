FROM --platform=amd64 ubuntu:18.04

ENV LD_LIBRARY_PATH="/home/libcsp/build:${PATH}"
ENV PYTHONPATH="/home/libcsp/build:${PATH}"

RUN apt-get update -y && apt-get install -y python3.7 python3.7-dev python3.7-venv python3-pip vim git gcc g++ pkg-config libsocketcan-dev libzmq3-dev can-utils curl tmux
RUN cd /home && git clone https://github.com/libcsp/libcsp.git && cd libcsp && git checkout libcsp-1

RUN mkdir -p /home/simple-client-server
COPY . /home/simple-client-server
WORKDIR /home/simple-client-server

RUN cp /home/simple-client-server/*.patch /home/libcsp
RUN cd /home/libcsp && patch examples/buildall.py buildall.patch && patch waf waf.patch && patch wscript wscript.patch

RUN cd /home/libcsp && python3.7 examples/buildall.py