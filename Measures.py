from re import search
import asyncio
from typing import Optional

import flet as ft
from flet_core import ControlEvent
from flet_core.border_radius import vertical
from flet_core.cupertino_icons import icons_list
from lxml.html.diff import end_tag

from CONFIG import Config as cfg, Config
from MEASUREMENTS_CONFIG import NOT_NORMAL_INTERVAL_COLOR
from misc import ShowLabelsForDebug

# Константы
DEFAULT_MAX_FLOAT_DIGITS = 1
ZERO_VALUE = "0"
DEBUG_LABELS = ShowLabelsForDebug() # .set_true()


# print(DEBUG_LABELS.value)


class Page:
    actual_page = None

    @classmethod
    def set_page(cls, page):
        cls.actual_page = page


class MeasurementHeader:
    def __init__(
            self,
            title: str,
            order_num: int,
            is_visible: bool,
    ):
        self.header = title
        self.order_num = order_num
        self.is_visible = is_visible
        self.header_color = cfg["Block"]["Header_text"]["color"]
        self.header_height = cfg["Block"]["Header_text"]["height"]
        self.header_size = cfg["Block"]["Header_text"]["size"]
        self.header_weight = cfg["Block"]["Header_text"]["weight"]
        self.alignment = cfg["Block"]["Header_text"]["alignment"]
        self.width = cfg["Block"]["Header_text"]["width"]

    def get_control(self) -> ft.Text:
        # value = self.header + f" [{self.order_num}]" if self.is_visible else ""
        value = self.header if self.is_visible else ""

        return ft.Text(
            # self.header + f" [{self.order_num}]",
            value=value,
            color=self.header_color,
            size=self.header_size,
            weight=self.header_weight,
            height=self.header_height,
            text_align=self.alignment,
            width=self.width,
        )


class MeasurementLabels:
    def __init__(self, label_config: dict, config=cfg):
        self.label_name = label_config["measure_title"]
        config = config["Block"]["measure_title"]
        self.label_color = config["color"]
        self.label_width = config["width"]
        self.label_height = config["height"]
        self.label_size = config["size"]

    def get_control(self):
        return ft.Text(
            self.label_name,
            color=self.label_color,
            size=self.label_size,
            height=self.label_height,
            width=self.label_width,
            text_align=ft.TextAlign.RIGHT,
            # bgcolor="#cc3333"
        )


class ValueIntervals:

    def __init__(self, intervals: list):
        self.intervals = intervals

    class Interval:
        def __init__(self):
            ...


class GeneralField:
    class DropdownField:
        def __init__(self, control_config: dict, style_config: dict = cfg):
            self.options = control_config["options"]
            self.field_id = control_config["field_id"]
            self.label = control_config["label"]
            self.hint_text = control_config["hint_text"]
            self.width = control_config["width"]
            self.text_size = control_config["text_size"]
            self.fill_color = style_config["Block"]["measure"]["fill_color"]
            self.update_on_change = control_config.get("update_on_change", True)

            self.control = self.get_control()

        def __make_options_list(self):
            return [ft.dropdown.Option(option) for option in self.options]

        def get_control(self):
            return ft.Dropdown(
                options=self.__make_options_list(),
                label=self.field_id if DEBUG_LABELS.value else self.label,
                hint_text=self.hint_text,
                width=self.width,
                text_size=self.text_size,
                fill_color=self.fill_color,
                on_change=None if not self.update_on_change else GlobalControlsList.calculate_on_update,
            )

    class TextField:
        def __init__(self, control_config: dict, style_config: dict = cfg):
            self.label = control_config["label"]
            self.field_id = control_config["field_id"]
            self.hint_text = control_config["hint_text"]
            self.width = control_config["width"]
            self.text_size = control_config["text_size"]
            self.fill_color = style_config["Block"]["measure"]["fill_color"]
            self.update_on_change = control_config.get("update_on_change", True)

            self.control = self.get_control()

        def get_control(self):
            return ft.TextField(
                label=self.field_id if DEBUG_LABELS.value else self.label,
                hint_text=self.hint_text,
                width=self.width,
                text_size=self.text_size,
                on_change=None if not self.update_on_change else GlobalControlsList.calculate_on_update,
                fill_color=self.fill_color,
            )

    def __init__(self, field_config: dict, style_config: dict = cfg):
        self.field_id = field_config["field_id"]
        field_config["control"]["field_id"] = self.field_id
        self.title = field_config["title"]
        self.measure_title = self.title
        self.printable_title = field_config["printable_title"]
        self.type = field_config["type"]
        self.control_object = self.make_control(field_config["control"])
        self.value_intervals = None
        self.fill_color = style_config["Block"]["measure"]["fill_color"]
        self.non_numeric_field = field_config.get("non_numeric_field", False)

        self.control_link = self.get_control()

        self.needed_params = []
        self.calculable = False

        # Внесём поле в глобальный список полей ввода и расчёта
        GlobalControlsList.insert_control(self)

    def make_control(self, control_config: dict):
        if self.type == ft.Dropdown:
            return self.DropdownField(control_config)
        elif self.type == ft.TextField:
            return self.TextField(control_config)
        else:
            return None

    def get_control(self):
        return self.control_object.control


class MeasurementField:
    def __init__(self, measurement_config: dict, style_config: dict = cfg):
        self.CFG = measurement_config
        self.style_config = style_config

        # Params
        self.label = ""
        self.measure_num: int = measurement_config["measure_num"]
        self.field_id: str = measurement_config["field_id"]
        self.measure_title: str = measurement_config["measure_title"]
        self.title = self.measure_title
        self.editable: bool = measurement_config["editable"]
        self.calculable: bool = measurement_config["calculable"]
        self.enabled: bool = measurement_config["enabled"]
        self.visible: bool = measurement_config["visible"]
        self.formula = measurement_config["formula"]
        self.needed_params = measurement_config["needed_params"]
        # Интервалы значений (если есть таковые)
        self.value_intervals = measurement_config.get("value_intervals", None)
        self.non_numeric_field = measurement_config.get("non_numeric_field", False)

    def get_field(self):
        if "custom_element_type" not in self.CFG:
            return self.get_default_text_field()
        elif self.CFG["custom_element_type"] == "checkbox":
            return self.get_checkbox_element()
        elif self.CFG["custom_element_type"] == "dropdown":
            return self.get_dropdown_element()
        else:
            raise Exception(f"{self.CFG["custom_element_type"]}: тип элемента не реализован")

    def get_dropdown_element(self):
        return MeasurementField_dropDown(self.CFG, self.style_config)

    def get_default_text_field(self):
        return MeasurementField_textField(self.CFG, self.style_config)

    def get_checkbox_element(self):
        return MeasurementField_checkBox(self.CFG, self.style_config)

    def __create_control(self):
        return None

    def clear_control_value(self):
        self.control_link.value = ""

    def get_control(self):
        return self.control_link


class MeasurementField_dropDown(MeasurementField):
    def __init__(self, measurement_config: dict, style_config: dict = cfg):
        super().__init__(measurement_config, style_config)
        self.CFG = measurement_config

        # Стиль блоков измерений
        style_config = style_config["Block"]
        self.width = int(style_config["Header_text"]["width"] * 0.90)
        # self.content_padding = style_config["content_padding"]
        # self.cursor_height = style_config["cursor_height"]
        # self.fill_color = style_config["fill_color"]
        # self.text_size = style_config["text_size"]
        # self.text_align = style_config["text_align"]
        # self.border_color = style_config["calculable_border_color"] if self.calculable else style_config["border_color"]
        # self.border_width = style_config["calculable_border_width"] if self.calculable else style_config["border_width"]
        # self.height = style_config["height"]
        # self.text_color = style_config["text_color"]
        # self.filled = style_config["filled"]
        # self.calculable_fill_color = style_config["calculable_fill_color"]
        # self.focused_border_width = style_config["focused_border_width"]

        self.drop_down_options_list = self.__create_options_list()

        # ссылка на объект Control
        self.control_link = self.__create_control()

    def clear_control_value(self):
        """Обнулить значение текстового поля """
        self.control_link.value = ""

    def __create_options_list(self):
        return [ft.dropdown.Option(list(option.keys())[0]) for option in self.CFG["options"]]

    def __create_control(self):
        return ft.Dropdown(
            label=self.field_id if DEBUG_LABELS.value else self.CFG["measure_title"],
            width=self.width,
            options=[*self.drop_down_options_list],
            on_change=GlobalControlsList.calculate_on_update,
            # item_height=49,
            # max_menu_height=300,
            # text_size=15,
            # text_style=ft.TextOverflow.FADE
        )

    def get_control(self):
        return self.control_link


class MeasurementField_checkBox(MeasurementField):
    def __init__(self, measurement_config: dict, style_config: dict = cfg):
        super().__init__(measurement_config, style_config)
        self.style_config = style_config["Block"]["measure"]
        self.default_value = measurement_config["default_value"]
        # Стиль блоков измерений
        # style_config = style_config["Block"]["measure"]
        # self.width = style_config["width"]
        # self.content_padding = style_config["content_padding"]
        # self.cursor_height = style_config["cursor_height"]
        # self.fill_color = style_config["fill_color"]
        # self.text_size = style_config["text_size"]
        # self.text_align = style_config["text_align"]
        # self.border_color = style_config["calculable_border_color"] if self.calculable else style_config["border_color"]
        # self.border_width = style_config["calculable_border_width"] if self.calculable else style_config["border_width"]
        # self.height = style_config["height"]
        # self.text_color = style_config["text_color"]
        # self.filled = style_config["filled"]
        # self.calculable_fill_color = style_config["calculable_fill_color"]
        # self.focused_border_width = style_config["focused_border_width"]

        # ссылка на объект Control
        self.control_link = self.__create_control()

    def clear_control_value(self):
        """Обнулить значение текстового поля """
        self.control_link.value = False

    def __create_control(self):
        # return ft.Checkbox(
        #     label=None,
        #     value=self.default_value,
        #     height=self.style_config["height"],
        #     #on_change=GlobalControlsList.calculate_on_update,
        # )

        return ft.Switch(
            # label="Unchecked switch",
            value=self.default_value,
            height=self.style_config["height"],
            on_blur=GlobalControlsList.calculate_on_update,
            label=self.field_id if DEBUG_LABELS.value else None,
        )

    def get_control(self):
        return self.control_link


class MeasurementField_textField(MeasurementField):
    def __init__(self, measurement_config: dict, style_config: dict = cfg):
        super().__init__(measurement_config, style_config)

        # Стиль блоков измерений
        style_config = style_config["Block"]["measure"]
        self.width = style_config["width"]
        self.content_padding = style_config["content_padding"]
        self.cursor_height = style_config["cursor_height"]
        self.fill_color = style_config["fill_color"]
        self.text_size = style_config["text_size"]
        self.text_align = style_config["text_align"]
        self.border_color = style_config["calculable_border_color"] if self.calculable else style_config["border_color"]
        self.border_width = style_config["calculable_border_width"] if self.calculable else style_config["border_width"]
        self.height = style_config["height"]
        self.text_color = style_config["text_color"]
        self.filled = style_config["filled"]
        self.calculable_fill_color = style_config["calculable_fill_color"]
        self.focused_border_width = style_config["focused_border_width"]

        # ссылка на объект Control
        self.control_link = self.__create_control()

    def clear_control_value(self):
        """Обнулить значение текстового поля """
        self.control_link.value = ""

    def __create_control(self):
        return ft.TextField(
            width=self.width,
            content_padding=self.content_padding,
            cursor_height=self.cursor_height,
            fill_color=self.fill_color if not self.calculable else self.calculable_fill_color,
            text_size=self.text_size,
            text_align=self.text_align,
            border_color=self.border_color,
            border_width=self.border_width,
            height=self.height,
            read_only=not self.editable,
            # on_change=GlobalControlsList.calculate_on_update,
            on_blur=GlobalControlsList.calculate_on_update,
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9.]*$", replacement_string=""),
            color=self.text_color,
            filled=self.filled,
            focused_border_width=self.focused_border_width,
            label=self.field_id if DEBUG_LABELS.value else None,
            dense=True,

            tooltip=ft.Tooltip(
                message="",
                padding=8,
                wait_duration=1200,
                border_radius=4,
                text_style=ft.TextStyle(size=14, color="#ffffff"),
            ),

        )

    def get_control(self):
        return self.control_link


class Block:
    def __init__(self, block_config: dict, style_config: dict = cfg):
        self.title = block_config["title"]
        self.print_title = block_config["print_title"]
        self.group_num = block_config["group_num"]
        self.group_id = block_config["group_id"]
        self.visible_title = block_config["visible_title"]
        self.disabled_title = block_config["disabled_title"]  # наличие/отсутствие заголовка блока в разметке

        self.no_label_fields = []

        self.labels_controls = self.__get_label_controls(block_config["measurements"])
        self.fields, self.fields_controls = self.__get_fields(block_config["measurements"])

        # Стиль заглавия блока
        header_config = style_config["Block"]["Block_header"]
        self.header_border = header_config["border"]
        self.header_width = header_config["width"]
        self.header_padding = header_config["padding"]
        self.header_margin = header_config["margin"]
        self.header_height = header_config["height"]
        # В самом конце конструктора создадим ft.Control ...
        self.control = self.__get_block_control()

    def __get_label_controls(self, measurements: list[dict]) -> list[ft.Control]:
        labels_list = []
        for measure in measurements:
            # Отключенные поля ввода не создаём и не выводим
            if not measure["enabled"]:
                continue

            if measure.get("no_label_field", False):
                # если это элемент без лейбла
                # например dropDown
                # то его вводим в список self.no_label_fields,
                # для вывода в конце блока и без лейбла
                continue

            control = MeasurementLabels(measure).get_control()

            labels_list.append(control)

        return labels_list

    def __get_fields(self, measurements: list[dict]) -> (list[MeasurementField], list[ft.Control]):
        fields_controls_list = []
        fields_list = []

        for measure in measurements:
            # Отключенные поля не создаём и не выводим
            if not measure["enabled"]:
                continue

            field = MeasurementField(measure).get_field()
            control = field.get_control()
            fields_list.append(field)

            if measure.get("no_label_field", False):
                # если это элемент без лейбла
                # например dropDown
                # то его вводим в список self.no_label_fields,
                # для вывода в конце блока и без лейбла
                self.no_label_fields.append(control)
            else:
                fields_controls_list.append(control)

            # добавим поле в глобальный список полей ввода и расчёта
            GlobalControlsList.insert_control(field)
        return fields_list, fields_controls_list

    def get_title_control(self) -> ft.Text:
        return MeasurementHeader(self.print_title, self.group_num, self.visible_title).get_control()

    def get_labels_column(self) -> ft.Column:
        return ft.Column(
            [*self.labels_controls],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
        )

    def get_text_fields_column(self) -> ft.Column:
        return ft.Column(
            [*self.fields_controls],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
        )

    def get_inner_row(self) -> ft.Row:
        return ft.Row(
            [
                self.get_labels_column(),
                self.get_text_fields_column(),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=7,
        )

    def __get_block_control(self) -> ft.Column:
        if not self.disabled_title:
            return ft.Column(
                [
                    ft.Container(
                        border=self.header_border,
                        width=self.header_width,
                        height=self.header_height,
                        padding=self.header_padding,
                        margin=self.header_margin,
                        content=self.get_title_control(),
                    ),
                    self.get_inner_row(),
                    *self.no_label_fields,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.END,
                spacing=0,
            )
        else:
            return ft.Column(
                [
                    self.get_inner_row(),
                ],
                # horizontal_alignment=ft.CrossAxisAlignment.END,
                # spacing=0,
            )


class GlobalControlsList:
    # Хранилище ссылок на объекты MeasurementField
    measurements: list[MeasurementField] = []

    @classmethod
    def prettify_value(cls, value, config=cfg):
        """Сделать value красивым для вывода в текстовых полях программы """
        max_float_digits = config["Block"]["measure"]["max_float_digits"]
        if not max_float_digits:
            max_float_digits = DEFAULT_MAX_FLOAT_DIGITS
        else:
            max_float_digits = int(max_float_digits)

        if not value:
            return ""
        if float(value) % 1 == 0:
            # значение можно без потерь обратить в целочисленное
            return str(int(value))
        else:
            # значение имеет ненулевую дробную часть - округлим
            return str(round(value, max_float_digits))

    @classmethod
    def insert_control(cls, control):
        cls.measurements.append(control)

    @classmethod
    def calculate_on_update(cls, e):
        """ При изменении значений происходит полный перерасчёт всей таблицы"""
        event_control = cls.find_mtf_by_control(e)
        # # Обработать ввод нулевого значения (по идее нулей не должно быть)
        # if str(event_control.control_link.value) == ZERO_VALUE:
        #     event_control.clear_control_value()

        # Полный пересчёт все таблицы блоков
        print("\n\n")
        for measurement in cls.measurements:
            # Два варианта:
            if cls.has_val(event_control.field_id):
                # 1) у вызвавшего объекта event_control ЕСТЬ ЗНАЧЕНИЕ на момент вызова ф-ии on_change
                # Все параметры needed_params должны иметь значения
                all_has_values = all([cls.has_val(param) for param in measurement.needed_params])
                if not all_has_values:
                    # Какой-то из параметров (кроме инициатора) не имеет значения
                    # расчёты произвести невозможно
                    continue
                # Получим список значений по списку параметров

                values_list = [float(cls.find_mtf_by_id(param).control_link.value)
                               for param
                               in measurement.needed_params]
                # print(measurement.needed_params)
                # 3. выполнить расчёты по формулам (только для вычисляемых полей)
                if measurement.calculable:
                    measurement.control_link.value = cls.prettify_value(measurement.formula(*values_list))

                ###################### округление результата сделать
            else:
                # 2) у вызвавшего объекта event_control НЕТ ЗНАЧЕНИЕ на момент вызова ф-ии on_change
                # - требуется очистить все текстовые поля, зависящие от поля инициатора ф-ии on_change
                cls.clear_values_where_id_needed(event_control.field_id)

            # field_id найден у кого-то в списке требуемых параметров

        # обновим подсветку вхождения значений в допустимые интервалы
        cls.update_intervals_visuality()
        # ОТЛАДКА
        cls.print_all_fields_values()

        Page.actual_page.update()

    @staticmethod
    def clear_entire_form(e: ControlEvent):
        """ Очистить всю форму """

        for measure in GlobalControlsList.measurements:
            measure.control_link.value = ""
            if measure.calculable:
                measure.control_link.fill_color = Config["Block"]["measure"]["calculable_fill_color"]
            else:
                measure.control_link.fill_color = Config["Block"]["measure"]["fill_color"]

        Page.actual_page.update()

    @classmethod
    def prettify_interval_values(cls, interval_list: list[int | float]):
        '''Преобразуем к человеко читаемому виду значения
        границ интерваллов значений показателей'''

        REALLY_BIG_NUMBER = 10 ** 10
        REALLY_SMALL_NUMBER = 1 / REALLY_BIG_NUMBER
        start = interval_list[0]
        end = interval_list[1]

        if start == REALLY_SMALL_NUMBER or start == -REALLY_BIG_NUMBER:
            start_str = "менее "
        else:
            start_str = f"от {start} до "

        if end == REALLY_BIG_NUMBER:
            start_str = "более "
            end_str = start
        else:
            end_str = end

        return f"{start_str}{end_str}"


    @classmethod
    def update_intervals_visuality(cls):
        # визуализация интервалов допустимых значений
        for measurement in cls.measurements:

            if measurement.value_intervals:
                # Интервалы допустимых значений присутствуют

                if not measurement.control_link.value:
                    # Значение не введено - пропустить
                    continue

                if measurement.non_numeric_field:
                    # Поле не числовое - пропустить
                    continue

                value = float(measurement.control_link.value)
                value_intervals = measurement.value_intervals["intervals"]
                # выбранный пол (None, Мужской, Женский)
                gender = cls.find_mtf_by_id("gender").control_link.value

                # Установить цвет поля в "НЕ НОРМА". Если значение поля не
                # войдёт ни в какой диапазон - значит ЭТО НЕ НОРМА
                # Если значение поля войдёт в какой-то диапазон - значит ЭТО НОРМА
                measurement.control_link.fill_color = NOT_NORMAL_INTERVAL_COLOR
                Page.actual_page.update()

                all_intervals = ""
                for i, interval in enumerate(value_intervals):
                    all_intervals += f"{i + 1}) {interval['description']} [{cls.prettify_interval_values(interval['values_belongs'])}] {'не зависит от пола' if not interval["gender"] else interval["gender"]}\n"

                for interval in value_intervals:
                    if interval["gender"] is None:
                        # пол не важен
                        if interval["values_belongs"][0] <= value <= interval["values_belongs"][1]:
                            measurement.control_link.fill_color = interval["color"]

                            # всплывающая подсказка
                            measurement.control_link.tooltip.message = (f"{measurement.measure_title}\n"
                                                                        f"значение: {measurement.control_link.value}\n"
                                                                        f"интервал: {interval["description"]}\n"
                                                                        f"значения интервала: {cls.prettify_interval_values(interval['values_belongs'])}\n"
                                                                        f"пол определяет интервал: {'да' if interval['gender'] else 'нет'}\n\n"
                                                                        f"все интервалы:\n"
                                                                        f"{all_intervals}")

                            Page.actual_page.update()
                            break
                    elif interval["gender"] is not None:
                        # пол важен
                        if (interval["gender"] == gender and
                                interval["values_belongs"][0] <= value <= interval["values_belongs"][1]):
                            measurement.control_link.fill_color = interval["color"]

                            # всплывающая подсказка
                            measurement.control_link.tooltip.message = (f"{measurement.measure_title}\n"
                                                                        f"значение: {measurement.control_link.value}\n"
                                                                        f"интервал: {interval["description"]}\n"
                                                                        f"значения интервала: {cls.prettify_interval_values(interval['values_belongs'])}\n"
                                                                        f"пол определяет интервал: {'да' if interval['gender'] else 'нет'}\n\n"
                                                                        f"все интервалы:\n"
                                                                        f"{all_intervals}")

                            Page.actual_page.update()
                            break
                Page.actual_page.update()

    @classmethod
    def print_all_fields_values(cls):
        """ Вывести все значения полей """
        for field in cls.measurements:
            print(f"{field.field_id}: значение - {field.control_link.value}")

    @classmethod
    def get_needed_params_by_id(cls, measure_id: str) -> list[str]:
        """Найти список требуемых параметров для рассчитываемого поля """
        return cls.find_mtf_by_id(measure_id).needed_params

    @classmethod
    def is_param_calculable(cls, measure_id: str) -> bool:
        """Является ли поле по искомому field_id вычисляемым """
        search_obj = cls.find_mtf_by_id(measure_id)
        if (search_obj.calculable or
                len(search_obj.needed_params) > 0):
            return True
        return False

    @classmethod
    def set_control_fill_color(cls):
        ...

    @classmethod
    def get_control_default_fill_color(cls, field_id):
        """ Определить цвет заливки по умолчанию """
        field = cls.find_mtf_by_id(field_id)
        if field.calculable:
            return cfg["Block"]["measure"]["calculable_fill_color"]
        else:
            return cfg["Block"]["measure"]["fill_color"]

    @classmethod
    def clear_values_where_id_needed(cls, field_id: str):
        """Очистит рекурсивно """
        field = cls.find_mtf_by_id(field_id)
        field.control_link.fill_color = cls.get_control_default_fill_color(field.field_id)

        for measure in cls.measurements:
            # print(f"{field_id}  = iter - ")
            # print(measure.needed_params)
            if field_id in measure.needed_params:
                measure.control_link.value = ""
                measure.control_link.fill_color = cls.get_control_default_fill_color(field_id)
                cls.clear_values_where_id_needed(measure.field_id)
        Page.actual_page.update()

    @classmethod
    def val(cls, field_id: str) -> str:
        # получить значение для field_id
        val = cls.find_mtf_by_id(field_id).get_control().value
        return val if val else None

    @classmethod
    def description(cls, field_id: str) -> str:
        # получить описание: типа "Объем, мл"
        descr = cls.find_mtf_by_id(field_id).measure_title
        return descr if descr else None

    @classmethod
    def gender(cls):
        # получить пол пациента "мужской" "женский" None
        obj = cls.val("gender")
        return obj if obj.lower() in ["мужской", "женский"] else None

    @classmethod
    def get_intervals_if_exist(cls, field_id: str) -> Optional[dict]:
        # получить блоки диапазона значений если есть
        obj = cls.find_mtf_by_id(field_id)
        intervals = obj.value_intervals
        if not intervals:
            return None
        else:
            return intervals["intervals"]

    @classmethod
    def interval(cls, field_id: str) -> Optional[dict]:
        # получить блок диапазона значений если есть

        def is_in_interval(val: float, interv: list) -> bool:
            # Входит ли значение в интрвал типа [начало, конец]
            if interv[0] <= val <= interv[1]:
                return True
            else:
                return False

        obj = cls.find_mtf_by_id(field_id)
        obj_val = cls.val(field_id)

        # выполним приведение к числовому типу
        try:
            obj_val_saved = obj_val

            if not obj.non_numeric_field:
                obj_val = float(obj_val)

        except Exception as e:
            print(f"Невозможно преобразовать {obj_val} к типу float, {e}\n{obj_val_saved} {obj.field_id}\n")

        match_interval = None

        if obj.value_intervals:
            # интервалы значений определены
            value_intervals = obj.value_intervals["intervals"]

            for interval in value_intervals:
                if interval["gender"]:
                    # Пол для интервала определён
                    if is_in_interval(obj_val, interval["values_belongs"]) and cls.gender() == interval["gender"]:
                        match_interval = interval
                        break
                else:
                    # Пол для интервала НЕ ОПРЕДЕЛЁН
                    if is_in_interval(obj_val, interval["values_belongs"]):
                        match_interval = interval
                        break
            else:
                match_interval = None  # значение поля не попало ни в один из диапазонов - значит результат None

        return match_interval

    @classmethod
    def find_mtf_by_id(cls, control_id: str) -> MeasurementField:
        """ Найти объект исследования (тип: MeasurementField) по комбинированному ID
        Параметр: control_id: str (Комбинированный ID. Пример: "m_1_1")

        Вернуть: объект MeasurementField
        """
        for measurement in cls.measurements:
            if measurement.field_id == control_id:
                return measurement

    @classmethod
    def has_val(cls, measure_id: str) -> bool:
        """ Определить: имеет ли значение объект MeasurementField
        в своём вложенном объекте ft.Control
        Параметр: field_id: str (Комбинированный ID. Пример: "m_1_1")

        Вернуть: bool
        """
        control_value = cls.find_mtf_by_id(measure_id).control_link.value
        if control_value == '':
            return False
        if control_value == 0:
            return False

        return True

    @classmethod
    def find_mtf_by_control(cls, e: ControlEvent) -> MeasurementField:
        """ Найти объект исследования (тип: MeasurementField) по вызывающему ft.Control объекту
        Параметр: e: ControlEvent (Объект flet события)

        Вернуть: объект MeasurementField
        """
        for measurement in cls.measurements:
            if e.control is measurement.control_link:
                print(measurement.field_id)
                return measurement
