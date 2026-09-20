import flet as ft

Config = {
    "MainWindow": {
        "title": "USonicMeter: УЗИ калькулятор. Версия 1.0.2",
        "width": 1150,
        "height": 900,
        "vertical_alignment": ft.MainAxisAlignment.START,
        "theme_mode": ft.ThemeMode.LIGHT,
        "resizable": True,
        "scroll": "auto",
    },

    "Block": {
        "Block_header": {
            "border": None, #ft.border.all(0, "#cccccc"),
            "width": 225,
            "height": 31,
            "padding": 3,
            "margin": 0,
        },
        "Header_text": {
            "color": "black",
            "height": 25,
            "size": 17,
            "width": 225,
            "weight": ft.FontWeight.W_500,
            "alignment": ft.TextAlign.END,
        },
        "measure_title": {
            "color": "black",
            "height": 28,
            "width": 170,
            "size": 16,
        },
        "measure": {
            "width": 80,
            "height": 28,
            "text_size": 16,
            "content_padding": ft.Padding(0, -5, 0, 0),
            "cursor_height": 20,
            "fill_color": ft.colors.WHITE,
            "calculable_fill_color": "#e8e8e8",
            "text_align": ft.TextAlign.CENTER,
            "border_color": "#cccccc",
            "calculable_border_color": "#707070",
            "text_color": "#000000",
            "filled": True,
            "bgcolor": "#000000",
            "border_width": 1,
            "calculable_border_width": 2,
            "max_float_digits": 2,
            "focused_border_width": 3,
        }
    },

}
