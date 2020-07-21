import argparse

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reserve', action='store_true', help='start making appointment of library seat')
    parser.add_argument('-u', '--update', action='store_true', help='update reserved information to the local file')
    parser.add_argument('-c', '--cancel', type=str, help='cancel designated order of appointment')
    parser.add_argument('-q', '--qrcode', action='store_true', help='generate qrcode and ticket from local files')
    parser.add_argument('--config', type=str, default="./config.json", help='path of config file')
    return parser.parse_args()