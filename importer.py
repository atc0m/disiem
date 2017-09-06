import json
import re
import os
import datetime
import time
import redis
import pytz
import itertools
import pickle
#import pandas as pd
from collections import OrderedDict
from storage import Storage

class Importer(object):
    def __init__(self, conf):
        start = datetime.datetime(2017, 4, 15, 2, 0, 1, tzinfo=pytz.utc)
        '''
        r = redis.Redis(
            host='localhost',
            port='6379'
        )
        '''
        self.storage = Storage(
            data_folder='data/',
            conf=conf,
            start=start,
            increment=120
        )

    def log_import(self):
        results = []
        for i in range(40):
            print '---- Iteration {} ----'.format(i)
            logs = self.storage.time_slice(i)
            results.append(self.find_common(logs))

        self.write_file(pickle.dumps(results))

    def write_file(self, item):
        with open('results', 'wb') as fle:
            fle.write(item)

    def transform_analysis(self):
        result_a = bytes()
        with open('results', 'rb') as fle:
            result_a = fle.read()
        results = pickle.loads(result_a)
        self.print_analysis(results)

    def print_analysis(self, some_analysis, sorting_term=None):
        if some_analysis:
            col_order = [k for k in some_analysis[0].keys()]

        # transform to dict of dict indexed by class name
        analysis = {}
        for i, stats in enumerate(some_analysis):
            analysis[i] = dict([(str(k), len(v)) for k, v in stats.items()])

        # Create a dataframe and sort if required
        df = pd.DataFrame.from_dict(analysis, orient='index')
        if sorting_term:
            df = df.sort_values(sorting_term, ascending=False)

        # return analysis in csv format as a string
        return df.to_csv('output.csv')

    def find_common(self, logs):
        combinations = []
        common_ips = {}
        for r in range(2, len(logs.keys()) + 1):
            for c in itertools.combinations(logs.keys(), r):
                combination = tuple(sorted(c))
                ip_sets = [set(logs[component].keys()) for component in combination]
                common_ips[combination] = {
                    ip: [len(logs[component][ip]) for component in combination]
                    for ip in ip_sets[0].intersection(*ip_sets[1:])
                }
        return common_ips
