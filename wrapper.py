import datetime
import dateutil.parser
import pytz


class WrapperManager(object):

    def __init__(self, conf):
        self.conf = conf

    def get_wrapper(self, software, dictionary):
        fields = self.conf[software]
        wrapper = Wrapper(
            dictionary=dictionary,
            source_ip=fields['source_ip'],
            destionation_ip=fields['destionation_ip'],
            date=fields['date'],
            date_return=fields['date_return']
        )
        return wrapper

    def wrapper_list(self):
        return self.conf.keys()


class Wrapper(dict):

    def __init__(self, dictionary, source_ip, destionation_ip, date, date_return):
        dict.__init__(self, dictionary)
        self.source_ip = source_ip
        self.destionation_ip = destionation_ip
        self.date = date
        self.date_return = date_return

    def get_src(self):
        return self.get(self.source_ip)

    def get_dest(self):
        return self.get(self.destionation_ip)

    def get_time(self):
        return self.date_return(self[self.date])
