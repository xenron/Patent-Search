import configparser, datetime, pytz, time
from selenium.webdriver.common.keys import Keys
from dateutil.relativedelta import relativedelta
# from utils.orm import Region, TimeZone


class SeleniumUtil(object):

    @staticmethod
    def moveEnd(driver):
        driver.find_element_by_tag_name("body").send_keys(Keys.END)
        time.sleep(1)


class DateUtil(object):

    @staticmethod
    def get_date(date_begin, month_interval):
        date_now = datetime.datetime.now()
        date_begin = datetime.datetime.strptime(date_begin, "%Y%m%d")
        if date_begin > date_now:
            return ''
        date_end = date_begin + relativedelta(months=month_interval)

        if date_now < date_end:
            date_end = date_now
        date_end = date_end.strftime("%Y%m%d")
        return date_end

    @staticmethod
    def get_next_day(date_begin):
        date_begin = datetime.datetime.strptime(date_begin, "%Y%m%d")
        next_day = date_begin + datetime.timedelta(days=1)
        next_day_str = next_day.strftime("%Y%m%d")
        return next_day_str

class ConfigUtil(object):

    def __init__(self, config_path='config.ini'):

        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')

    def load_value(self, key_base, key_sub, default_value=''):

        result = ""
        if key_base and key_sub:
            # check key_base not exist
            if not key_base in self.config.sections():
                pass
            # check key_sub exist
            elif not key_sub in dict(self.config.items(key_base)):
                pass
            # check key_base+key_sub is empty
            elif self.config.get(key_base, key_sub):
                result = self.config.get(key_base, key_sub)
        if len(result) == 0 and default_value and len(default_value):
            result = default_value
        return result

    def load_pair(self, key_base, key_sub, default_value=''):

        result = ""
        result = self.load_value(key_base, key_sub, default_value)
        if result and len(result.split(',')) > 1:
            result = result.split(',')

        return result

    # work_time=0830:1730
    # work_time=1:0830:1730|2:0730:2230|5:1110:2359
    def load_work_time(self, key_base, key_sub, default_value=''):

        result = ""
        result = self.load_value(key_base, key_sub, default_value)
        if result:
            # work_time={1:[0830,1730], 2:[0730,2230], 5:[1110:2359]}
            if '|' in result:
                work_time_dict = {}
                for day_info in result.split('|'):
                    time_info = day_info.split(':')
                    work_time_dict[time_info[0]] = [time_info[1], time_info[2]]
                result = work_time_dict
            # work_time=0830:1730
            else:
                result = result.split(':')

        return result


class TypeUtil(object):
    @staticmethod
    def str_to_bool(str):
        return True if str.lower() == 'true' else False


class ClassUtil(object):

    @staticmethod
    def object_to_dict(objet):

        properties = {}

        for name in dir(objet):
            value = getattr(objet, name)

            if name.startswith('__') or name.startswith('_') or callable(value):
                continue

            properties[name] = value

        return properties


    @staticmethod
    def get_instance_by_dict(object, properties):

        for name, value in dir(object):
            value = getattr(object, name)

            if name.startswith('__') or name.startswith('_') or callable(value):
                continue

            properties[name] = value

        return properties


if __name__ == '__main__':
    date_str = DateUtil.get_next_day('20200127')
    print(date_str)
    # pass
