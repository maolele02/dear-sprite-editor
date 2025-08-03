import os
from encodings.idna import sace_prefix

import cv2
import math
import logging
import numpy as np
from PIL import Image

import core.math
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
    if split_data.mode in [spritesheet.SplitMode.GRID_BY_CELL_SIZE, spritesheet.SplitMode.GRID_BY_CELL_COUNT]:
        for col in range(total_col):
            for row in range(total_row):
                x = split_data.offset.x + col * (sprite_w + split_data.offset.x)
                y = split_data.offset.y + row * (sprite_h + split_data.offset.y)
                crop_img = img.crop((x, y, x + sprite_w, y + sprite_h))
                alpha = np.array(crop_img.getchannel('A'))
                if np.all(alpha == 0):
                    continue
                sp.append_sprite_rect(x, y, sprite_w, sprite_h)
    elif split_data.mode == spritesheet.SplitMode.AUTOMATIC:
        rects = find_contours_with_transparency(img_path, min_area=split_data.automatic_min_area)
        sp.extend_sprite_rects(rects)
    else:
        logging.error(f'error mode: {split_data.mode}')
    return sp

def find_contours_with_transparency(image_path, min_area=64):
    rectangles = []
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        logging.error(f'can not load image file: {image_path}')
        return rectangles

    # 检查是否有alpha通道
    if image.shape[2] == 4:
        # 分离alpha通道
        alpha = image[:, :, 3]
        # 创建二值化图像（全透明像素为0，非透明像素为1）
        binary = (alpha > 0).astype(np.uint8) * 255
    else:
        # 如果没有alpha通道，将整个图像视为不透明
        binary = np.ones(image.shape[:2], dtype=np.uint8) * 255

    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 处理每个轮廓
    for contour in contours:
        # 计算轮廓面积
        area = cv2.contourArea(contour)
        # 忽略太小的轮廓
        if area < min_area:
            continue
        # 获取边界矩形
        x, y, w, h = cv2.boundingRect(contour)
        rectangles.append(core.math.Rect(x, y, w, h))
    return rectangles