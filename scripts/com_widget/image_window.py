import math
from core.math import *
from spritesheettool import spritesheet
import dearpygui.dearpygui as dpg

__all__ = [
    'ImageWindow',
]

from spritesheettool.spritesheet import SpriteSheetSplitData


class ImageWindow(object):
    def __init__(self, parent):
        self._parent = parent
        self._win = 0
        self._texture = 0
        self._draw_list = 0
        self._bg_layer = 0
        self._img_layer = 0
        self._box_layer = 0
        self._img_path = ''
        self._scale = 1.0
        self._img_size = Vector2()
        self._split_data: spritesheet.SpriteSheetSplitData = SpriteSheetSplitData()
        self._init_split_data()

    def create(self):
        self._win = dpg.add_child_window(parent=self._parent, horizontal_scrollbar=True, show=False)

    def get_guid(self):
        return self._win

    def set_image(self, image):
        self._load_img(image)

    def get_image_path(self):
        return self._img_path

    def get_image_size(self):
        return self._img_size

    def set_scale(self, scale: float):
        self._scale = scale
        self._rebuild_draw_list()

    def get_split_data(self):
        return self._split_data

    def get_mode(self):
        return self.split_data.mode

    def set_mode(self, mode):
        if mode == self.split_data.mode:
            return
        self.split_data.mode = mode
        self.split_data.offset = Vector2(0, 0)
        self.split_data.padding = Vector2(0, 0)
        self.refresh()

    def refresh(self):
        if self._texture > 0:
            self._rebuild_draw_list()

    def _init_split_data(self):
        data = self._split_data
        data.sprite_size = Vector2(16, 16)
        data.rc = Vector2(1, 1)

    def _load_img(self, img_path):
        self._img_path = img_path
        w, h, channels, data = dpg.load_image(img_path)
        self._img_size.x = w
        self._img_size.y = h
        with dpg.texture_registry(show=False):
            self._texture = dpg.add_static_texture(w, h, data)

    def _rebuild_draw_list(self):
        self._del_draw_list()
        w, h = self._img_size * self._scale
        with dpg.drawlist(width=w, height=h, parent=self._win) as draw_list:
            self._bg_layer = dpg.add_draw_layer()
            self._img_layer = dpg.add_draw_layer()
            self._box_layer = dpg.add_draw_layer()
            self._draw_list = draw_list
        self._reset_bg_layer()
        self._reset_img_layer()
        self._rest_box_layer()

    def _del_draw_list(self):
        if self._draw_list > 0:
            dpg.delete_item(self._draw_list)
            self._draw_list = 0
            self._bg_layer = 0

    def _reset_bg_layer(self):
        w, h = self._img_size * self._scale
        self._bg_layer = dpg.add_draw_layer(parent=self._draw_list)
        rect_length = 8
        total_col = math.ceil(w / rect_length)
        total_row = math.ceil(h / rect_length)
        grey = (190, 190, 190, 127)
        white = (0, 0, 0, 127)
        for row in range(total_row):
            for col in range(total_col):
                if (
                    row % 2 == 0 and col % 2 != 0 or
                    row % 2 == 1 and col % 2 == 0
                ):
                    color = white
                else:
                    color = grey
                top_left = col * rect_length, row * rect_length
                right_down = top_left[0] + rect_length, top_left[1] + rect_length
                dpg.draw_rectangle(
                    top_left,
                    right_down,
                    color=color,
                    thickness=1,
                    fill=color,
                    parent=self._bg_layer
                )

    def _reset_img_layer(self):
        w, h = self._img_size * self._scale
        self._img_layer = dpg.add_draw_layer(parent=self._draw_list)
        dpg.draw_image(
            self._texture,
            pmin=(0, 0),
            pmax=(w, h),
            uv_min=(0, 0),
            uv_max=(1, 1),
            parent=self._img_layer
        )

    def _rest_box_layer(self):
        row, col = self.split_data.rc
        cell_w, cell_h = self.split_data.sprite_size * self._scale
        padding_x, padding_y = self.split_data.padding * self._scale
        offset_x, offset_y = self.split_data.offset * self._scale
        scaled_w, scaled_h = self._img_size * self._scale
        w = scaled_w - offset_x
        h = scaled_h - offset_y
        if self.split_data.mode == spritesheet.SplitMode.GRID_BY_CELL_COUNT:
            # cell_h由h = row * cell_h + (row - 1) * padding_y得出
            cell_h = (h - (row - 1) * padding_y) / row
            # cell_w由h = col * cell_w + (col - 1) * padding_x得出
            cell_w = (w - (col - 1) * padding_x) / col
        elif self.split_data.mode == spritesheet.SplitMode.GRID_BY_CELL_SIZE:
            row = math.ceil((h + padding_y) / (cell_h + padding_y))
            col = math.ceil((w + padding_x) / (cell_w + padding_x))
        with dpg.draw_layer(parent=self._draw_list) as box_layer:
            for row_index in range(row):
                for col_index in range(col):
                    top_left = (
                        offset_x + col_index * (cell_w + padding_x),
                        offset_y + row_index * (cell_h + padding_y)
                    )
                    right_down = (
                        top_left[0] + cell_w,
                        top_left[1] + cell_h
                    )
                    dpg.draw_rectangle(
                        top_left,
                        right_down,
                        color=(255, 0, 0, 255),
                        thickness=1,
                    )
        self._box_layer = box_layer

    guid = property(get_guid)
    split_data = property(get_split_data)
    mode = property(get_mode, set_mode)
    image_path = property(get_image_path)
    image_size = property(get_image_size)