import datetime
import dateutil.parser
import pytz
from storage import Storage
from importer import Importer
from wrapper import WrapperManager
from oneoff import sort_log_file

conf = {
    'bro': {
        'source_ip': 'origin_ip',
        'destionation_ip': 'dest_ip',
        'date': 'timestamp',
        'date_return': (lambda x: datetime.datetime.utcfromtimestamp(float(x)).replace(tzinfo=pytz.utc))
    },
    'pan': {
        'source_ip': 'src',
        'destionation_ip': 'dst',
        'date': 'datetime',
        'date_return': (lambda x: dateutil.parser.parse(x).replace(tzinfo=pytz.utc))
    },
    'ciscoasa': {
        'source_ip': 'src_ip',
        'destionation_ip': 'dst_ip',
        'date': '@timestamp',
        'date_return': (lambda x: dateutil.parser.parse(x).replace(tzinfo=pytz.utc))
    },
    'ciscovpn': {
        'source_ip': 'ip',
        'destionation_ip': '',
        'date': '@timestamp',
        'date_return': (lambda x: dateutil.parser.parse(x).replace(tzinfo=pytz.utc))
    },
    'suricata': {
        'source_ip': 'src_ip',
        'destionation_ip': 'dest_ip',
        'date': 'timestamp',
        'date_return': (lambda x: dateutil.parser.parse(x).replace(tzinfo=pytz.utc))
    },
    'mcafee': {
        'source_ip': 'src_ip',
        'destionation_ip': 'dest_ip',
        'date': 'detected_timestamp',
        'date_return': (lambda x: dateutil.parser.parse(x).replace(tzinfo=pytz.utc))
    }
}

data_folder = 'data/'
importer = Importer(conf, data_folder)

def parse_logs():
    # json field names and processing options for each software logs  dateutil.parser.parse('2017-04-15T00:00:03+00:00').replace(tzinfo=pytz.utc)
    importer.log_import()

def transform_analysis():
    importer.transform_analysis()

def time_map():
    importer.time_map()

def sort_file():
    wrapper_manager = WrapperManager(conf)
    sort_log_file('mcafee', 'cleaning/all.txt', wrapper_manager)

def main():
    options = {
        1: ('1 - import logs', parse_logs),
        2: ('2 - export results', transform_analysis),
        3: ('3 - time coverage', time_map)
    }
    print '\n\n'.join([option[0] for option in options.values()])
    choice = raw_input('Choose function: ')
    if int(choice) in options.keys():
        options[int(choice)][1]()


if __name__ == '__main__':
    main()
