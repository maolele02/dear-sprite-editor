import os
import math
import logging
import sys

import dearpygui.dearpygui as dpg
from spritesheettool import spritesheet
from spritesheettool import com_func
from com_widget.image_window import *

MODE_AUTOMATIC = 'Automatic'
MODE_GRID_BY_CELL_COUNT = 'Grid By Cell Count'
MODE_GRID_BY_CELL_SIZE = 'Grid By Cell Size'

class UserWindow(object):

    MODES = (
        MODE_GRID_BY_CELL_SIZE,
        MODE_GRID_BY_CELL_COUNT,
        MODE_AUTOMATIC,
    )

    MODE_2_OP_TITLES = {
        spritesheet.SplitMode.AUTOMATIC: (),
        spritesheet.SplitMode.GRID_BY_CELL_COUNT: (
            'Column & Row',
            'Offset',
            'Padding'
        ),
        spritesheet.SplitMode.GRID_BY_CELL_SIZE: (
            'Pixel Size',
            'Offset',
            'Padding',
        )
    }

    OP_INPUT_BOX_WIDTH = 120

    def __init__(self):
        # region 控件guid
        self._win = dpg.add_window(label='SpriteSheetSpliter', autosize=True)
        self._file_dlg = 0
        self._img_win = 0
        self._op_root_group = 0
        self._auto_operate_group = 0
        self._grid_by_cell_size_group = 0
        self._grid_by_cell_count_group = 0
        self._no_import_alert = 0
        self._export_menu = 0
        # endregion
        # region ui数据
        self._mode_2_group = {}
        self._default_mode = spritesheet.SplitMode.GRID_BY_CELL_SIZE
        self._img_win_obj: ImageWindow = ImageWindow(self._win)
        # endregion

    def create(self):
        self._create_widgets()
        self._init()
        return self._win

    def destroy(self):
        dpg.delete_item(self._file_dlg)

    def _get_mode_desc(self, mode) -> str:
        if mode == spritesheet.SplitMode.GRID_BY_CELL_COUNT:
            return MODE_GRID_BY_CELL_COUNT
        if mode == spritesheet.SplitMode.GRID_BY_CELL_SIZE:
            return MODE_GRID_BY_CELL_SIZE
        if mode == spritesheet.SplitMode.AUTOMATIC:
            return MODE_AUTOMATIC
        logging.error(f'error mode: {mode}')
        return ''

    def _create_widgets(self):
        self._create_menu()
        self._create_img_operates()
        self._create_img_child_window()
        self._create_file_dlg()
        self._create_alerts()

    def _init(self):
        self._switch_mode(self._default_mode)

    def _create_menu(self):
        with dpg.menu_bar(parent=self._win):
            with dpg.menu(label='File'):
                dpg.add_menu_item(label='Open', callback=self._on_open_file)
                with dpg.menu(label='Export') as export_menu:
                    dpg.add_menu_item(
                        label='Export As Images',
                        user_data='images',
                        callback=self._on_export
                    )
                    dpg.add_menu_item(
                        label='Export As Json',
                        user_data='json',
                        callback=self._on_export
                    )
                self._export_menu = export_menu
            dpg.add_menu_item(label='Help', callback=self._on_help)

    def _create_file_dlg(self):
        with dpg.file_dialog(
                directory_selector=False,
                show=False,
                file_count=1,
                callback=self._on_add_file,
                width=700, height=400
        ) as file_dlg:
            self._file_dlg = file_dlg
            dpg.add_file_extension(".png", color=(255, 255, 0, 255))
            dpg.add_file_extension(".jpg", color=(255, 0, 255, 255))
            dpg.add_file_extension(".bmp", color=(0, 255, 0, 255))
            dpg.add_file_extension(".*")

    def _create_img_operates(self):
        with dpg.group(horizontal=False, parent=self._win, show=False) as op_group:
            # 图片缩放滑动条
            dpg.add_slider_float(
                min_value=0.5,
                max_value=5.0,
                default_value=1.0,
                callback=self._on_scale_img,
                label='scale'
            )
            # 框选模式下拉框
            dpg.add_combo(
                self.MODES,
                default_value=self._get_mode_desc(self._default_mode),
                label='Mode',
                callback=self._on_switch_mode
            )

            for mode, titles in self.MODE_2_OP_TITLES.items():
                ret_group = self._create_op_group(mode, titles)
                self._mode_2_group[mode] = ret_group
            self._op_root_group = op_group
            dpg.add_button(label='slice', callback=self._on_slice)

    def _create_op_group(self, mode, titles):
        with dpg.group(horizontal=False) as ret_group:
            with dpg.table(header_row=False):
                for _ in titles:
                    dpg.add_table_column()
                for title in titles:
                    with dpg.table_row():
                        with dpg.table_cell():
                            dpg.add_text(default_value=title)
                        with dpg.table_cell():
                            self._create_op_widgets(mode, title)
        return ret_group

    def _create_op_widgets(self, mode, title):
        group = dpg.add_group(horizontal=True)
        if title == 'Offset':  # 通用操作项group
            dpg.add_input_int(
                label='X',
                callback=self._on_input_offset_x,
                width=self.OP_INPUT_BOX_WIDTH,
                parent=group
            )
            dpg.add_input_int(
                label='Y',
                callback=self._on_input_offset_y,
                width=self.OP_INPUT_BOX_WIDTH,
                parent=group
            )
        elif title == 'Padding':
            dpg.add_input_int(
                label='X',
                callback=self._on_input_padding_x,
                width=self.OP_INPUT_BOX_WIDTH,
                parent=group,
            )
            dpg.add_input_int(
                label='Y',
                callback=self._on_input_padding_y,
                width=self.OP_INPUT_BOX_WIDTH,
                 parent = group,
            )
        else:
            if mode == spritesheet.SplitMode.GRID_BY_CELL_COUNT:
                if title == 'Column & Row':
                    dpg.add_input_int(
                        label='C',
                        min_value=1,
                        default_value=self._img_win_obj.split_data.rc.y,
                        callback=self._on_input_cell_col,
                        width=self.OP_INPUT_BOX_WIDTH,
                        parent=group,
                    )
                    dpg.add_input_int(
                        label='R',
                        min_value=1,
                        default_value=self._img_win_obj.split_data.rc.x,
                        callback=self._on_input_cell_row,
                        width=self.OP_INPUT_BOX_WIDTH,
                        parent=group,
                    )
            elif mode == spritesheet.SplitMode.GRID_BY_CELL_SIZE:
                if title == 'Pixel Size':
                    dpg.add_input_int(
                        label='X',
                        callback=self._on_input_cell_w,
                        default_value=self._img_win_obj.split_data.sprite_size.x,
                        width=self.OP_INPUT_BOX_WIDTH,
                        parent=group,
                    )
                    dpg.add_input_int(
                        label='Y',
                        callback=self._on_input_cell_h,
                        default_value=self._img_win_obj.split_data.sprite_size.y,
                        width=self.OP_INPUT_BOX_WIDTH,
                        parent=group,
                    )

    def _create_img_child_window(self):
        self._img_win_obj.create()

    def _create_alerts(self):
        with dpg.window(label='export error', modal=True, show=False, no_title_bar=True) as no_import_alert:
            dpg.add_text("not exist imported image")
            dpg.add_separator()
            dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item(no_import_alert, show=False))
        self._no_import_alert = no_import_alert

    # region 菜单操作相关

    def _on_open_file(self):
        dpg.show_item(self._file_dlg)

    def _on_add_file(self, sender, app_data):
        selections = app_data['selections']
        if not selections:
            logging.info('no file')
            return
        file_path = list(selections.values())[0]
        if not os.path.exists(file_path):
            logging.warning(f'path not exists: {file_path}')
            return
        self._img_path = file_path
        self._img_win_obj.set_image(self._img_path)
        self._img_win_obj.refresh()
        dpg.show_item(self._op_root_group)
        dpg.show_item(self._img_win_obj.guid)

    def _on_export(self, sender, app_data, file_type):
        if not self._img_win_obj.image_path:
            dpg.show_item(self._no_import_alert)
        parent_dir = os.path.join(sys.argv[0], '..', '..', 'output')
        img_w, img_h = self._img_win_obj.image_size
        split_data = self._img_win_obj.split_data
        sp = com_func.get_sprite_sheet_by_split_data(
            self._img_win_obj.image_path,
            img_w, img_h,
            split_data
        )
        if file_type == 'images':
            sp.save(parent_dir)
        elif file_type == 'json':
            path = os.path.join(parent_dir, 'output.json')
            sp.save(path)


    def _on_help(self):
        import webbrowser
        webbrowser.open('https://space.bilibili.com/353269387', new=1)
    # endregion

    def _on_scale_img(self, sender, scale):
        self._img_win_obj.set_scale(scale)

    def _on_switch_mode(self, sender, mode_name):
        mode = 0
        if mode_name == MODE_GRID_BY_CELL_SIZE:
            mode = spritesheet.SplitMode.GRID_BY_CELL_SIZE
        elif mode_name == MODE_GRID_BY_CELL_COUNT:
            mode = spritesheet.SplitMode.GRID_BY_CELL_COUNT
        if mode > 0:
            self._switch_mode(mode)

    def _on_slice(self, sender):
        pass

    def _switch_mode(self, mode):
        if self._img_win_obj.mode == mode:
            return
        self._img_win_obj.mode = mode
        self._img_win_obj.refresh()
        for cur_mode in [
            spritesheet.SplitMode.GRID_BY_CELL_COUNT,
            spritesheet.SplitMode.GRID_BY_CELL_SIZE,
            spritesheet.SplitMode.AUTOMATIC,
        ]:
            group = self._mode_2_group.get(cur_mode, 0)
            if group == 0:
                continue
            if mode == cur_mode:
                dpg.show_item(group)
            else:
                dpg.hide_item(group)

    def _on_input_offset_x(self, sender, offset_x):
        self._img_win_obj.split_data.offset.x = offset_x
        self._img_win_obj.refresh()

    def _on_input_offset_y(self, sender, offset_y):
        self._img_win_obj.split_data.offset.y = offset_y
        self._img_win_obj.refresh()

    def _on_input_padding_x(self, sender, padding_x):
        self._img_win_obj.split_data.padding.x = padding_x
        self._img_win_obj.refresh()

    def _on_input_padding_y(self, sender, padding_y):
        self._img_win_obj.split_data.padding.y = padding_y
        self._img_win_obj.refresh()

    def _on_input_cell_row(self, sender, row_count):
        self._img_win_obj.split_data.rc.x = row_count
        self._img_win_obj.refresh()

    def _on_input_cell_col(self, sender, col_count):
        self._img_win_obj.split_data.rc.y = col_count
        self._img_win_obj.refresh()

    def _on_input_cell_w(self, sender, cell_w):
        self._img_win_obj.split_data.sprite_size.x = cell_w
        self._img_win_obj.refresh()

    def _on_input_cell_h(self, sender, cell_h):
        self._img_win_obj.split_data.sprite_size.y = cell_h
        self._img_win_obj.refresh()
