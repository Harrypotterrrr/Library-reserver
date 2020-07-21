import json
import qrcode

from PIL import Image, ImageDraw, ImageFont

from utils import ColorPrint as cp

class Ticket():

    ticket_path = "./record"

    def __init__(self, file_path, identity):

        self.__load_params(file_path)
        self.params["identity"] = identity

        img_name = f'{self.params["Date"]}{self.params["Session"][:2]}.png'

        ticket_path = self.ticket_path + f'/{img_name}' # original ticket
        cticket_path = self.ticket_path + f'/d_{img_name}' # compressed ticket

        self.w, self.h = 900, 1100
        self.interval_y1, self.interval_y2 = 70, 50

        self.font_type = './Deng.ttf'
        self.font_size1, self.font_size2 = 55, 35
        self.font1 = ImageFont.truetype(self.font_type, self.font_size1)
        self.font2 = ImageFont.truetype(self.font_type, self.font_size2)

        self.color = "#000000"

        self.wallpaper = Image.new("RGB", (self.w, self.h), "white")
        self.draw = ImageDraw.Draw(self.wallpaper)

        self.draw_header()
        self.draw_qrcode(self.create_qrcode())
        self.draw_content()


        self.wallpaper.save(ticket_path, 'png')

        ticket_img = Image.open(ticket_path)
        cticket_img = ticket_img.resize((self.w // 2, self.h // 2), Image.ANTIALIAS)
        cticket_img.save(cticket_path)

        cp.print_success(f"Successfully create library ticket for {img_name}")

    def __load_params(self, file_path, k = 0):

        with open(file_path, "r", encoding='utf-8') as f:
            config = json.load(f)

        assert config["reply"] == "ok"

        self.params = {}
        self.params["id"] = config["list"][k]["id"]
        self.params["order"] = config["list"][k]["order"]
        self.params["libname"] = config["list"][k]["libname"]
        self.params["Date"] = config["list"][k]["Date"]
        self.params["Session"] = config["list"][k]["Session"]
        self.params["Locationid"] = config["list"][k]["Locationid"]
        self.params["note"] = config["list"][k]["note"]
        self.params["time"] = config["list"][k]["time"]

    def draw_header(self):

        header = f'订单号：{self.params["order"]}'
        status = "状态 预约成功"

        header_w, header_h = self.draw.textsize(header, font=self.font1)
        status_w, status_y = self.draw.textsize(status, font=self.font2)

        header_x, header_y = (self.w - header_w) // 2, 80
        status_x, status_y = (self.w - status_w) // 2, header_y + self.interval_y1

        self.draw.text((header_x, header_y), header, self.color, font=self.font1)
        self.draw.text((status_x, status_y), status, self.color, font=self.font2)

    def draw_qrcode(self, img):

        img_w, img_h = img.size
        qrcode_x, qrcode_y = (self.w - img_w) // 2, 250

        self.wallpaper.paste(img, (qrcode_x, qrcode_y))

    def draw_content(self):

        datetime = f'{self.params["Date"]} {self.params["Session"]}'
        location = f'进馆序号：{self.params["Locationid"]}'

        libname_w, libname_h = self.draw.textsize(self.params["libname"], font=self.font1)
        datetime_w, datetime_h = self.draw.textsize(datetime, font=self.font2)
        location_w, location_h = self.draw.textsize(location, font=self.font2)
        indentity_w, identity_h = self.draw.textsize(self.params["identity"], font=self.font2)

        libname_x, libname_y = (self.w - libname_w) // 2, 820
        datetime_x, datetime_y = (self.w - datetime_w) // 2, libname_y + self.interval_y1
        location_x, location_y = (self.w - location_w) // 2, datetime_y + self.interval_y2
        indentity_x, identity_y = (self.w - indentity_w) // 2, location_y + self.interval_y2

        self.draw.text((libname_x, libname_y), self.params["libname"], self.color, self.font1)
        self.draw.text((datetime_x, datetime_y), datetime, self.color, self.font2)
        self.draw.text((location_x, location_y), location, self.color, self.font2)
        self.draw.text((indentity_x, identity_y), self.params["identity"], self.color, self.font2)

    def create_qrcode(self):

        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M ,
            box_size=20,
            border=1,
        )
        qr.add_data("202007212000437282")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        return img

if __name__ == "__main__":

    ticket = Ticket("./record/check_list.json", "贾昊霖 110xxxxxxxxxxxxxxx")
