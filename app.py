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

def parse_logs():
    # json field names and processing options for each software logs  dateutil.parser.parse('2017-04-15T00:00:03+00:00').replace(tzinfo=pytz.utc)
    importer = Importer(conf, data_folder)
    #importer.log_import()
    #importer.transform_analysis()
    importer.time_map()

def sort_file():
    wrapper_manager = WrapperManager(conf)
    sort_log_file('mcafee', 'cleaning/all.txt', wrapper_manager)

def main():
    parse_logs()


if __name__ == '__main__':
    main()
