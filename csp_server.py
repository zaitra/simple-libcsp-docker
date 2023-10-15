#!/usr/bin/python3
# Copyright (C) 2023 Zaitra s.r.o <info@zaitra.io>
# Zaitra s.r.o - All rights reserved.
#
# This source code is protected under international copyright law.  All rights
# reserved and protected by the copyright holders.
# This file is confidential and only available to authorized individuals with the
# permission of the copyright holders.  If you encounter this file and do not have
# permission, please contact the copyright holders and delete this file.


import threading
import argparse
import time
import os
import sys
import logging

import libcsp_py3 as libcsp

ZMQ_INTERFACE = 'localhost'
VERSION = '0.0.1'
MODEL = 'payload'
HOST_NAME = 'payload_service'

def get_options():
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument(
        "-s", "--server-address", type=int, default=20, help="Server address"
    )
    return parser.parse_args(sys.argv[1:])



def init_libcsp(options):
    # init csp
    libcsp.init(options.server_address, HOST_NAME, MODEL, VERSION, 10, 300)


    libcsp.zmqhub_init(options.server_address, ZMQ_INTERFACE)
    libcsp.rtable_set(0, 0, "ZMQHUB")

    libcsp.route_start_task()
    time.sleep(3)

    print("Hostname: %s" % libcsp.get_hostname())
    print("Model:    %s" % libcsp.get_model())
    print("Revision: %s" % libcsp.get_revision())

    print("Routes:")
    libcsp.print_routes()


def csp_server():
    sock = libcsp.socket()
    libcsp.bind(sock, libcsp.CSP_ANY)
    libcsp.listen(sock, 5)
    while True:
        # wait for incoming connection
        conn = libcsp.accept(sock, libcsp.CSP_MAX_TIMEOUT)
        if not conn:
            continue

        print(
            f"connection: source={libcsp.conn_src(conn)}:{libcsp.conn_sport(conn)}, dest={libcsp.conn_dst(conn)}:{libcsp.conn_dport(conn)}"
        )

        while True:
            # Read all packets on the connection
            packet = libcsp.read(conn, 100)
            if packet is None:
                break
            # pass request on to service handler
            libcsp.service_handler(conn, packet)


if __name__ == "__main__":
    options = get_options()
    init_libcsp(options)

    # start CSP server
    threading.Thread(target=csp_server).start()