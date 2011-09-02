EMAIL_HOST = 'smtp.elasticemail.com'
EMAIL_PORT = 2525

EMAIL_HOST_USER = 'mail@peterbe.com'
EMAIL_HOST_PASSWORD = '67255e4d-f88b-4e6a-a7d3-c8a6bfea8ea3'

EMAIL_USE_TLS = False

import os
op = os.path
PICKLE_LOCATION = op.join(op.dirname(__file__), 'pickled_messages')
if not op.isdir(PICKLE_LOCATION):
    os.mkdir(PICKLE_LOCATION)
