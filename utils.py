import json

Headers = [
    "User-Agent: Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-TL00 Build/HUAWEITAG-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2570 MMWEBSDK/200601 Mobile Safari/537.36 MMWEBID/7949 MicroMessenger/7.0.16.1700(0x27001034) Process/appbrand2 WeChat/arm32 NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
]

config_path = "./config.json"

def load_config(config_path=config_path):
    with open(config_path, "r", encoding='utf-8') as f:
        config = json.load(f)
    return config

def str2params(sstr):

    params = {}
    for i in sstr.split('&'):
        params[i.split('=')[0]] = i.split('=')[-1]
    print(params)

    return params

class ColorPrint():
    foreground = '\033[38;2;'
    background = '\033[48;2;'
    end = '\033[0m'

    red = (170, 0, 0)
    orange = (215, 120, 45)
    yellow = (245, 210, 70)
    green = (10, 160, 10)
    blue = (30, 80, 190)
    purple = (160, 40, 160)
    white = (255, 255, 255)
    black = (0, 0, 0)

    @staticmethod
    def __color(color):
        return f"{color[0]};{color[1]};{color[2]}"

    @staticmethod
    def print_error(sstr):
        print(f"{ColorPrint.foreground}{ColorPrint.__color(ColorPrint.red)}m{sstr}{ColorPrint.end}")

    @staticmethod
    def print_warning(sstr):
        print(f"{ColorPrint.foreground}{ColorPrint.__color(ColorPrint.orange)}m{sstr}{ColorPrint.end}")

    @staticmethod
    def print_success(sstr):
        print(f"{ColorPrint.foreground}{ColorPrint.__color(ColorPrint.green)}m{sstr}{ColorPrint.end}")

    @staticmethod
    def print_info(sstr):
        print(f"{ColorPrint.foreground}{ColorPrint.__color(ColorPrint.blue)}m{sstr}{ColorPrint.end}")

    @staticmethod
    def print_message(sstr):
        print(f"{ColorPrint.foreground}{ColorPrint.__color(ColorPrint.purple)}m{sstr}{ColorPrint.end}")
