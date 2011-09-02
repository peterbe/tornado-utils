import datetime

# Language constants
MINUTE = 'minute'
MINUTES = 'minutes'
HOUR = 'hour'
HOURS = 'hours'
YEAR = 'year'
YEARS = 'years'
MONTH = 'month'
MONTHS = 'months'
WEEK = 'week'
WEEKS = 'weeks'
DAY = 'day'
DAYS = 'days'
AND = 'and'


#@register.filter
def smartertimesince(d, now=None):
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        if d.tzinfo:
            raise NotImplementedError
            from django.utils.tzinfo import LocalTimezone
            now = datetime.datetime.now(LocalTimezone(d))
        else:
            now = datetime.datetime.now()

    r = timeSince(d, now, max_no_sections=1, minute_granularity=True)
    if not r:
        return "seconds"
    return r

# Copied and adopted from FriedZopeBase
def timeSince(firstdate, seconddate, afterword=None,
              minute_granularity=False,
              max_no_sections=3):
    """
    Use two date objects to return in plain english the difference between them.
    E.g. "3 years and 2 days"
     or  "1 year and 3 months and 1 day"

    Try to use weeks when the no. of days > 7

    If less than 1 day, return number of hours.

    If there is "no difference" between them, return false.
    """

    def wrap_afterword(result, afterword=afterword):
        if afterword is not None:
            return "%s %s" % (result, afterword)
        else:
            return result

    fdo = firstdate
    sdo = seconddate

    day_difference = abs(sdo-fdo).days

    years = day_difference/365
    months = (day_difference % 365)/30
    days = (day_difference % 365) % 30
    minutes = ((day_difference % 365) % 30) % 24


    if days == 0 and months == 0 and years == 0:
        # use hours
        hours = abs(sdo-fdo).seconds/3600
        if hours == 1:
            return wrap_afterword("1 %s" % (HOUR))
        elif hours > 0:
            return wrap_afterword("%s %s" % (hours, HOURS))
        elif minute_granularity:

            minutes = abs(sdo-fdo).seconds / 60
            if minutes == 1:
                return wrap_afterword("1 %s" % MINUTE)
            elif minutes > 0:
                return wrap_afterword("%s %s" % (minutes, MINUTES))
            else:
                # if the differnce is smaller than 1 minute,
                # return 0.
                return 0
        else:
            # if the difference is smaller than 1 hour,
            # return it false
            return 0
    else:
        s = []
        if years == 1:
            s.append('1 %s'%(YEAR))
        elif years > 1:
            s.append('%s %s'%(years,YEARS))

        if months == 1:
            s.append('1 %s'%MONTH)
        elif months > 1:
            s.append('%s %s'%(months,MONTHS))

        if days == 1:
            s.append('1 %s'%DAY)
        elif days == 7:
            s.append('1 %s'%WEEK)
        elif days == 14:
            s.append('2 %s'%WEEKS)
        elif days == 21:
            s.append('3 %s'%WEEKS)
        elif days > 14:
            weeks = days / 7
            days = days % 7
            if weeks == 1:
                s.append('1 %s'%WEEK)
            else:
                s.append('%s %s'%(weeks, WEEKS))
            if days % 7 == 1:
                s.append('1 %s'%DAY)
            elif days > 0:

                s.append('%s %s'%(days % 7,DAYS))
        elif days > 1:
            s.append('%s %s'%(days,DAYS))

        s = s[:max_no_sections]

        if len(s)>1:
            return wrap_afterword("%s" % (string.join(s,' %s '%AND)))
        else:
            return wrap_afterword("%s" % s[0])
