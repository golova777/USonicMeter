import os
from dataclasses import field
from pprint import pprint
from re import search
import asyncio
import flet as ft
from flet_core import ControlEvent
from docxtpl import DocxTemplate

from Measures import GlobalControlsList
import datetime
import base64
import io

from prepare_report_template.gen_str_data import SAVE_FILE_PY
from template_docx import TEMPLATE_BASE64_STRING
from misc import IntervalType

SAVE_REPORT_BUTTON_LABEL = "Сохранить заключение в файл"
DEFAULT_REPORT_TEXT = "Отчёт не сформирован!"
DEFAULT_REPORT_SAVE_FILENAME = "report.docx"
REPORT_DIALOG_TITLE = "Сохранить заключение"
TEMPLATE_FILE_HOLDER = SAVE_FILE_PY


class Field:
    def __init__(self, field_id: str):
        Global = GlobalControlsList
        self.glb = Global
        self.field_id = field_id
        self.description = Global.description(field_id)  # текстовое описание поля
        self.val = self.make_float_if_possible(Global.val(field_id))  # если None - значение не введено
        self.empty = True if self.val == "" or self.val == None else False
        # self.gender = Global.gender() if self.val else None
        self.interval = Global.interval(field_id) if self.val else None
        self.interval_type = self.interval["type"] if self.interval else None
        self.error = True if self.interval_type == IntervalType.ERROR else False
        self.interval_desc = self.interval["description"] if self.interval else None
        self.interval_gender = self.interval["gender"] if self.interval else None
        self.all_intervals = Global.get_intervals_if_exist(self.field_id)
        self.is_normal = None
        self.lower_than_normal = None
        self.upper_than_normal = None
        self.set_lower_upper_normal()

    def make_float_if_possible(self, val):
        if val == 'True':
            return 'Да'

        if val == 'False':
            return 'Нет'

        if val == 'None':
            return '---'

        try:
            val = float(val)
        finally:
            return val

    def set_lower_upper_normal(self):
        if not (type(self.val) is float or type(self.val) is int):
            # пропустим все НЕЧИСЛОВЫЕ значения
            self.is_normal = None
            self.lower_than_normal = None
            self.upper_than_normal = None
            return

        gender = self.glb.gender()
        gender = gender if gender else None

        if self.interval_gender:
            # пол определён - рассматриваем только диапазоны с указанием на пол
            if self.all_intervals:
                # диапазоны какие-то есть
                for interval in self.all_intervals:
                    if interval["gender"] == gender and interval["type"] == IntervalType.NORMAL:
                        if interval["values_belongs"][0] <= self.val <= interval["values_belongs"][1]:
                            # значение входит в диапазон НОРМЫ
                            self.is_normal = True
                            self.lower_than_normal = False
                            self.upper_than_normal = False
                            return
                        if self.val < interval["values_belongs"][0]:
                            # значение меньше диапазона НОРМЫ
                            self.is_normal = False
                            self.lower_than_normal = True
                            self.upper_than_normal = False
                            return
                        if self.val > interval["values_belongs"][1]:
                            # значение больше диапазона НОРМЫ
                            self.is_normal = False
                            self.lower_than_normal = False
                            self.upper_than_normal = True
                            return

            else:
                # диапазоны отсутствуют
                self.is_normal = None
                self.lower_than_normal = None
                self.upper_than_normal = None

        else:
            # пол не определён - рассмотрим все диапазоны без пола
            if self.all_intervals:
                # диапазоны какие-то есть
                for interval in self.all_intervals:
                    if interval["type"] == IntervalType.NORMAL:
                        if interval["values_belongs"][0] <= self.val <= interval["values_belongs"][1]:
                            # значение входит в диапазон НОРМЫ
                            self.is_normal = True
                            self.lower_than_normal = False
                            self.upper_than_normal = False
                            return
                        if self.val < interval["values_belongs"][0]:
                            # значение меньше диапазона НОРМЫ
                            self.is_normal = False
                            self.lower_than_normal = True
                            self.upper_than_normal = False
                            return
                        if self.val > interval["values_belongs"][1]:
                            # значение больше диапазона НОРМЫ
                            self.is_normal = False
                            self.lower_than_normal = False
                            self.upper_than_normal = True
                            return
            else:
                # диапазоны отсутствуют
                self.is_normal = None
                self.lower_than_normal = None
                self.upper_than_normal = None
                return

    def __repr__(self):
        field_as_str = ""
        field_as_str += f"=========Объект: {self.__class__.__name__} для field_id=\"{self.field_id}\"\n"
        field_as_str += f"Измерение: \"{self.description}\",  Тип: {self.__class__.__name__}\n"
        field_as_str += f"Поля:\n"
        field_as_str += "\n".join([f"{key}: {value}" for key, value in self.__dict__.items()])
        field_as_str += "\n================================\n\n"
        return field_as_str


class Report:
    def __init__(self, page: ft.Page, global_controls_list: GlobalControlsList):
        self.page = page
        self.global_controls_list = global_controls_list

        self.report_button_control = self.__make_report_button_control()
        self.report_text_area_control = self.__get_report_textarea_control()
        self.file_picker = self.__get_file_picker()
        self.page.overlay.append(self.file_picker)

        self.save_report_button = None
        self.report_file_name = None
        self.report_date_time = None

    def copy_report_data_to_report_textarea(self, e: ControlEvent):
        #######################################################################
        # подготовка отчёта

        self.report_text_area_control.value = self.__get_report_text()
        self.page.update()

    def __get_file_picker(self):
        return ft.FilePicker(on_result=self.__save_file)

    def regenerate_report_file_name(self):
        self.report_file_name = self.__generate_report_file_name(self.global_controls_list)

    def __generate_report_file_name(self, global_controls_list: GlobalControlsList):
        # формирование имени файла заключения
        patient_name = global_controls_list.val("PatientFirstLastName")
        if patient_name:
            patient_name = "_".join([substr.capitalize() for substr in patient_name.split()])
        else:
            patient_name = "без_ФИО"

        self.report_date_time = datetime.datetime.now()
        report_date_time = self.report_date_time.strftime("%Y-%m-%d__%H-%M-%S")

        birth_year = global_controls_list.val("birth_year")
        if birth_year:
            birth_year = str(birth_year)
        else:
            birth_year = "отсутствует"

        return f"Заключение_от_{report_date_time}_{patient_name}_год_рождения_{birth_year}.docx"

    def get_create_report_button(self):
        # получить активную кнопку сохранения отчёта
        self.save_report_button = self.__get_save_report_button_control(self.file_picker, self.global_controls_list)
        return self.save_report_button

    def __get_save_report_button_control(self, file_picker, global_controls_list: GlobalControlsList):
        # Здесь лябмда выполнить две функции [callable(), callable()]
        # первая обновит значение имени сохраняемого файла, поскольку данные для его формирования
        # появляются позже создания кнопки сохранения отчёта

        return ft.ElevatedButton(SAVE_REPORT_BUTTON_LABEL,
                                 on_click=lambda _: [self.regenerate_report_file_name(),
                                                     file_picker.save_file(
                                                         file_name=self.report_file_name,
                                                         dialog_title=REPORT_DIALOG_TITLE,
                                                         initial_directory=os.getcwd(),
                                                         file_type=ft.FilePickerFileType.ANY,
                                                     ), ],
                                 bgcolor=ft.colors.LIGHT_BLUE_100,
                                 style=ft.ButtonStyle(
                                     shape=ft.ContinuousRectangleBorder(radius=30),
                                     padding=ft.padding.all(10),
                                     color="#000000",
                                     text_style=ft.TextStyle(size=20, color="#000000"),

                                 ),
                                 width=350,
                                 height=50,

                                 )

    def __get_report_textarea_control(self):
        return ft.TextField(
            label="",
            multiline=True,
            min_lines=8,
            max_lines=100,
            value="",
            bgcolor=ft.colors.WHITE,
            text_size=20,

        )

    def __make_report_button_control(self):
        return ft.ElevatedButton("Сформировать заключение",
                                 on_click=self.copy_report_data_to_report_textarea,
                                 #bgcolor=ft.colors.AMBER,
                                 bgcolor=ft.colors.LIGHT_BLUE_100,
                                 style=ft.ButtonStyle(
                                     shape=ft.ContinuousRectangleBorder(radius=30),
                                     padding=ft.padding.all(10),
                                     color="#000000",
                                     text_style=ft.TextStyle(size=20, color="#000000"),

                                 ),
                                 width=350,
                                 height=50,

                                 )

    def generate_template_context(self, report_template: DocxTemplate):
        context = {}

        # здесь надо брать сформированное поле с заключением, а не генерировать его вновь
        final_report_text = self.report_text_area_control.value

        for field in report_template.get_undeclared_template_variables():
            try:
                if field == "final_report":
                    context[field] = final_report_text
                    continue

                if field == "current_date":
                    context[field] = self.report_date_time.strftime("%Y-%m-%d %H:%M:%S")
                    continue

                val = self.global_controls_list.val(field)

                val = val if val else "---"
                context[field] = val
            except Exception as e:
                print(f"Error in self.generate_template_context()\n"
                      f"parameter: {field}. {e}")
        return context

    def __save_file(self, e: ft.FilePickerResultEvent):
        save_location = e.path
        if save_location:
            try:
                # with open(save_location, "wb") as file:
                #     bin_data = io.BytesIO(base64.b64decode(TEMPLATE_BASE64_STRING))
                #     report_template = DocxTemplate(bin_data)
                #     context = self.generate_template_context(report_template)
                #     report_template.render(context)
                #     # data = report_template.save(filename=bin_data)
                #     report_template.save(save_location)
                #
                #     # file.write(bin_data.read())
                bin_data = io.BytesIO(base64.b64decode(TEMPLATE_BASE64_STRING))
                report_template = DocxTemplate(bin_data)
                context = self.generate_template_context(report_template)
                report_template.render(context)
                report_template.save(save_location)

            except Exception as e:
                print("error ", e)

        self.page.update()



    def __get_report_text(self):
        # self.global_controls_list.measurements
        # report - итоговы текст
        data = self.global_controls_list
        report = ""  # = report_data.val("PatientFirstLastName")

        def have_missing_vals(*fields):
            if len(fields) <= 0:
                return True
            for _field in fields:
                if _field.val is None:
                    return True
            return False


        #############################
        # 1. полости сердца -ЛП
        def razmery_polostey_lp():
            m_5_2 = Field("m_5_2")
            m_5_6 = Field("m_5_6")

            if have_missing_vals(m_5_2, m_5_6):
                return ""

            if m_5_2.error and m_5_6.error:
                return ""

            if m_5_2.is_normal and m_5_6.is_normal:
                return ""

            if m_5_2.error and m_5_6.is_normal:
                return ""
            if m_5_2.error and m_5_6.upper_than_normal:
                return "Расширение левого предсердия."
            if m_5_2.is_normal and m_5_6.error:
                return ""
            if m_5_2.upper_than_normal and m_5_6.error:
                return "Расширение левого предсердия."

            if m_5_2.is_normal and m_5_6.upper_than_normal:
                return "Признаки расширения левого предсердия."
            if m_5_6.is_normal and m_5_2.upper_than_normal:
                return "Признаки расширения левого предсердия."

            if m_5_2.upper_than_normal and m_5_6.upper_than_normal:
                return "Расширение левого предсердия."

            #return f"m_5_2 и m_5_6  - необработанный вариант."
            return f""

        report += razmery_polostey_lp() or ""

        #############################
        # 2. полости сердца - ПП
        def razmery_polostey_pp():
            m_7_1 = Field("m_7_1")

            if have_missing_vals(m_7_1):
                return ""

            if m_7_1.error or m_7_1.is_normal:
                return ""

            if m_7_1.upper_than_normal:
                return m_7_1.interval_desc

            #return f"m_7_1 - необработанный вариант."
            return f""

        report += razmery_polostey_pp() or ""

        #############################
        # 3. полости сердца - ЛЖ
        def razmery_polostey_lj():
            m_2_1 = Field("m_2_1")
            m_4_1 = Field("m_4_1")

            if have_missing_vals(m_4_1, m_2_1):
                return ""

            if m_2_1.error and m_4_1.error:
                return ""
            if m_2_1.is_normal and m_4_1.is_normal:
                return ""

            if m_2_1.error and m_4_1.is_normal:
                return ""
            if m_2_1.is_normal and m_4_1.error:
                return ""

            if m_2_1.is_normal and m_4_1.upper_than_normal:
                return "Признаки расширения левого желудочка."
            if m_2_1.upper_than_normal and m_4_1.is_normal:
                return "Признаки расширения левого желудочка."

            if m_2_1.error and m_4_1.upper_than_normal:
                return "Расширение левого желудочка."
            if m_2_1.upper_than_normal and m_4_1.error:
                return "Расширение левого желудочка."

            if m_2_1.upper_than_normal and m_4_1.upper_than_normal:
                return "Расширение левого желудочка."

            return f""

        report += razmery_polostey_lj() or ""

        #############################
        # 4. полости сердца - ПЖ
        def razmery_polostey_pj():
            m_6_1 = Field("m_6_1")
            m_6_2 = Field("m_6_2")
            m_6_3 = Field("m_6_3")

            if have_missing_vals(m_6_3, m_6_2, m_6_1):
                return ""


            if all([m_6_1.error, m_6_2.error, m_6_3.error]):
                return ""

            if all([m_6_1.is_normal, m_6_2.is_normal, m_6_3.is_normal]):
                return ""

            if all([m_6_1.upper_than_normal, m_6_2.upper_than_normal, m_6_3.upper_than_normal]):
                return "Расширение правого желудочка."

            fields_no_errors = [field for field in fields if not field.error]
            fields_no_errors_upper_norm = [field for field in fields_no_errors if field.upper_than_normal]

            if len(fields_no_errors_upper_norm) >= 2:
                return "Расширение правого желудочка."
            elif len(fields_no_errors_upper_norm) == 1:
                return "Признаки расширения правого желудочка."
            else:
                return ""

        report += razmery_polostey_pj() or ""

        #############################
        # 5. ГЛЖ
        def glj():
            m_3_3 = Field("m_3_3")
            m_3_2 = Field("m_3_2")

            if have_missing_vals(m_3_2, m_3_3):
                return ""

            if m_3_3.upper_than_normal and m_3_2.upper_than_normal:
                return "Концентрическое ремоделирование миокарда левого желудочка."
            elif m_3_3.upper_than_normal and m_3_2.is_normal:
                return "Концентрическая гипертрофия миокарда левого желудочка."
            elif m_3_3.is_normal and m_3_2.upper_than_normal:
                return "Эксцентрическая гипертрофия миокарда левого желудочка."
            else:
                return ""

        report += glj() or ""

        #############################
        # 6. Диастолическая функция
        def diastolic_function():
            m_4_3 = Field("m_4_3")
            m_11_5 = Field("m_11_5")
            m_11_1 = Field("m_11_1")
            m_11_8 = Field("m_11_8")
            m_11_7 = Field("m_11_7")
            m_10_3 = Field("m_10_3")
            m_5_6 = Field("m_5_6")

            if have_missing_vals(m_5_6, m_10_3, m_11_7, m_11_8, m_11_1, m_11_5, m_4_3):
                return ""

            check_list1 = [m_11_8, m_11_7, m_10_3, m_5_6]
            check_list2 = [m_11_8, m_10_3, m_5_6]

            if m_4_3.error:
                return ""

            if m_4_3.is_normal:
                normal_fields = [field for field in check_list1 if field.is_normal]
                if len(normal_fields) >= 3:
                    return "Диастолическая функция левого желудочка не нарушена."
                elif len(normal_fields) == 2:
                    return ""
                elif len(normal_fields) <= 1:
                    return "Нарушение диастолической функции левого желудочка."
                else:
                    return ""
            elif m_4_3.lower_than_normal:
                if m_11_5.lower_than_normal and m_11_1.lower_than_normal:
                    return ("Нарушение диастолической функции миокарда левого желудочка "
                            "по 1 типу (гипертрофический тип), характеризующееся нормальным "
                            "давлением в левом предсердии и нарушением релаксации левого желудочка.")
                if m_11_5.upper_than_normal:
                    return "Нарушение диастолической функции миокарда левого желудочка по 3 типу (рестриктивный тип)."
                if m_11_5.is_normal or (m_11_5.lower_than_normal and m_11_1.is_normal):
                    normal_fields = [field for field in check_list2 if field.is_normal]
                    if len(normal_fields) >= 2:
                        return ("Нарушение диастолической функции миокарда левого желудочка "
                                "по 1 типу (гипертрофический тип), характеризующееся нормальным "
                                "давлением в левом предсердии и нарушением релаксации левого желудочка.")
                    elif len(normal_fields) <= 1:
                        return ("Нарушение диастолической функции миокарда левого желудочка по 2 типу: "
                                "псевдо-нормальный кровоток с повышенным давлением в левом предсердии.")
                    else:
                        return ""

            else:
                return ""

        report += diastolic_function() or ""

        #############################
        # 7. Фракция выброса

        def fractional_excretion():
            m_4_3 = Field("m_4_3")

            if have_missing_vals(m_4_3):
                return ""

            if m_4_3.error:
                return ""

            if m_4_3.is_normal:
                return "Систолическая функция левого желудочка сохранена."

            if m_4_3.lower_than_normal:
                return "Систолическая функция левого желудочка снижена."

            return ""

        report += fractional_excretion() or ""

        #############################
        # 8. Аорта синусы

        def aorta_sinus():
            m_1_2 = Field("m_1_2")

            if have_missing_vals(m_1_2):
                return ""

            if m_1_2.is_normal:
                return ""

            if m_1_2.upper_than_normal:
                return "Расширение корня аорты."

            if m_1_2.lower_than_normal:
                return "Сужение корня аорты."

            return ""

        report += aorta_sinus() or ""

        #############################
        # 9. Аорта восходящий отдел

        def aorta_voshod():
            m_1_4 = Field("m_1_4")

            if have_missing_vals(m_1_4):
                return ""

            if m_1_4.is_normal:
                return ""

            if m_1_4.upper_than_normal:
                return "Расширение восходящего отдела аорты."

            if m_1_4.lower_than_normal:
                return "Сужение восходящего отдела аорты."

            return ""

        report += aorta_voshod() or ""

        #############################
        # 10. Аорта дуга

        def aorta_duga():
            m_1_5 = Field("m_1_5")

            if have_missing_vals(m_1_5):
                return ""

            if m_1_5.is_normal:
                return ""

            if m_1_5.upper_than_normal:
                return "Расширение дуги аорты."

            if m_1_5.lower_than_normal:
                return "Сужение дуги аорты."

            return ""

        report += aorta_duga() or ""

        #############################
        # 11. аортальный клапан

        def aorta_klapan():
            m_13_2 = Field("m_13_2")
            m_13_3 = Field("m_13_3")
            m_13_4 = Field("m_13_4")

            if have_missing_vals(m_13_2, m_13_3, m_13_4):
                return ""

            result = ""

            if m_13_2.val:
                result += "Створки аортального клапана уплотнены. "

            if m_13_3.val:
                result += "Створки аортального клапана утолщены. "



            if m_13_4.val == "степень 1":
                result += "Незначительный кальциноз аортального клапана. "
            if m_13_4.val == "степень 2":
                result += "Умеренный кальциноз аортального клапана. "
            if m_13_4.val == "степень 3":
                result += "Выраженный кальциноз аортального клапана. "

            return result

        report += aorta_klapan() or ""

        #############################
        # 12. Аортальный стеноз

        def aorta_stenoz():
            m_9_1 = Field("m_9_1")
            m_9_4 = Field("m_9_4")

            if have_missing_vals(m_9_4, m_9_1):
                return ""

            check_list = [m_9_1, m_9_4]
            use_list = [_field for _field in check_list if
                        _field.interval_type is not IntervalType.NORMAL and
                        _field.interval_type is not IntervalType.ERROR]

            grade_1_list = [f for f in use_list if f.interval_type is IntervalType.GRADE1]
            grade_2_list = [f for f in use_list if f.interval_type is IntervalType.GRADE2]
            grade_3_list = [f for f in use_list if f.interval_type is IntervalType.GRADE3]


            if m_9_4.interval_type is IntervalType.GRADE1 and m_9_1.interval_type is IntervalType.GRADE1:
                return "Формирование незначительного аортального стеноза."
            if m_9_4.interval_type is IntervalType.GRADE2 and m_9_1.interval_type is IntervalType.GRADE2:
                return "Умеренный стеноз аортального клапана."
            if m_9_4.interval_type is IntervalType.GRADE3 and m_9_1.interval_type is IntervalType.GRADE3:
                return "Выраженный стеноз аортального клапана."

            if grade_1_list and grade_2_list:
                return "Умеренный стеноз аортального клапана."
            if grade_2_list and grade_3_list:
                return "Выраженный стеноз аортального клапана."
            if grade_1_list and grade_3_list:
                return "[[ ОШИБКА: при определении степени аортального стеноза !!! ]]"

            return ""


        report += aorta_stenoz() or ""

        #############################
        # 13. Митральный клапан

        def mitral_klapan():
            m_14_2 = Field("m_14_2")
            m_14_3 = Field("m_14_3")
            m_14_4 = Field("m_14_4")

            if have_missing_vals(m_14_2, m_14_3, m_14_4):
                return ""

            result = ""

            if m_14_2.val:
                result += "Створки митрального клапана уплотнены. "

            if m_14_3.val:
                result += "Створки митрального клапана утолщены. "



            if m_14_4.val == "степень 1":
                result += "Незначительный кальциноз митрального клапана. "
            if m_14_4.val == "степень 2":
                result += "Умеренный кальциноз митрального клапана. "
            if m_14_4.val == "степень 3":
                result += "Выраженный кальциноз митрального клапана. "

            return result

        report += mitral_klapan() or ""

        #############################
        # 14. Митральный стеноз
        # НЕТ РЕАЛИЗАЦИИ 15.06.2025
        # def mitral_stenoz():
        #     m_11_3 = Field("m_11_3")
        #     m_11_4 = Field("m_11_4")
        #     m_8_4 = Field("m_8_4")
        #
        # report += mitral_stenoz()


        #############################
        # 15. Легочная гипертензия
        def legojnaya_hypertension():
            m_10_3 = Field("m_10_3")
            m_8_1 = Field("m_8_1")
            m_7_1 = Field("m_7_1")
            m_8_6 = Field("m_8_6")
            m_6_5 = Field("m_6_5")
            m_7_5 = Field("m_7_5")
            m_1_1 = Field("m_1_1")

            if have_missing_vals(m_1_1, m_7_5, m_6_5, m_8_6, m_7_1, m_8_1, m_10_3):
                return ""

            ######################
            # значения не из диапазонов
            critical_speed_rekurgit = 3.4
            upper_speed_rekurgit = 2.8
            min_count_symtoms = 2


            leg_hyp_simtoms = [
                m_8_1.interval_type is IntervalType.UPPER,
                m_7_1.interval_type is IntervalType.GRADE1 or m_7_1.interval_type is IntervalType.GRADE2,
                m_8_6.interval_type is IntervalType.LOWER,
                m_6_5.interval_type is IntervalType.LOWER,
                m_7_5.interval_type is IntervalType.GRADE2 or m_7_5.interval_type is IntervalType.GRADE3,
                (m_7_5.val and m_1_1.val) and (m_7_5.val / m_1_1.val > 1.0),
            ]

            if m_10_3.val:
                if m_10_3.interval_type is IntervalType.NORMAL:
                    # !!! нормальное давление в легочной артерии, но это не выводиться
                    return ""
                if m_10_3.val > critical_speed_rekurgit:
                    return "Лёгочная гипертензия. "
                if upper_speed_rekurgit <= m_10_3.val <= critical_speed_rekurgit:
                    if sum(leg_hyp_simtoms) >= min_count_symtoms:
                        return "Имеются признаки лёгочной гипертензии, повышения нагрузки на правые отделы сердца. "

            # если ничего не сработало, то всё рано вернём пустую строку чтобы не возвращать None
            return ""

        report += legojnaya_hypertension() or ""

        #########################################################################
        #########################################################################
        #########################################################################


        return report
        # return report.replace("\n", "  ")
