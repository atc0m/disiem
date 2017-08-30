import json
import re
import os
import datetime
import time
import redis
import pytz
import itertools
from storage import Storage

class Importer(object):
    def __init__(self, conf):
        start = datetime.datetime(2017, 4, 15, 2, 0, 1, tzinfo=pytz.utc)
        r = redis.Redis(
            host='localhost',
            port='6379'
        )
        self.storage = Storage(
            data_folder='data/',
            conf=conf,
            start=start,
            increment=120
        )

    def log_import(self):
        for i in range(30):
            logs = self.storage.time_slice(i)
            self.find_common(logs)

    def find_common(self, logs):
        combinations = []
        common_ips = {}
        for r in range(2, len(logs.keys()) + 1):
            for c in itertools.combinations(logs.keys(), r):
                combination = tuple(sorted(c))
                ip_sets = [set(logs[component].keys()) for component in combination]
                common_ips[combination] = {ip: [len(logs[component][ip]) for component in combination] for ip in ip_sets[0].intersection(*ip_sets[1:])}
        print common_ips
