import os
import re
import time
import json
import copy
import string
import random
import requests

from urllib import parse
from http.cookies import SimpleCookie
from requests.cookies import cookiejar_from_dict

from utils import ColorPrint as cp
from utils import str2params
from ticket import Ticket

class BaseSession:

    def __init__(self, sess=None):
        self.sess = sess if sess else requests.session()


class Reserver(BaseSession):

    config_path = "./config.json"
    record_path = "./record"

    base_url = 'https://yhkj.cylibyj.com'

    url_suffix = "1001"
    url_query = "/Service.asmx/makeapp_load" + url_suffix
    url_submit = "/Service.asmx/makeapp_submit" + url_suffix
    url_cancel = "/Service.asmx/makeapporder_cancel" + url_suffix
    url_check_list = "/Service.asmx/makeapporder_lists" + url_suffix

    interval_time = [3, 7] # TODO


    def __init__(self, sess=None, args=None):
        super().__init__(sess)
        self.__config_sess(args)
        self.__config_path()
        self.create_virtual_openid()
        self.start_time = time.time()

    def __config_sess(self, args=None):

        if args:
            self.config_path = args.config
        config = self.load_config()

        # raw_cookie = config['buff']['requests_kwargs']['cookie']
        # simple_cookie = SimpleCookie(raw_cookie)
        # cookie_dict = {key: morsel.value for key, morsel in simple_cookie.items()}
        # self.sess.cookies = cookiejar_from_dict(cookie_dict)

        self.sess.headers['User-Agent'] = config['chaoyang']['requests_kwargs']['headers']['User-Agent'] # TODO use various User-Agent

        self.params = config['chaoyang']['payload']
        # params['date'] = f"{params['site']}${params['date']}${params['time']}"
        # # params.pop('site')
        # # params.pop('time') # TODO Potential bug

    def __config_path(self):

        if not os.path.exists(self.record_path):
            os.makedirs(self.record_path)

    def _post_payload(self, buff_api, params=None):

        params = params if params else self.params
        post_res = self.sess.post(buff_api, json=params)

        if post_res.status_code != 200:
            post_json = json.loads(post_res.text)
            cp.print_error(f"Post error! {post_json['Message']}")
            exit(-1)
            # raise Exception("Fail to post!")
        else:
            cp.print_message("Post successfully!")

        post_text = post_res.text.replace('{"d":null}', '')

        ## Regular expression to deprive useless '{"d":null}' suffix is deprecated
        # text_pattern = re.compile(r'{(.+?)}', re.S)
        # post_text = text_pattern.findall(post_res.text)
        # post_text =  f"{{{post_text[0]}}}"
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

    def load_config(self):
        with open(self.config_path, "r", encoding='utf-8') as f:
            config = json.load(f)
        return config

    def save_json(self, content, file_path):

        json_dict = json.dumps(content, ensure_ascii=False, indent=4)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_dict)
            cp.print_success(f"Write to {file_path} successfully!")

    def create_virtual_openid(self, openid_len=64):
        config = self.load_config()
        if not config["chaoyang"]["payload"]["openid"]:
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=openid_len))
            cp.print_success(f"Create virtual openid successfully: {rand_str}")
            config["chaoyang"]["payload"]["openid"] = rand_str

            self.save_json(config, self.config_path)

    def reserve_seat(self):

        # if self.params["time"]:
        #     time = [self.params["time"]]
        # else:
        #     time = ["上午", "下午"]

        # for t in time:
        ## remove time

        params = copy.deepcopy(self.params)

        params['date'] = f"{params['site']}${params['date']}"
        params.pop('site')
        params.pop('time')

        while True:
            self.end_time = time.time()
            r_num = random.uniform(self.interval_time[0], self.interval_time[1])
            if self.end_time - self.start_time < self.interval_time[0]:
                cp.print_message(f"sleep {r_num:.2f}s, current time: {time.strftime('%H:%M:%S')}")
                time.sleep(r_num)

            post_json = self._post_payload(self.base_url + self.url_submit, params)
            self.start_time = time.time()

            if post_json["reply"] == "ok":
                print(post_json["list"][0]["msg"])
                break
            # elif post_json["reply"] == "error": # TODO potential bug: other error string
            else:
                cp.print_error(f'Error: {post_json["msg"]}')

        # datetime = self.params["date"]+t
        datetime = self.params["date"]
        self.save_json(post_json, f"{self.record_path}/{datetime}.json")

        self.check_list()

    def check_list(self, con='u'):

        assert con in ["a", "u"] # a: all, u: unused

        params = {
            "openid": self.params["openid"],
            "con": con,
            "pages": 1 # TODO potential bug
        }

        post_json = self._post_payload(self.base_url + self.url_check_list, params)
        self.save_json(post_json, f"{self.record_path}/check_list.json")
        self.create_ticket()

    def cancel_reserve(self, order):

        if not order:
            cp.print_error("Order id should no be empty!")
            exit(-1)

        params = {
            "order": order,
        }

        post_json = self._post_payload(self.base_url + self.url_cancel, params)

        if post_json["reply"] == "ok":
            cp.print_warning(f'Cancel order "{order}" successfully! {post_json["order_cancel"]}')
            cp.print_info("Please check appointment information 'check_list.json' for more detail.")
        # elif post_json["reply"] == "error": # TODO potential bug: other error string
        else:
            cp.print_error(f'Cancel order "{order}" failed! {post_json["msg"]}')

        self.check_list()

    def create_ticket(self):

        identity = f'{self.params["name"]} {self.params["idcard"]}'
        ticket = Ticket(identity)