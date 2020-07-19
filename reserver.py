import re
import time
import json
import random
import requests

from urllib import parse
from http.cookies import SimpleCookie
from requests.cookies import cookiejar_from_dict

from utils import ColorPrint as cp
from utils import load_config, str2params

class BaseSession:

    def __init__(self, sess=None):
        self.sess = sess if sess else requests.session()


class Reserver(BaseSession):

    base_url = 'https://yhkj.cylibyj.com'

    url_submit = "/Service.asmx/makeapp_submit"
    url_query = "/Service.asmx/makeapp_load"
    url_check_list = "/Service.asmx/makeapporder_lists"

    interval_time = [3, 7] # TODO


    def __init__(self, sess=None):
        super().__init__(sess)
        self.__config_sess()
        self.start_time = time.time()

    def __config_sess(self):

        config = load_config()

        # raw_cookie = config['buff']['requests_kwargs']['cookie']
        # simple_cookie = SimpleCookie(raw_cookie)
        # cookie_dict = {key: morsel.value for key, morsel in simple_cookie.items()}
        # self.sess.cookies = cookiejar_from_dict(cookie_dict)

        self.sess.headers['User-Agent'] = config['chaoyang']['requests_kwargs']['headers']['User-Agent'] # TODO use various User-Agent

        params = config['chaoyang']['payload']
        params['date'] = f"{params['site']}${params['date']}${params['time']}"
        params.pop('site')
        params.pop('time')
        self.params = params

    def _post_payload(self, buff_api, params=None):

        params = params if params else self.params
        post_res = self.sess.post(buff_api, json=params)

        if post_res.status_code != 200:
            raise Exception("fail to post!")
        else:
            cp.print_success("Post successfully!")

        text_pattern = re.compile(r'{(.+?)}', re.S)

        post_text = text_pattern.findall(post_res.text)
        post_text =  f"{{{post_text[0]}}}"
        post_json = json.loads(post_text)

        return post_json

    def _get_data(self, buff_api, params=None):

        self.end_time = time.time()
        r_num = random.uniform(self.interval_time[0], self.interval_time[1])
        if self.end_time - self.start_time  < self.interval_time[0]:
            cp.print_message(f"sleep {r_num:.2f}s")
            time.sleep(r_num)

        api_request = self.sess.get(buff_api, params=params)
        # print(api_request.url)
        self.start_time = time.time()

        if api_request.status_code != 200:
            raise Exception("fail to request api!")

        data = api_request.json()
        if data["code"] == "Login Required":
            raise Exception("login required!")
        if data["code"] == "Invalid Argument":
            raise Exception("Invalid Argument!")

        return data["data"]

    def create_virtual_openid(self):
        pass

    def reserve_seat(self):

        post_json = self._post_payload(self.base_url + self.url_submit)
        print(post_json)


    def check_list(self):
        tmp = "openid=1&con=a&pages=1"
        params = str2params(tmp)

        post_json = self._post_payload(self.base_url + self.url_check_list, params)
        print(post_json)