from urllib import quote as url_quote
from tornado.web import HTTPError
import base64

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


def basic_auth(checkfunc, realm="Authentication Required!"):
    """Decorate methods with this to require basic auth"""
    def wrap(method):
        def request_auth(self):
            self.set_header('WWW-Authenticate', 'Basic realm=%s' % realm)
            self.set_status(401)
            self.finish()
            return False
        
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            auth = self.request.headers.get('Authorization')
            if auth is None or not auth.startswith('Basic '):
                return request_auth(self)
            auth = auth[6:]
            try:
                username, password = base64.decodestring(auth).split(':', 2)
            except:
                return request_auth(self)
            
            if checkfunc(username, password):
                self.request.basic_auth = (username, password)
                return method(self, *args, **kwargs)
            else:
                return request_auth(self)
                
        return wrapper
    
    return wrap
