import os, re
import logging
from subprocess import Popen, PIPE

def get_git_revision():
    return _get_git_revision()

def _get_git_revision():
    # this is actually very fast. Takes about 0.01 seconds on my machine!
    home = os.path.dirname(__file__)
    proc = Popen('cd %s;git log --no-color -n 1 --date=iso' % home,
                  shell=True, stdout=PIPE, stderr=PIPE)
    output = proc.communicate()
    try:
        date = [x.split('Date:')[1].split('+')[0].strip() for x in
                output[0].splitlines() if x.startswith('Date:')][0]
        date_wo_tz = re.split('-\d{4}', date)[0].strip()
        return date_wo_tz
    except IndexError:
        logging.debug("OUTPUT=%r" % output[0], exc_info=True)
        logging.debug("ERROR=%r" % output[1])
        return 'unknown'
