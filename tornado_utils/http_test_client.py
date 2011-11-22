from urllib import urlencode
import Cookie
from tornado.httpclient import HTTPRequest
from tornado import escape

__version__ = '1.3'

class LoginError(Exception):
    pass

class HTTPClientMixin(object):

    def get(self, url, data=None, headers=None, follow_redirects=False):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data, True)
            if '?' in url:
                url += '&%s' % data
            else:
                url += '?%s' % data
        return self._fetch(url, 'GET', headers=headers,
                           follow_redirects=follow_redirects)

    def post(self, url, data, headers=None, follow_redirects=False):
        if data is not None:
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, unicode):
                        data[key] = value.encode('utf-8')
                data = urlencode(data, True)
        return self._fetch(url, 'POST', data, headers,
                           follow_redirects=follow_redirects)

    def _fetch(self, url, method, data=None, headers=None, follow_redirects=True):
        full_url = self.get_url(url)
        request = HTTPRequest(full_url, follow_redirects=follow_redirects,
                              headers=headers, method=method, body=data)
        self.http_client.fetch(request, self.stop)
        return self.wait()


class TestClient(HTTPClientMixin):
    def __init__(self, testcase):
        self.testcase = testcase
        self.cookies = Cookie.SimpleCookie()

    def _render_cookie_back(self):
        return ''.join(['%s=%s;' %(x, morsel.value)
                        for (x, morsel)
                        in self.cookies.items()])

    def get(self, url, data=None, headers=None, follow_redirects=False):
        if self.cookies:
            if headers is None:
                headers = dict()
            headers['Cookie'] = self._render_cookie_back()
        response = self.testcase.get(url, data=data, headers=headers,
                                     follow_redirects=follow_redirects)

        self._update_cookies(response.headers)
        return response

    def post(self, url, data, headers=None, follow_redirects=False):
        if self.cookies:
            if headers is None:
                headers = dict()
            headers['Cookie'] = self._render_cookie_back()
        response = self.testcase.post(url, data=data, headers=headers,
                                     follow_redirects=follow_redirects)
        self._update_cookies(response.headers)
        return response

    def _update_cookies(self, headers):
        try:
            sc = headers['Set-Cookie']
            self.cookies.update(Cookie.SimpleCookie(
              escape.native_str(sc)))
        except KeyError:
            return

    def login(self, email, password, url='/auth/login/'):
        data = dict(email=email, password=password)
        response = self.post(url, data, follow_redirects=False)
        if response.code != 302:
            raise LoginError(response.body)
        if 'Error' in response.body:
            raise LoginError(response.body)
