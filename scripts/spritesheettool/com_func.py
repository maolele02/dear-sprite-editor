import json
import math
import pathlib
import logging
import core.math
from PIL import Image
from . import spritesheet

def get_sprite_sheet_by_sprite_size(
    sprite_w, sprite_h,
    img,
    img_w, img_h,
    offset_x, offset_y,
    padding_x, padding_y
) -> spritesheet.SpriteSheet:
    sp = spritesheet.SpriteSheet(img, img_w, img_h)
    total_col = math.ceil((img_w - offset_x) / (sprite_w + padding_x))
    total_row = math.ceil((img_h - offset_y) / (sprite_h + padding_y))
    for col in range(total_col):
        for row in range(total_row):
            x = offset_x + col * (sprite_w + offset_x)
            y = offset_y + row * (sprite_h + offset_y)
            sp.append_sprite_rect(x, y, sprite_w, sprite_h)
    return sp
