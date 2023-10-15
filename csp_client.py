#!/usr/bin/python3
# Copyright (C) 2023 Zaitra s.r.o <info@zaitra.io>
# Zaitra s.r.o - All rights reserved.
#
# This source code is protected under international copyright law.  All rights
# reserved and protected by the copyright holders.
# This file is confidential and only available to authorized individuals with the
# permission of the copyright holders.  If you encounter this file and do not have
# permission, please contact the copyright holders and delete this file.


import time
import sys
import argparse

import libcsp_py3 as libcsp

DEFAULT_TIMEOUT = 1000  # ms
ZMQ_INTERFACE = 'localhost'


def get_options():
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument(
        "-a", "--address", type=int, default=10, help="Local CSP address"
    )
    parser.add_argument(
        "-s", "--server-address", type=int, default=20, help="Server address"
    )
    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":

    options = get_options()

    libcsp.init(options.address, "csp_client", "obc", "v0.1.0", 10, 300)

    libcsp.zmqhub_init(options.address, ZMQ_INTERFACE)
    libcsp.rtable_load("0/0 ZMQHUB")

    libcsp.route_start_task()
    time.sleep(3)  # allow router task startup

    print("Connections:")
    libcsp.print_connections()

    print("Routes:")
    libcsp.print_routes()

    print(f"Sending PING to server address {options.server_address}")
    res = libcsp.ping(options.server_address)
    print(f"Received PING result {res} from server address {options.server_address}")