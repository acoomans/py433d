#!/usr/bin/env python3

import logging
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from queue import Queue
from signal import (
    signal,
    SIGINT
)
from threading import Thread

from py433 import (
    tcp_server,
    transmitter,
    configuration,
    __version__,
    defaults
)

parser = ArgumentParser(description='Server for 433Mhz communication')
parser.add_argument('-v', '--version', help="Show version")
parser.add_argument('-c', '--conf', default=defaults.config, help="Configuration file")
parser.add_argument('-p', '--port', help="Set port to listen on")
parser.add_argument('-l', '--log', help="Log file")
args = parser.parse_args()

if args.version:
    print(__version__)
    exit(0)

def reload():
    tx.stop()
    srv.stop()
    conf.stop()

def exithandler(self, signal):
    tx.stop()
    srv.stop()
    conf.stop()
    logging.info("Server stopped")

signal(SIGINT, exithandler)

while True:
    conf = configuration.load(filename=args.conf)
    conf.watch(reload)

    rootLogger = logging.getLogger()
    rootLogger.setLevel(conf.log_level)

    logFormatter = logging.Formatter("%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s")

    rootLogger.handlers = []

    # rootLogger.handlers[0].setFormatter(logFormatter)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    fileHandler = logging.handlers.RotatingFileHandler(args.log or conf.log_filename, maxBytes=(1024 * 1024), backupCount=7)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    logging.info("Server started")

    q = Queue()

    tx = transmitter(q, messages=conf.messages, pin=conf.tx_pin, protocol=conf.tx_protocol, pulse=conf.tx_pulse)
    t1 = Thread(target=tx.run)
    t1.daemon = True
    t1.start()

    srv = tcp_server(port=args.port or conf.port, handler=lambda m: q.put(m))
    t2 = Thread(target=srv.run)
    t2.daemon = True
    t2.start()

    t1.join()
    t2.join()
