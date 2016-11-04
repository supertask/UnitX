from dateutil.parser import parse
import pytz
import re
from datetime import datetime

class UnitLib(object):
    """A class of library for converting a value by units.

    Attributes:
        __is_init_rate: a bool
        __currency_rate:
        __tz_re:
    """

    def __init__(self):
        """Inits attributes of a UnitLib class."""
        self.__is_init_rate = False
        self.__currency_rate = {}
        self.__tz_re = re.compile('(\d+):(\d+)') # For a timezone() function


    def base(self, value, unit):
        """Returns a value converted by base 2, 8, 10, or 16.

        Args:
            value: A int value in UnitXObject. (a value of base 2,8,10,16)
            unit: An instance of Unit in UnitXObject.
        Returns:
            A float which is a currency exchange rate.
        """
        return value * 2


    def timezone(self, line, unit):
        """
        """
        if not unit.numer or not unit.ex_numer:
            return line
        ex_tzline = '/'.join(unit.ex_numer.split('_'))
        tzline = '/'.join(unit.numer.split('_'))

        for m in self.__tz_re.finditer(line):
            ex_time = m.group()
            hour, minute = m.groups()
            if not hour.isdigit() or not minute.isdigit():
                return line
            date = datetime.now(pytz.timezone(ex_tzline))
            date = date.replace(hour = int(hour), minute = int(minute))
            date = date.astimezone(pytz.timezone(tzline))
            line = line.replace(ex_time, date.strftime('%H:%M'))
        
        return line


    def __download_rate(self):
        """Downloads and installs a currency exchange rate
            from a web site to database(self.__currency_rate).

        The name of website is "European Central Bank"(http://www.ecb.europa.eu/).
        There is a currency exchange rate on the website.
        """
        if self.__is_init_rate: return
        try:
            import requests
            from xml.etree import ElementTree as ET
            r = requests.get('http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml', stream=True)
            tree = ET.parse(r.raw)
            root = tree.getroot()
            namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
            for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):
                rate = float(cube.attrib['rate'])
                self.__currency_rate[cube.attrib['currency']] = rate
        except: pass
        self.__is_init_rate = True
        return


    def rate(self, line):
        """Returns a currency exchange rate from a database(self.__currency_rate).

        Args:
            line: A string of UnitXObject's value.
        Returns:
            A float which is a currency exchange rate.
        """
        self.__download_rate()
        if line in self.__currency_rate:
            return self.__currency_rate[line]
        else:
            return 1.0

