from httpx import Client
from string import ascii_lowercase, digits
from random import choice

class Afterpay:
    fingerprint = "".join(choice(ascii_lowercase+digits) for _ in range(32))
    API_URL = "https://portalapi.afterpay.com/portal/consumers"
    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://portal.afterpay.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://portal.afterpay.com/",
        "accept-language": "en-US,en;q=0.9"
    }
    next_auth_token = None
    def __init__(self):
        self.session = Client(http2=True)
        self.session.headers = self.headers
    def _req(self, method, route, **kwargs):
        print(f"Method: {method}")
        print(f"URL: {self.API_URL}{route}")
        if self.next_auth_token:
            print(f"Auth token set ({self.next_auth_token}), adding to request")
            if "headers" in kwargs and type(kwargs["headers"]) is dict:
                kwargs["headers"]["x-auth-token"] = self.next_auth_token
            else:
                kwargs["headers"] = {"x-auth-token": self.next_auth_token}
            self.next_auth_token = None
        r = self.session.request(method.upper(), self.API_URL + ("/" if route[0] != "/" else "") + route, **kwargs)
        if "x-auth-token" in r.headers:
            print(f"Auth token received ({r.headers['x-auth-token']}), sending with next request")
            self.next_auth_token = r.headers["x-auth-token"]
        return r
    def get(self, route, **kwargs):
        return self._req("get", route, **kwargs)
    def post(self, route, **kwargs):
        return self._req("post", route, **kwargs)
    def options(self, route, **kwargs):
        return self._req("options", route, **kwargs)
