from urllib import quote as url_quote
from tornado.web import HTTPError

import functools
import urllib
import urlparse
# taken from tornado.web.authenticated

def authenticated_plus(extra_check):
    """Decorate methods with this to require that the user be logged in."""
    def wrap(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not (self.current_user and extra_check(self.current_user)):
                if self.request.method in ("GET", "HEAD"):
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            # if login url is absolute, make next absolute too
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urllib.urlencode(dict(next=next_url))
                    self.redirect(url)
                    return
                raise HTTPError(403)
            return method(self, *args, **kwargs)
        return wrapper
    return wrap
