import json
import logging
import os

import importlib
watchdog = importlib.find_loader('watchdog')
if watchdog:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

from . import defaults


class configuration:

    @classmethod
    def load(cls, filename=defaults.config):
        conf = dict()
        try:
            with open(filename) as f:
                conf = json.load(f)
            loaded = True
        except Exception as e:
            print(e)
        logging.debug("loaded config from file '" + filename + "':" + str(conf))

        new_instance = cls()
        new_instance.filename = filename
        new_instance.tx_pin = conf.get("radio").get("tx_pin", 17)
        new_instance.tx_protocol = conf.get("radio").get("tx_protocol", 1)
        new_instance.tx_pulse = conf.get("radio").get("tx_pulse", 180)
        new_instance.port = conf.get("server").get("port", defaults.port)
        new_instance.log_filename = conf.get("log").get("filename", "433d.log")
        new_instance.messages = conf.get("messages")

        return new_instance

    def watch(self, callback=None):
        if watchdog:

            filename = self.filename
            class Handler(FileSystemEventHandler):
                @staticmethod
                def on_any_event(event):
                    if event.src_path == filename:
                        callback()

            self.observer = Observer()
            self.observer.schedule(Handler(), os.path.dirname(os.path.realpath(self.filename)))
            self.observer.start()

    def stop(self):
        if watchdog:
            self.observer.stop()