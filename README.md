# Simple docker image with libcsp

It prides environment for easy development and testing of both client and server implementation of Cubesat Space Protocol (CSP) in [version 1](https://github.com/libcsp/libcsp/tree/libcsp-1) using Docker, Python and ZMQ. 

## Setup

```
docker-compose build
```

## Usage

Start a Bash shell in the container
```
docker-compose run --rm simple-libcsp
```

Start ZMQ queue in the background `/home/libcsp/build/zmqproxy &` or use `tmux`
```
tmux
/home/libcsp/build/zmqproxy
```
Note: press CTRL+B D to detach from session

Start CSP server in new tmux session or terminal
```
python3.7 csp_server.py
```

And send command (ping by default) by running `python3.7 csp_client.py`
