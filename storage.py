import os
import json
import time
import pickle
from datetime import datetime, timedelta
from wrapper import WrapperManager
from collections import OrderedDict

class Storage(object):

    def __init__(self, data_folder, conf, start, increment):
        self.start = start
        self.increment = increment
        self.conf = conf
        self.ignored = ['.gz', 'ESS']
        self.dict_manager = WrapperManager(conf)
        self.delta_map = {}
        self.log_structure = self.explore_files(data_folder)

    def explore_files(self, data_folder):
        structure = {}

        for root, folders, filenames in os.walk(data_folder):
            head, device = os.path.split(root)
            head, software = os.path.split(head)

            if software in self.dict_manager.wrapper_list():
                if not structure.get(software):
                    structure[software] = {}
                if not structure.get(software).get(device):
                    structure[software][device] = OrderedDict()
                ordered_files = sorted(filenames)

                for filename in ordered_files:
                    if all([not filename.endswith(end) for end in self.ignored]):
                        structure[software][device][filename] = os.path.join(root, filename)
        self.display_structure(structure)

        return structure

    def time_map(self):
        time_coverage = {}
        for software, devices in self.log_structure.items():
            time_coverage[software] = self.find_window(software, devices)
            print '\t'.join([software, str(time_coverage[software])])
        return time_coverage

    def find_window(self, software, file_dict):
        window = {
            'start': {
                'time': None,
                'compare': lambda og, current: og > current,
                'region': lambda x: x[0],
                'files': [file_paths.values()[0] for _, file_paths in file_dict.items()]
            },
            'end': {
                'time': None,
                'compare': lambda og, current: og < current,
                'region': lambda x: x[-1],
                'files': [file_paths.values()[-1] for _, file_paths in file_dict.items()]
            }
        }

        for part, time in window.items():
            for path in time['files']:
                with open(path) as fl:
                    lines = fl.readlines()
                    if lines:
                        try:
                            log = self.dict_manager.get_wrapper(software, json.loads(time['region'](lines)))
                        except:
                            import code
                            code.interact(local=locals())
                        if not time['time'] or time['compare'](time['time'], log.get_time()):
                            window[part]['time'] = log.get_time()
        return {
            key: value['time']
            for key, value
            in window.items()
        }


    def load_time_slice(self, delta, increment_lambda, state_step):
        data = {}
        if not self.delta_map:
            self.delta_map[delta] = {}
            for software, devices in self.log_structure.items():
                self.delta_map[delta][software] = {}
                for device, files in devices.items():
                    for filename, path in files.items():
                        self.delta_map[delta][software][device] = (filename, path, 0)
                        break
            # second slice does not start where the first one ends
            self.delta_map[delta + 1] = self.delta_map[delta].copy()
        if self.delta_map.get(delta):
            for software, devices in self.delta_map[delta].items():
                print software
                data[software] = self.load_file_time_slice(
                    devices=devices,
                    key=software,
                    delta=delta,
                    start_func=self.start + timedelta(seconds=delta*(increment_lambda(self.increment))),
                    state_step=state_step
                )
                print len(data[software])
        return data

    def load_file_time_slice(self, key, devices, delta, start_func, state_step):
        start = start_func
        end = start + timedelta(seconds=self.increment)
        logs = {}
        for device, state in devices.items():
            print device
            found = False
            files_end = True
            line_number = 0
            for name, path in self.log_structure[key][device].items():
                if state[0] == name:
                    found = True
                if found:
                    print '---- current state {} ----'.format(state)
                    with open(path) as fn:
                        for i, line in enumerate(fn):
                            if i >= state[2]:
                                log = self.dict_manager.get_wrapper(key, json.loads(line))
                                line_number = i
                                if log.get_time() < start:
                                    continue
                                if log.get_time() > end:
                                    files_end = False
                                    break
                                if logs.get(log.get_src()):
                                    logs[log.get_src()].append(log)
                                else:
                                    logs[log.get_src()] = [log]
                    if not files_end:
                        next_state = (name, path, line_number)
                        self.save_state(delta, key, device, next_state, state_step)
                        break
            if files_end:
                next_state = (name, path, line_number)
                self.save_state(delta, key, device, next_state, state_step)

        return logs

    def load_file(self, path):
        print 'Opening: ' + path
        start = time.time()
        with open(path, 'rb') as fle:
            data = pickle.load(fle)
        print 'Took ' + str(time.time() - start) + ' seconds'
        return data

    def save_state(self, delta, key, device, state, state_step):
        if not self.delta_map.get(delta + state_step):
            self.delta_map[delta + state_step] = {}
        if not self.delta_map.get(delta + state_step).get(key):
            self.delta_map[delta + state_step][key] = {}
        print '---- saved state {} ----'.format(state)
        self.delta_map[delta + state_step][key][device] = state

    def display_structure(self, structure):
        print '----\tFile Structure\t----'
        print '\nSoftware\tDevice\tFile\n'
        for software, devices in structure.items():
            print software
            for device, files in devices.items():
                print '\t' + device
                for fn in files.keys():
                    print '\t\t' + fn
