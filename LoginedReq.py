# _*_ coding=utf-8 _*_
"""
获得一个已经登陆github的请求
"""
import re

import requests

from headers import headers


class GetLoginnReq:
    """
    这个类处理登陆github，并返回一个包含了登陆后的cookies的会话请求
    """

    def __init__(self, req):
        self.req = req

    def get_auth_value(self):
        """
        用于返回post请求中用于提交的authenticity_token参数
        """
        r = self.req.get(url="https://github.com/login", headers=headers, verify=False)
        if r.status_code == requests.codes.ok:
            try:
                pattern = re.compile('name="authenticity_token" value="(.*?==)"')
                auth_value = re.search(pattern, r.text).group(1)
                return auth_value
            except AttributeError:
                print("Not such value")

    def login_github(self):
        """
        登陆github的方法, 方法的结果是得到了登陆后第一个页面的响应。
        """
        data = {

            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token": self.get_auth_value(),
            "login": "mikeyumingtao",
            "password": "killer960416",
            "webauthn-support": "supported"

            }
        self.req.post(url="https://github.com/session", headers=headers, data=data, verify=False)


reqObject = requests.session()
S = GetLoginnReq(reqObject)
S.get_auth_value()
S.login_github()

if __name__ == "__main__":
    print(reqObject)

