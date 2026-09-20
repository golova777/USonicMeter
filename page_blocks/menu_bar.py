import flet as ft
from Measures import GlobalControlsList, DEBUG_LABELS





class AppBar:
    def __init__(self, page: ft.Page):
        self.page = page
        self.alert_dialog_control_modal = self.get_alert_dialog_control()
        self.control_list = [
            # ft.ElevatedButton(
            #     "Debug",
            #     #icon=ft.icons.BOY,
            #     on_click=lambda e: [DEBUG_LABELS.toggle(), self.page.update()]
            #
            # ),
            ft.ElevatedButton(
                "Очистить форму",
                icon=ft.icons.CLEAR,
                on_click=lambda e: self.page.open(self.alert_dialog_control_modal)
            ),
        ]

    def get_control(self):
        return ft.AppBar(
            leading=ft.Icon(ft.icons.MONITOR_HEART_SHARP),
            leading_width=40,
            title=ft.Text("УЗИ Калькулятор // Врач: Груздева А.А. д.м.н.", size=15),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[*self.control_list, ],

        )

    def get_alert_dialog_control(self):
        def handle_close(e):
            self.page.close(alert_dialog)

        def handle_close_and_clear(e):
            self.page.close(alert_dialog)
            GlobalControlsList.clear_entire_form(e)

        alert_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Очистить форму?"),
            content=ft.Text("Удалить все заполненные и рассчитанные значения?"),
            actions=[
                ft.TextButton("Да", on_click=handle_close_and_clear),
                ft.TextButton("Нет", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        return alert_dialog
