import logging
import dearpygui.dearpygui as dpg
from spritesheettool.view import user_window

"""
精灵图集剪裁工具
1. 导入图片: 文件对话框导入, 控制台参数导入
2. 设置裁切数据:
    2.1 设定行列数
    2.2 设定单位格尺寸
3. 设置导出参数:
    3.1 直接导出: 导出到当前目录
    3.2 文件对话框导出
"""

# 初始化日志
logging.basicConfig(level=logging.INFO)

dpg.create_context()

# 创建窗口
user_window = user_window.UserWindow()
user_window_guid = user_window.create()
dpg.set_primary_window(user_window_guid, True)

dpg.create_viewport(title='Sprite Editor', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()