import os
import misc
import config
import logging
import dearpygui.dearpygui as dpg
from spritesheettool.view import user_window


# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='run.log',
    filemode='w'
)

config.load(misc.get_root_dir() / 'config.toml')

dpg.create_context()

# 创建窗口
user_window = user_window.UserWindow()
user_window_guid = user_window.create()
dpg.set_primary_window(user_window_guid, True)

icon_path = (misc.get_root_dir() / 'icon.png').as_posix()

dpg.create_viewport(
    title='Dear Sprite Editor',
    width=800, height=600,
    small_icon=icon_path, large_icon=icon_path
)
dpg.setup_dearpygui()
dpg.show_viewport()
logging.info('start run dpg loop')
dpg.start_dearpygui()
dpg.destroy_context()
logging.info('dpg destroy')