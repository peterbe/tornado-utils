from urllib import quote as url_quote
from tornado.web import HTTPError

def login_required(func, redirect_to=None):
    def is_logged_in(self):
        guid = self.get_secure_cookie('user')
        if guid:
            if self.db.users.User(dict(guid=guid)):
                return func(self)
        if redirect_to:
            next = self.request.path
            if self.request.query:
                next += '?%s' % self.request.query
            url = redirect_to + '?next=%s' % url_quote(next)
            self.redirect(url)
        else:
            raise HTTPError(403, "Must be logged in")
    return is_logged_in

def login_redirect(func):
    return login_required(func, redirect_to='/login/')

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
