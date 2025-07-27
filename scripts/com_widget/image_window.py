from core.math import *
import dearpygui.dearpygui as dpg

def create(parent):
    pass

class ImageWindow(object):
    def __init__(self, img, parent):
        self._win = dpg.add_child_window(parent=parent)
        self._img_path = img
        self._img_size = Vector2()
        self._texture = 0
        self._draw_list = 0
        self._bg_layer = 0
        self._load_img(img)

    def _load_img(self, img_path):
        w, h, channels, data = dpg.load_image(img_path)
        self._img_size.x = w
        self._img_size.y = h
        with dpg.texture_registry(show=False):
            self._texture = dpg.add_static_texture(w, h, data)

    def _create_draw_list(self):
        with dpg.drawlist(parent=self._win) as draw_list:
            self._bg_layer = self._create_bg_layer()
            self._draw_list = draw_list

    def set_image(self, image):
        self._img_path = image


    def _create_bg_layer(self, parent):
        with dpg.add_draw_layer(parent=parent) as layer:
            pass
        return layer

