from dateutil.parser import parse
import pytz
import re
from datetime import datetime

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

