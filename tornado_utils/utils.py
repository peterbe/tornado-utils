import os
import re
import datetime
import random
try:
    import bcrypt
except ImportError:
    # it'd be a shame to rely on this existing
    bcrypt = None


class djangolike_request_dict(dict):
    def getlist(self, key):
        value = self.get(key)
        return self.get(key)

class DatetimeParseError(Exception):
    pass

_timestamp_regex = re.compile('\d{13}|\d{10}\.\d{0,4}|\d{10}')
def parse_datetime(datestr):
    _parsed = _timestamp_regex.findall(datestr)
    if _parsed:
        datestr = _parsed[0]
        if len(datestr) >= len('1285041600000'):
            try:
                return datetime.datetime.fromtimestamp(float(datestr)/1000)
            except ValueError:
                pass
        if len(datestr) >= len('1283140800'):
            try:
                return datetime.datetime.fromtimestamp(float(datestr))
            except ValueError:
                pass # will raise
    raise DatetimeParseError(datestr)

def datetime_to_date(dt):
    return datetime.date(dt.year, dt.month, dt.day)

def encrypt_password(raw_password, log_rounds=10):
    if not bcrypt:
        raise SystemError("bcrypt could no be imported")
    salt = bcrypt.gensalt(log_rounds=log_rounds)
    hsh = bcrypt.hashpw(raw_password, salt)
    algo = 'bcrypt'
    return u'%s$bcrypt$%s' % (algo, hsh)


def niceboolean(value):
    if type(value) is bool:
        return value
    falseness = ('','no','off','false','none','0', 'f')
    return str(value).lower().strip() not in falseness



email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain
def valid_email(email):
    return bool(email_re.search(email))


def mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                    "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        if tail:
            os.mkdir(newdir)

from random import choice
from string import letters
def random_string(length):
    return ''.join(choice(letters) for i in xrange(length))


def all_hash_tags(tags, title):
    """return true if all tags in the title were constructed with a '#' instead
    of a '@' sign"""
    for tag in tags:
        if re.findall(r'(^|\s)@%s\b' % re.escape(tag), title):
            return False
    return True

def all_atsign_tags(tags, title):
    """return true if all tags in the title were constructed with a '@' instead
    of a '#' sign"""
    for tag in tags:
        if re.findall(r'(^|\s)#%s\b' % re.escape(tag), title):
            return False
    return True

def format_time_ampm(time_or_datetime):
    if isinstance(time_or_datetime, datetime.datetime):
        h = int(time_or_datetime.strftime('%I'))
        ampm = time_or_datetime.strftime('%p').lower()
        if time_or_datetime.minute:
            m = time_or_datetime.strftime('%M')
            return "%s:%s%s" % (h, m, ampm)
        else:
            return "%s%s" % (h, ampm)
    elif isinstance(time_or_datetime, (tuple, list)) and len(time_or_datetime) >= 2:
        h = time_or_datetime[0]
        m = time_or_datetime[1]
        assert isinstance(h, int), type(h)
        assert isinstance(m, int), type(m)
        ampm = 'am'
        if h > 12:
            ampm = 'pm'
            h -= 12
        if m:
            return "%s:%s%s" % (h, m, ampm)
        else:
            return "%s%s" % (h, ampm)
    else:
        raise ValueError("Wrong parameter to this function")


def generate_random_color():
    def dec2hex(d):
        return "%02X" % d
    return '#%s%s%s' % (
      dec2hex(random.randint(0, 255)),
      dec2hex(random.randint(0, 255)),
      dec2hex(random.randint(0, 255)),
    )
