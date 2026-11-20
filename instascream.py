from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import textwrap
import random
import sys
from colorsys import hls_to_rgb, rgb_to_hls
from foreground import get_foreground


def get_random_colour():
    hex_colour = f'{"#%06x" % random.randint(0, 0xFFFFFF)}'
    return hex_colour


def text_on_img(filename='01.jpg', text="AHHHH"):
    fnt = ImageFont.truetype('comic.ttf', 52)
    # create image
    background_colour = get_random_colour()
    image = Image.new(mode="RGB", size=(1080, 1080), color=background_colour)
    draw = ImageDraw.Draw(image)
    # draw text
    # if text is 27 characters or longer then wrap it on a new line
    # (one line can only fit 26 characters with this font size of 52)
    # (there can be 17 lines max with this size of 1080x1080)
    if len(text) >= 27:
        text = "\n".join(textwrap.wrap(text, width=26))

    text_colour = get_foreground(background_colour, output='RGB')
    draw.text((10, 10), text, font=fnt, fill=text_colour)

    # save file
    image.save(filename)

# generate the scream text
# max length = 17 lines * 26 characters per line = 442 characters (1 A and 1-441 Hs)
#


def generate_text():
    num_of_h = random.SystemRandom().randint(1, 441)
    num_of_a = random.SystemRandom().randint(1, 442 - num_of_h)
    return "A" * num_of_a + "H" * num_of_h


if __name__ == "__main__":
    #test = generate_text()
    # print(len(test))
    text_on_img(text=generate_text())
