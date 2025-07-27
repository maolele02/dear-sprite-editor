import os
import math
import logging
import dearpygui.dearpygui as dpg

class UserWindow(object):
    MODE_AUTOMATIC = 'Automatic'
    MODE_GRID_BY_CELL_COUNT = 'Grid By Cell Count'
    MODE_GRID_BY_CELL_SIZE = 'Grid By Cell Size'

    MODES = (
        MODE_GRID_BY_CELL_COUNT,
        MODE_GRID_BY_CELL_SIZE,
        MODE_AUTOMATIC,
    )

    MODE_2_OP_TITLES = {
        MODE_AUTOMATIC: (),
        MODE_GRID_BY_CELL_COUNT: (
            'Column & Row',
            'Offset',
            'Padding'
        ),
        MODE_GRID_BY_CELL_SIZE: (
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
        self._tex = 0
        self._img_win = 0
        self._op_root_group = 0
        self._auto_operate_group = 0
        self._grid_by_cell_size_group = 0
        self._grid_by_cell_count_group = 0
        self._img_draw_list = 0
        self._grid_line_layer = 0
        self._no_import_alert = 0
        self._export_menu = 0
        # endregion
        # region ui数据
        self._img_w = 0
        self._img_h = 0
        self._img_scale = 1.0
        self._default_mode = self.MODE_GRID_BY_CELL_SIZE
        self._mode = self._default_mode
        self._mode_2_group = {}
        self._row = 1
        self._col = 1
        self._cell_w = 16
        self._cell_h = 16
        self._offset_x = 0
        self._offset_y = 0
        self._padding_x = 0
        self._padding_y = 0
        # endregion

    def create(self):
        self._create_widgets()
        self._init()
        return self._win

    def destroy(self):
        dpg.delete_item(self._file_dlg)

    def _create_widgets(self):
        self._create_menu()
        self._create_file_dlg()
        self._create_img_operates()
        self._create_img_child_window()
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
                        label='Export As XML',
                        user_data='xml',
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
                default_value=self._default_mode,
                label='Mode',
                callback=self._on_switch_mode
            )

            for mode, titles in self.MODE_2_OP_TITLES.items():
                ret_group = self._create_op_group(mode, titles)
                self._mode_2_group[mode] = ret_group
            self._op_root_group = op_group

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
            if mode == self.MODE_GRID_BY_CELL_COUNT:
                if title == 'Column & Row':
                    dpg.add_input_int(
                        label='C',
                        min_value=1,
                        default_value=self._col,
                        callback=self._on_input_cell_col,
                        width=self.OP_INPUT_BOX_WIDTH,
                        parent=group,
                    )
                    dpg.add_input_int(
                        label='R',
                        min_value=1,
                        default_value=self._row,
                        callback=self._on_input_cell_row,
                        width=self.OP_INPUT_BOX_WIDTH,
                        parent=group,
                    )
            if mode == self.MODE_GRID_BY_CELL_SIZE:
                if title == 'Pixel Size':
                    dpg.add_input_int(
                        label='X',
                        callback=self._on_input_cell_w,
                        default_value=self._cell_w,
                        width=self.OP_INPUT_BOX_WIDTH,
                        parent=group,
                    )
                    dpg.add_input_int(
                        label='Y',
                        callback=self._on_input_cell_h,
                        default_value=self._cell_h,
                        width=self.OP_INPUT_BOX_WIDTH,
                        parent=group,
                    )

    def _create_img_child_window(self):
        self._img_win = dpg.add_child_window(parent=self._win, show=False, horizontal_scrollbar=True)

    def _create_alerts(self):
        with dpg.window(label='export error', modal=True, show=False, no_title_bar=True) as no_import_alert:
            dpg.add_text("not exist imported image")
            dpg.add_separator()
            dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item(no_import_alert, show=False))
        self._no_import_alert = no_import_alert

    def _rebuild_img_draw_list_layers(self):
        if self._img_draw_list > 0:
            dpg.delete_item(self._img_draw_list)
            self._img_draw_list = 0
            self._grid_line_layer = 0
        w = self._img_w * self._img_scale
        h = self._img_h * self._img_scale
        with dpg.drawlist(width=w + 10, height=h + 10, parent=self._img_win) as draw_list:
            with dpg.draw_layer():
                dpg.draw_image(self._tex, (0, 0), (w, h), uv_min=(0, 0), uv_max=(1, 1))
        self._img_draw_list = draw_list
        self._rebuild_draw_layers()

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
        self._img_w, self._img_h, channels, data = dpg.load_image(file_path)
        with dpg.texture_registry(show=False):
            self._tex = dpg.add_static_texture(self._img_w, self._img_h, data)
        dpg.show_item(self._op_root_group)
        dpg.show_item(self._img_win)
        if self._img_draw_list > 0:
            dpg.delete_item(self._img_draw_list)
        self._rebuild_img_draw_list_layers()
        self._rebuild_draw_layers()

    def _on_export(self, sender, app_data, file_type):
        if self._img_draw_list == 0:
            dpg.show_item(self._no_import_alert)
        if file_type == 'images':
            pass
        elif file_type == 'xml':
            pass

    def _on_help(self):
        import webbrowser
        webbrowser.open('https://space.bilibili.com/353269387', new=1)
    # endregion

    def _on_scale_img(self, sender, scale):
        self._img_scale = scale
        self._rebuild_img_draw_list_layers()

    def _on_switch_mode(self, sender, selected_item):
        self._switch_mode(selected_item)

    def _switch_mode(self, mode):
        self._mode = mode
        for mode in self.MODES:
            group = self._mode_2_group.get(mode, 0)
            if group == 0:
                continue
            if mode == self._mode:
                dpg.show_item(group)
            else:
                dpg.hide_item(group)
        self._rebuild_draw_layers()

    def _on_input_offset_x(self, sender, offset_x):
        self._offset_x = offset_x
        self._rebuild_draw_layers()

    def _on_input_offset_y(self, sender, offset_y):
        self._offset_y = offset_y
        self._rebuild_draw_layers()

    def _on_input_padding_x(self, sender, padding_x):
        self._padding_x = padding_x
        self._rebuild_draw_layers()

    def _on_input_padding_y(self, sender, padding_y):
        self._padding_y = padding_y
        self._rebuild_draw_layers()

    def _on_input_cell_row(self, sender, row_count):
        self._row = row_count
        self._rebuild_draw_layers()

    def _on_input_cell_col(self, sender, col_count):
        self._col = col_count
        self._rebuild_draw_layers()

    def _on_input_cell_w(self, sender, cell_w):
        self._cell_w = cell_w
        self._rebuild_draw_layers()

    def _on_input_cell_h(self, sender, cell_h):
        self._cell_h = cell_h
        self._rebuild_draw_layers()

    def _rebuild_draw_layers(self):
        if self._img_draw_list == 0:
            return
        if self._grid_line_layer > 0:
            dpg.delete_item(self._grid_line_layer)
        row, col = 0, 0
        cell_w, cell_h = 0, 0
        img_w = self._img_w * self._img_scale
        img_h = self._img_h * self._img_scale
        padding_x = self._padding_x * self._img_scale
        padding_y = self._padding_y * self._img_scale
        offset_x = self._offset_x * self._img_scale
        offset_y = self._offset_y * self._img_scale
        w = img_w - 2 * padding_x
        h = img_h - 2 * padding_y
        if self._mode == self.MODE_GRID_BY_CELL_COUNT:
            row = self._row
            col = self._col
            # cell_h由h = row * cell_h + (row - 1) * offset_y得出
            cell_h = (h - (row - 1) * offset_y) / row
            # cell_w由h = col * cell_w + (col - 1) * offset_x得出
            cell_w = (w - (col - 1) * offset_x) / col
        elif self._mode == self.MODE_GRID_BY_CELL_SIZE:
            cell_w = self._cell_w * self._img_scale
            cell_h = self._cell_h * self._img_scale
            row = math.ceil((h + offset_y) / (cell_h + offset_y))
            col = math.ceil((w + offset_x) / (cell_w + offset_x))
        enable_offset_y = offset_y > 0 and row > 1
        enable_offset_x = offset_x > 0 and col > 1
        if enable_offset_x:
            col_line_count = col * 2
        else:
            col_line_count = col + 1
        if enable_offset_y:
            row_line_count = row * 2
        else:
            row_line_count = row + 1
        with dpg.draw_layer(parent=self._img_draw_list) as draw_layer:
            begin_x = padding_x
            for index in range(row_line_count):  # 横线
                if enable_offset_y:
                    cell_no = int(index / 2) + 1  # 当前要绘制的是第几个格子的线段
                    is_lower_line = index % 2 == 1  # 当前绘制的是否是格子的下部分的线段
                    offset_count = cell_no - 1
                    above_sum_cell_height = (cell_no - 1) * cell_h
                    above_sum_offset = offset_count * offset_y
                    y = padding_y + above_sum_cell_height + above_sum_offset + int(is_lower_line) * cell_h
                else:
                    y = padding_y + index * cell_h
                dpg.draw_line(
                    (begin_x, y),
                    (begin_x + w, y),
                    color=(255, 0, 0, 255),
                    thickness=1,
                )
            begin_y = padding_y
            for index in range(col_line_count):  # 竖线
                if enable_offset_x:
                    cell_no = int(index / 2) + 1  # 当前要绘制的是第几个格子的线段
                    is_right_line = index % 2 == 1  # 当前绘制的是否是格子的右部分的线段
                    offset_count = cell_no - 1
                    left_sum_cell_width = (cell_no - 1) * cell_w
                    left_sum_offset = offset_count * offset_x
                    x = padding_x + left_sum_cell_width + left_sum_offset + int(is_right_line) * cell_w
                else:
                    x = padding_x + index * cell_w
                dpg.draw_line(
                    (x, begin_y),
                    (x, begin_y + h),
                    color=(255, 0, 0, 255),
                    thickness=1,
                )
        self._grid_line_layer = draw_layer
