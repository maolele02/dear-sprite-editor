import logging
import dearpygui.dearpygui as dpg
from spritesheettool.view import user_window


# 初始化日志
logging.basicConfig(level=logging.INFO)

dpg.create_context()

# 创建窗口
user_window = user_window.UserWindow()
user_window_guid = user_window.create()
dpg.set_primary_window(user_window_guid, True)

dpg.create_viewport(title='Dear Sprite Editor', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()