"""Pickling email sender"""

import time
import datetime
import os.path
import cPickle
import logging
from utils.send_mail.backends.base import BaseEmailBackend
from utils.send_mail import config

class EmailBackend(BaseEmailBackend):

    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)
        self.location = config.PICKLE_LOCATION
        self.protocol = getattr(config, 'PICKLE_PROTOCOL', 0)

        # test that we can write to the location
        open(os.path.join(self.location, 'test.pickle'), 'w').write('test\n')
        os.remove(os.path.join(self.location, 'test.pickle'))

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return

        num_sent = 0
        for message in email_messages:
            if self._pickle(message):
                num_sent += 1
        return num_sent

    def _pickle(self, message):
        t0 = time.time()
        filename = self._pickle_actual(message)
        t1 = time.time()
        logging.debug("Took %s seconds to create %s" % \
                      (t1 - t0, filename))
        return True

    def _pickle_actual(self, message):
        filename_base = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        c = 0
        filename = os.path.join(self.location,
                                filename_base + '_%s.pickle' % c)
        while os.path.isfile(filename):
            c += 1
            filename = os.path.join(self.location,
                                    filename_base + '_%s.pickle' % c)
        cPickle.dump(message, open(filename, 'wb'), self.protocol)
        return filename
