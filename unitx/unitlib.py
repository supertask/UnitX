from dateutil.parser import parse
import pytz
import re
from datetime import datetime
import requests
from xml.etree import ElementTree as ET


# For Bill
money_rate = {}
try:
	r = requests.get('http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml', stream=True)
	tree = ET.parse(r.raw)
	root = tree.getroot()
	namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
	for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):
		rate = float(cube.attrib['rate'])
		money_rate[cube.attrib['currency']] = rate
except: pass

# For timezone function
tz_re = re.compile('(\d+):(\d+)')


def base(value, unit):
	return value * 2

def timezone(line, unit):
	if not unit.numer or not unit.ex_numer:
		return line
	ex_tzline = '/'.join(unit.ex_numer.split('_'))
	tzline = '/'.join(unit.numer.split('_'))

	for m in tz_re.finditer(line):
		ex_time = m.group()
		hour, minute = m.groups()
		if not hour.isdigit() or not minute.isdigit():
			return line
		date = datetime.now(pytz.timezone(ex_tzline))
		date = date.replace(hour = int(hour), minute = int(minute))
		date = date.astimezone(pytz.timezone(tzline))
		line = line.replace(ex_time, date.strftime('%H:%M'))
	
	return line


def rate(line):
	if line in money_rate:
		return money_rate[line]
	else:
		return 1

