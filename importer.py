import json
import re
import os
import datetime
import time
import redis
import pytz
import itertools
import pickle
# import pandas as pd
from collections import OrderedDict
from storage import Storage
from random import randint

class Importer(object):
    def __init__(self, conf, data_folder):
        start = datetime.datetime(2017, 4, 15, 3, 30, 0, tzinfo=pytz.utc)
        '''
        r = redis.Redis(
            host='localhost',
            port='6379'
        )
        '''
        self.storage = Storage(
            data_folder=data_folder,
            conf=conf,
            start=start,
            increment=120
        )

    def time_map(self):
        time_map = self.storage.time_map()
        self.write_file(pickle.dumps(time_map), 'time_map')

    def log_import(self):
        results = []
        for i in range(391, 1441):
            print '---- Iteration {} ----'.format(i)
            logs = self.storage.time_slice(i)
            results.append(self.find_common(logs))
            if i % 30 == 0:
                self.write_file(self.storage.delta_map, 'delta_map' + str(i))
                self.write_file(results, 'bak' + str(i))
                results = []

    def write_file(self, item, title):
        print 'Writing file: ' + title
        start = time.time()
        with open('storage/' + title, 'wb') as fle:
            pickle.dump(item, fle)
        print 'Took ' + str(time.time() - start) + ' seconds'

    def transform_analysis(self, data_folder, file_stub):
        sorted_filenames = sorted(
            [filename for filename in os.listdir(data_folder) if filename.startswith(file_stub)],
            key=lambda x: int(x[len(file_stub):])
        )
        for filename in sorted_filenames:
            results = []
            print 'Opening: ' + filename
            start = time.time()
            with open(os.path.join(data_folder, filename), 'rb') as fle:
                results = pickle.load(fle)
            print 'Took ' + str(time.time() - start) + ' seconds'
            self.summarise_traffic_analysis(results, filename)
            # self.print_analysis(results)

    def summarise_traffic_analysis(self, results, filename):
        summary = {}
        for i, time_slice in enumerate(results):
            if i % 2 == 0:
                for combinations, addresses in time_slice.items():
                    stats = {
                        'unique': len(addresses.keys()),
                        'traffic': max(
                            [0] if not addresses.values() else
                            [len(requests) for requests in addresses.values()]
                        )
                    }
                    if combinations not in summary:
                        summary[combinations] = stats
                    else:
                        for key, stat in stats.items():
                            summary[combinations][key] += stat
        self.write_file(summary, 'summary_' + filename)

    def print_analysis(self, some_analysis, sorting_term=None):
        if some_analysis:
            col_order = sorted(some_analysis[0].keys(), key=lambda l: len(l))
        # transform to dict of dict indexed by class name
        analysis = {}
        for i, stats in enumerate(some_analysis):
            analysis[i] = OrderedDict([(str(k), stats[k]) for k in col_order])

        # Create a dataframe and sort if required
        df = pd.DataFrame.from_dict(analysis, orient='index')
        if sorting_term:
            df = df.sort_values(sorting_term, ascending=False)

        # return analysis in csv format as a string
        return df.to_csv('reports/output.csv')

    def print_analysis_simulation(self, some_analysis, sorting_term=None):
        if some_analysis:
            col_order = sorted(some_analysis[0].keys(), key=lambda l: len(l))

        # transform to dict of dict indexed by class name
        analysis = []
        for i, stats in enumerate(some_analysis):
            if i >= 14 or i <= 29:
                analysis.append(OrderedDict([(str(k), 30 * len(stats[k]) + randint(0,30) if len(stats[k]) > 0 else 0) for k in col_order]))

        # Create a dataframe and sort if required
        df = pd.DataFrame.from_dict(dict(zip(range(0,15), analysis)), orient='index')
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
                    ip: {component: [wrapper.get_dict() for wrapper in logs[component][ip]]  for component in combination}
                    for ip in ip_sets[0].intersection(*ip_sets[1:])
                }
        return common_ips
