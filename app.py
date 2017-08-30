import datetime
import dateutil.parser
import pytz
from storage import Storage
from importer import Importer

def parse_logs():
    # json field names and processing options for each software logs  dateutil.parser.parse('2017-04-15T00:00:03+00:00').replace(tzinfo=pytz.utc)
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
        }
    }
    importer = Importer(conf)
    importer.log_import()


def main():
    parse_logs()

if __name__ == '__main__':
    main()
