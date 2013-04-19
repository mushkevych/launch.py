"""
Created on 2011-02-15

Module contains small functions that are used to format, transform or classify the date-time structures 

@author: Bohdan Mushkevych
"""
import calendar

from datetime import datetime, timedelta
from system.process_context import ProcessContext

SYNERGY_DATE_PATTERN = '%Y%m%d%H'
SYNERGY_SESSION_PATTERN = '%Y%m%d%H%M%S'

def define_pattern(timestamp):
    hasYear = False
    hasMonth = False
    hasDay = False
    hasHour = False

    for index in range(0, len(timestamp)):
        if index >= 0 and index < 4 and timestamp[index] != '0':
            hasYear = True
        elif index >= 4 and index < 6 and timestamp[index] != '0':
            hasMonth = True
        elif index >= 6 and index < 8 and timestamp[index] != '0':
            hasDay = True
        elif index >= 8 and timestamp[index] != '0':
            hasHour = True

    pattern = ''
    if hasYear:
        pattern += '%Y'
    else:
        pattern += '0000'
    if hasMonth:
        pattern += '%m'
    else:
        pattern += '00'
    if hasDay:
        pattern += '%d'
    else:
        pattern += '00'
    if hasHour:
        pattern += '%H'
    else:
        pattern += '00'

    return pattern

def raw_to_session(timestamp):
    """@param timestamp: as float from time.time() output
    @return string in YYYYMMDD_HHMMSS format"""
    t = datetime.utcfromtimestamp(timestamp)
    return t.strftime(SYNERGY_SESSION_PATTERN)

def session_to_hour(timestamp):
    """@param timestamp: as string in YYYYMMDD_HHMMSS format
    @return string in YYYYMMDDHH format"""
    t = datetime.strptime(timestamp, SYNERGY_SESSION_PATTERN)
    return t.strftime(SYNERGY_DATE_PATTERN)

def hour_to_day(timestamp):
    """@param timestamp: as string in YYYYMMDDHH format
    @return string in YYYYMMDD00 format"""
    t = datetime.strptime(timestamp, SYNERGY_DATE_PATTERN)
    return t.strftime('%Y%m%d00')

def day_to_month(timestamp):
    """@param timestamp: as string in YYYYMMDD00 format
    @return string in YYYYMM0000 format"""
    t = datetime.strptime(timestamp, '%Y%m%d00')
    return t.strftime('%Y%m0000')

def month_to_year(timestamp):
    """@param timestamp: as string in YYYYMM0000 format
    @return string in YYYY000000 format"""
    t = datetime.strptime(timestamp, '%Y%m0000')
    return t.strftime('%Y000000')

def actual_timeperiod(time_qualifier):
    """ method receives time qualification (hourly/daily/monthly/yearly)
    @return: string representing current datetime (utc now) in proper Synergy Date format """
    return datetime_to_synergy(time_qualifier, datetime.utcnow())
        
def increment_timeperiod(time_qualifier, timestamp):
    """ method is used by Scheduler to define <<next>> time period.
    For hourly, it is next hour: 20100101_19 -> 20100101_20 
    For month - next month: 201001 -> 201002, etc"""
    
    pattern = define_pattern(timestamp)
    t = datetime.strptime(timestamp, pattern)

    if time_qualifier == ProcessContext.QUALIFIER_HOURLY:
        t = t + timedelta(hours=1)
        return t.strftime('%Y%m%d%H')
    
    elif time_qualifier == ProcessContext.QUALIFIER_DAILY:
        t = t + timedelta(days=1)
        return t.strftime('%Y%m%d00')
    
    elif time_qualifier == ProcessContext.QUALIFIER_MONTHLY:
        if t.month + 1 > 12:
            new_month = 1
            new_year = t.year + 1
            t = t.replace(year = new_year, month = new_month)
        else:
            t = t.replace(month = t.month + 1)
        return t.strftime('%Y%m0000')
    
    elif time_qualifier == ProcessContext.QUALIFIER_YEARLY:
        t = t.replace(year = t.year + 1)
        return t.strftime('%Y000000')
    else:
        raise ValueError('unknown time qualifier %s' % time_qualifier)

def cast_to_time_qualifier(time_qualifier, timestamp):
    """ method is used to cast synergy_time accordingly to process time qualifier.
    For example: for QUALIFIER_HOURLY, it can be either 20100101_19 or 20100101_193412 """
    
    date_format = None
    if time_qualifier == ProcessContext.QUALIFIER_HOURLY:
        if len(timestamp) > 10:
            t = datetime.strptime(timestamp, SYNERGY_SESSION_PATTERN)
            return t.strftime(SYNERGY_DATE_PATTERN)
        else:
            return timestamp

    elif time_qualifier == ProcessContext.QUALIFIER_DAILY :
        date_format = '%Y%m%d00'
    elif time_qualifier == ProcessContext.QUALIFIER_MONTHLY:
        date_format = '%Y%m0000'
    elif time_qualifier == ProcessContext.QUALIFIER_YEARLY:
        date_format = '%Y000000'

    pattern = define_pattern(timestamp)
    t = datetime.strptime(timestamp, pattern)

    if date_format is not None:
        return t.strftime(date_format)
    else:
        raise ValueError('unknown time qualifier: %s ' % time_qualifier)

def datetime_to_synergy(time_qualifier, dt):
    """ method parses datetime and returns Synergy Date"""
    if time_qualifier == ProcessContext.QUALIFIER_HOURLY:
        date_format = SYNERGY_DATE_PATTERN
    elif time_qualifier == ProcessContext.QUALIFIER_DAILY:
        date_format = '%Y%m%d00'
    elif time_qualifier == ProcessContext.QUALIFIER_MONTHLY:
        date_format = '%Y%m0000'
    elif time_qualifier == ProcessContext.QUALIFIER_YEARLY:
        date_format = '%Y000000'
    elif time_qualifier == ProcessContext.QUALIFIER_REAL_TIME:
        date_format = SYNERGY_SESSION_PATTERN
    else:
        raise ValueError('unknown time qualifier: %s' % time_qualifier)
    return dt.strftime(date_format)

def synergy_to_datetime(time_qualifier, timestamp):
    """ method receives timestamp in Synergy format YYYYMMDD_HH and convert it to _naive_ datetime"""
    if time_qualifier == ProcessContext.QUALIFIER_HOURLY:
        date_format = SYNERGY_DATE_PATTERN
    elif time_qualifier == ProcessContext.QUALIFIER_DAILY:
        date_format = '%Y%m%d00'
    elif time_qualifier == ProcessContext.QUALIFIER_MONTHLY:
        date_format = '%Y%m0000'
    elif time_qualifier == ProcessContext.QUALIFIER_YEARLY:
        date_format = '%Y000000'
    elif time_qualifier == ProcessContext.QUALIFIER_REAL_TIME:
        date_format = SYNERGY_SESSION_PATTERN
    else:
        raise ValueError('unknown time qualifier: %s ' % time_qualifier)
    return datetime.strptime(timestamp, date_format).replace(tzinfo=None)

def session_to_epoch(timestamp):
    """ converts Synergy Timestamp for session to UTC zone seconds since epoch """
    utc_timetuple = datetime.strptime(timestamp, SYNERGY_SESSION_PATTERN).replace(tzinfo=None).utctimetuple()
    return calendar.timegm(utc_timetuple)


if __name__ == '__main__':
    pass