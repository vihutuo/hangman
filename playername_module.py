import flet as ft
from typing import Callable, Optional

class PlayerNameControl(ft.UserControl):
    def __init__(self, player_name: str, on_name_change: Optional[Callable[[str], None]] = None):
        super().__init__()
        self.player_name = player_name
        self._text_control: ft.Text | None = None
        self.on_name_change = on_name_change

    def build(self):

        span = ft.TextSpan(
            self.player_name,
            on_click=self._on_click,   # internal member method
            style=ft.TextStyle(
                decoration=ft.TextDecoration.UNDERLINE,
                decoration_style=ft.TextDecorationStyle.DOTTED,
                size=18,
                color=ft.colors.SECONDARY
            )
        )
        self._text_control = ft.Text(style=ft.TextThemeStyle.LABEL_LARGE, spans=[span])
        return self._text_control

    def did_mount(self):
        pass

    def _on_click(self, e: ft.ControlEvent):
          if self.page is not None:
              txt_name = ft.Ref[ft.TextField]()

              def close_dlg_ok(e):
                  txt_name.current.value = txt_name.current.value.strip()
                  if len(txt_name.current.value) == 0:
                      return
                  #update_player_name(txt_name.current.value)
                  self.player_name = txt_name.current.value
                  self._text_control.spans[0].text = self.player_name
                  dlg_modal.open = False
                  if callable(self.on_name_change):
                      try:
                          self.on_name_change(self.player_name)
                      except Exception as ex:
                            print("on_name_change callback error:", ex)
                  self.page.update()
                  self._text_control.update()

              def close_dlg_cancel(e):
                  dlg_modal.open = False
                  self.page.update()

              dlg_modal = ft.AlertDialog(
                  modal=True,
                  title=ft.Text("Enter your name"),
                  content=ft.TextField(ref=txt_name, hint_text="Enter your name", value=self.player_name, max_length=10),
                  actions=[
                      ft.TextButton("OK", on_click=close_dlg_ok),
                      ft.TextButton("Cancel", on_click=close_dlg_cancel),
                  ],
                  actions_alignment=ft.MainAxisAlignment.CENTER,
              )
              self.page.open(dlg_modal)
              self.page.update()