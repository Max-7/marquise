import pathlib
import argparse
from PIL import Image, ImageDraw, ImageFont

import qrcode


MENU_TYPES = {
    "Drinks": ("Boissons", 310, 90),
    "Snacks": ("Snacks", 250, 90),
}


def generate_text_image(text, width, height):
    img = Image.new("RGB", (width, height), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("Roboto-Bold.ttf", 70)
    d.text((10, 5), text, fill=(0, 0, 0), font=font)
    return img


def generate_qr_code(uri, text):
    qr_code = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, border=4, box_size=20)
    qr_code.add_data(uri)
    qr_code.make()
    qr_img = qr_code.make_image()
    height = 40 if text else 0
    final_img = Image.new("RGB", (qr_img.size[0], qr_img.size[1] + height), (255, 255, 255))
    final_img.paste(qr_img, (0, height))

    if text:
        text_img = generate_text_image(*MENU_TYPES[text])
        x = qr_img.size[0] / 2 - text_img.size[0] / 2
        final_img.paste(text_img, (int(x), 10))

    return final_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("uri")
    parser.add_argument("-o", "--output", type=pathlib.Path, default="qrcode.png")
    parser.add_argument("-t", "--text", type=str, choices=["Snacks", "Drinks", None], required=False)

    args = parser.parse_args()
    img = generate_qr_code(args.uri, args.text)
    img.save(args.output)
