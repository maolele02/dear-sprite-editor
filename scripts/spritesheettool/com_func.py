import math
import logging
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

def get_sprite_sheet_by_split_data(
        img,
        img_w, img_h,
        split_data: spritesheet.SpriteSheetSplitData
) -> spritesheet.SpriteSheet:
    sp = spritesheet.SpriteSheet(img, img_w, img_h)
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
            sp.append_sprite_rect(x, y, sprite_w, sprite_h)
    return sp