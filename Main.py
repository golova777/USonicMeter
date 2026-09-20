from datetime import datetime
import os

import flet as ft
from flet_core import IconButton, icons
from rich.text import Text

from CONFIG import Config as CFG
from Measures import Block, GeneralField, GlobalControlsList
from MEASUREMENTS_CONFIG import measurement_blocks as blocks
from MEASUREMENTS_CONFIG import general_fields as fields
from Measures import Page

from page_blocks.menu_bar import AppBar
from Report import Report


def main(page: ft.Page):
    page.title = CFG["MainWindow"]["title"]
    page.theme_mode = CFG["MainWindow"]["theme_mode"]
    page.vertical_alignment = CFG["MainWindow"]["vertical_alignment"]
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = CFG["MainWindow"]["width"]
    page.window.height = CFG["MainWindow"]["height"]
    page.window.resizable = CFG["MainWindow"]["resizable"]
    page.scroll = CFG["MainWindow"]["scroll"]

    Page.set_page(page)

    # создадим поля общего назначения
    patient_first_last_name_field = GeneralField(fields["fields"]["PatientFirstLastName"]).get_control()
    birth_year = GeneralField(fields["fields"]["birth_year"]).get_control()
    gender_field = GeneralField(fields["fields"]["gender"]).get_control()

    # Создадим блоки вычислений
    init_1_block = Block(blocks["init_block_1"])
    init_2_block = Block(blocks["init_block_2"])
    init_3_block = Block(blocks["init_block_3"])
    init_4_block = Block(blocks["init_block_4"])

    aorta_block = Block(blocks["aorta"])
    left_ventricle = Block(blocks["left_ventricle"])
    UnknownBlock1 = Block(blocks["UnknownBlock1"])
    UnknownBlock2 = Block(blocks["UnknownBlock2"])

    left_atrium = Block(blocks["left_atrium"])
    right_ventricle = Block(blocks["right_ventricle"])
    right_atrium = Block(blocks["right_atrium"])
    unknownBlock3 = Block(blocks["UnknownBlock3"])

    aortic_valve = Block(blocks["aortic_valve"])
    pk_tk = Block(blocks["pk_tk"])
    diastolic_pk = Block(blocks["diastolic_pk"])
    unknownBlock4 = Block(blocks["UnknownBlock4"])

    extra_block1 = Block(blocks["extra_block1"])
    extra_block2 = Block(blocks["extra_block2"])

    #######################################################################
    # Объект отчёта
    report = Report(page, GlobalControlsList)
    #######################################################################

    # Здесь добавить блоки

    top_row = ft.Row(
        [

            patient_first_last_name_field,
            gender_field,
            birth_year,

        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    init_row = ft.Row(
        [
            init_1_block.control,
            init_2_block.control,
            # init_3_block.control,
            # init_4_block.control,

        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    row_1 = ft.Row(
        [
            aorta_block.control,
            left_ventricle.control,
            UnknownBlock1.control,
            UnknownBlock2.control,
            # Сюда добавлять блоки
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    row_2 = ft.Row(
        [
            left_atrium.control,
            right_ventricle.control,
            right_atrium.control,
            unknownBlock3.control,
            # Сюда добавлять блоки
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    row_3 = ft.Row(
        [
            aortic_valve.control,
            pk_tk.control,
            diastolic_pk.control,
            unknownBlock4.control,
            # Сюда добавлять блоки
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    row_4 = ft.Row(
        [
            extra_block1.control,
            extra_block2.control,
            # Сюда добавлять блоки
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    report = ft.Row(

        [
            ft.Column(
                [
                    ft.Row([
                        # сформировать заключение - кнопка
                        report.report_button_control,
                        # Кнопка для генерации файла отчёта
                        report.get_create_report_button(),
                    ]),
                    # поле для вывода заключения
                    report.report_text_area_control,
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=10,

                width=CFG["MainWindow"]["width"]-80,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

        vertical_alignment=ft.CrossAxisAlignment.START
    )

    # def mysavefile(e: ft.FilePickerResultEvent):
    #     save_location = e.path
    #     if save_location:
    #         try:
    #             with open(save_location, "w", encoding="utf-8")  as file:
    #                 print("сохраненно успешно")
    #                 file.write(txt)
    #         except Exception as e:
    #             print("error ", e)
    #
    #     page.update()

    # saveme = ft.FilePicker(on_result=mysavefile)
    # page.overlay.append(saveme)

    page.add(

        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.colors.AMBER_ACCENT_200),
            # bgcolor=ft.colors.SURFACE_VARIANT,
            padding=5,
            margin=0,
            width=CFG["MainWindow"]["width"],
            # border=ft.border.all(1, "#cccccc"),
            border_radius=ft.border_radius.all(6),
            content=top_row,
        ),

        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.colors.AMBER_ACCENT_200),
            # bgcolor=ft.colors.SURFACE_VARIANT,
            padding=5,
            margin=0,
            width=CFG["MainWindow"]["width"],
            # border=ft.border.all(1, "#cccccc"),
            border_radius=ft.border_radius.all(6),
            content=init_row,
        ),
        ft.Divider(height=1, color="#cccccc"),

        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.colors.AMBER_ACCENT_200),
            # bgcolor=ft.colors.SURFACE_VARIANT,
            padding=5,
            margin=0,
            width=CFG["MainWindow"]["width"],
            # border=ft.border.all(1, "#cccccc"),
            border_radius=ft.border_radius.all(8),
            content=row_1,
        ),

        ft.Divider(height=1, color="black"),
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.colors.AMBER_ACCENT_200),
            # bgcolor=ft.colors.SURFACE_VARIANT,
            padding=0,
            margin=0,
            width=CFG["MainWindow"]["width"],
            # border=ft.border.all(1, ft.colors.BLACK87),
            border_radius=ft.border_radius.all(8),
            content=row_2,
        ),
        ft.Divider(height=1, color="black"),
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.colors.AMBER_ACCENT_200),
            # bgcolor=ft.colors.SURFACE_VARIANT,
            padding=0,
            margin=0,
            width=CFG["MainWindow"]["width"],
            # border=ft.border.all(1, ft.colors.BLACK87),
            border_radius=ft.border_radius.all(8),
            content=row_3,
        ),
        ft.Divider(height=1, color="black"),
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.colors.AMBER_ACCENT_200),
            # bgcolor=ft.colors.SURFACE_VARIANT,
            padding=0,
            margin=0,
            width=CFG["MainWindow"]["width"],
            # border=ft.border.all(1, ft.colors.BLACK87),
            border_radius=ft.border_radius.all(8),
            content=row_4,
        ),

        ft.Divider(height=1, color="#cccccc"),

        # # сформировать заключение - кнопка
        # report.report_button_control,
        #
        # # поле для вывода заключения
        # report.report_text_area_control,

        ft.Divider(height=1, color="black"),
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.colors.AMBER_ACCENT_200),
            # bgcolor=ft.colors.SURFACE_VARIANT,
            padding=0,
            margin=0,
            width=CFG["MainWindow"]["width"],
            # border=ft.border.all(1, ft.colors.BLACK87),
            border_radius=ft.border_radius.all(8),
            content=report,
        ),

        # Кнопка для генерации файла отчёта
        # report.get_create_report_button(),
    )

    page.appbar = AppBar(page).get_control()

    page.update()


if __name__ == "__main__":
    # , view=ft.AppView.WEB_BROWSER
    ft.app(target=main)
