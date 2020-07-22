import json
import qrcode

from PIL import Image, ImageDraw, ImageFont

from utils import ColorPrint as cp

class Ticket():

    ticket_path = "./record"

    def __init__(self, identity, file_path="./record/check_list.json"):

        self.__load_params(file_path, identity)

        for payload in self.params:
            self.create_ticket(payload)

    def __load_params(self, file_path, identity):

        with open(file_path, "r", encoding='utf-8') as f:
            config = json.load(f)

        assert config["reply"] == "ok"

        self.params = []

        for item in (config["list"]):
            if item["note"] != "预约成功":
                continue
            tmp_dict = {}
            tmp_dict["id"] = item["id"]
            tmp_dict["order"] = item["order"]
            tmp_dict["libname"] = item["libname"]
            tmp_dict["Date"] = item["Date"]
            tmp_dict["Session"] = item["Session"]
            tmp_dict["Locationid"] = item["Locationid"]
            tmp_dict["note"] = item["note"]
            tmp_dict["time"] = item["time"]
            tmp_dict["identity"] = identity

            self.params.append(tmp_dict)

    def create_ticket(self, payload):

        img_name = f'{payload["Date"]}{payload["Session"][:2]}.png'

        ticket_path = self.ticket_path + f'/{img_name}'  # original ticket
        cticket_path = self.ticket_path + f'/d_{img_name}'  # compressed ticket

        self.w, self.h = 900, 1050
        self.interval_y1, self.interval_y2 = 70, 50

        self.font_type = 'Deng' # TODO potential bug for Mac system: ttf format is not supported
        self.font_size1, self.font_size2 = 55, 35
        self.font1 = ImageFont.truetype(self.font_type, self.font_size1)
        self.font2 = ImageFont.truetype(self.font_type, self.font_size2)

        self.color = "#000000"

        self.wallpaper = Image.new("RGB", (self.w, self.h), "white")
        self.draw = ImageDraw.Draw(self.wallpaper)

        # Begin drawing
        self.draw_header(payload)
        self.draw_qrcode(self.create_qrcode(payload["order"]))
        self.draw_content(payload)

        self.wallpaper.save(ticket_path, 'png')

        # Create compressed ticket image
        # ticket_img = Image.open(ticket_path)
        # cticket_img = ticket_img.resize((self.w // 2, self.h // 2), Image.ANTIALIAS)
        # cticket_img.save(cticket_path)

        cp.print_success(f"Successfully create library ticket for {img_name}")

    def draw_header(self, payload):

        header = f'订单号：{payload["order"]}'
        status = "状态 预约成功"

        header_w, header_h = self.draw.textsize(header, font=self.font1)
        status_w, status_y = self.draw.textsize(status, font=self.font2)

        header_x, header_y = (self.w - header_w) // 2, 80
        status_x, status_y = (self.w - status_w) // 2, header_y + self.interval_y1

        self.draw.text((header_x, header_y), header, self.color, font=self.font1)
        self.draw.text((status_x, status_y), status, self.color, font=self.font2)

    def draw_qrcode(self, img):

        img_w, img_h = img.size
        qrcode_x, qrcode_y = (self.w - img_w) // 2, 200

        self.wallpaper.paste(img, (qrcode_x, qrcode_y))

    def draw_content(self, payload):

        datetime = f'{payload["Date"]} {payload["Session"]}'
        location = f'进馆序号：{payload["Locationid"]}'

        libname_w, libname_h = self.draw.textsize(payload["libname"], font=self.font1)
        datetime_w, datetime_h = self.draw.textsize(datetime, font=self.font2)
        location_w, location_h = self.draw.textsize(location, font=self.font2)
        indentity_w, identity_h = self.draw.textsize(payload["identity"], font=self.font2)

        libname_x, libname_y = (self.w - libname_w) // 2, 770
        datetime_x, datetime_y = (self.w - datetime_w) // 2, libname_y + self.interval_y1
        location_x, location_y = (self.w - location_w) // 2, datetime_y + self.interval_y2
        indentity_x, identity_y = (self.w - indentity_w) // 2, location_y + self.interval_y2

        self.draw.text((libname_x, libname_y), payload["libname"], self.color, self.font1)
        self.draw.text((datetime_x, datetime_y), datetime, self.color, self.font2)
        self.draw.text((location_x, location_y), location, self.color, self.font2)
        self.draw.text((indentity_x, identity_y), payload["identity"], self.color, self.font2)

    def create_qrcode(self, order):

        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M ,
            box_size=20,
            border=1,
        )
        qr.add_data(order)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        return img

if __name__ == "__main__":

    ticket = Ticket("./record/check_list.json", "贾xx 110xxxxxxxxxxxxxxx")
