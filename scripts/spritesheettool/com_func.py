import os
import math
import logging
import numpy as np
from PIL import Image
from . import spritesheet

def get_sprite_sheet_by_split_data(
        img_path,
        split_data: spritesheet.SpriteSheetSplitData
) -> spritesheet.SpriteSheet:
    if not os.path.exists(img_path):
        logging.error(f'img path not exists: {img_path}')
    img = Image.open(img_path)
    img_w, img_h = img.size
    sp = spritesheet.SpriteSheet(img_path, img_w, img_h)
    total_row, total_col = split_data.rc
    sprite_w, sprite_h = split_data.sprite_size
    if split_data.mode == spritesheet.SplitMode.GRID_BY_CELL_COUNT:
        sprite_h = math.ceil(
            (img_h - (split_data.rc.x - 1) * split_data.padding.y) / split_data.rc.x
        )
        sprite_w = math.ceil(
            (img_w - (split_data.rc.y - 1) * split_data.padding.x) / split_data.rc.y
        )
    elif split_data.mode == spritesheet.SplitMode.GRID_BY_CELL_SIZE:
        total_col = math.ceil(
            (img_w - split_data.offset.x + split_data.padding.x) / (split_data.sprite_size.x + split_data.padding.x)
        )
        total_row = math.ceil(
            (img_h - split_data.offset.y + split_data.padding.y) / (split_data.sprite_size.y + split_data.padding.y)
        )
    else:
        logging.error(f'error mode: {split_data.mode}')
    for col in range(total_col):
        for row in range(total_row):
            x = split_data.offset.x + col * (sprite_w + split_data.offset.x)
            y = split_data.offset.y + row * (sprite_h + split_data.offset.y)
            crop_img = img.crop((x, y, x + sprite_w, y + sprite_h))
            alpha = np.array(crop_img.getchannel('A'))
            if np.all(alpha == 0):
                continue
            sp.append_sprite_rect(x, y, sprite_w, sprite_h)
    return sp