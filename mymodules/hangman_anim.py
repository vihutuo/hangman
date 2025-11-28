import flet as ft
from typing import Any

def create_hangman_display(width: int = 260, height: int = 200) -> ft.Container:

    c = ft.Container(
        width=width,
        height=height,
        alignment=ft.alignment.center,
        bgcolor="#1A1A1A",
        border_radius=15,
        padding=15,
        border=ft.border.all(3, "#FF4F4F"),
        animate_opacity=300,
        animate_scale=300,
        scale=ft.Scale(1.0),
        opacity=1.0
    )
    c.content = ft.Text("", size=34, font_family="Courier New")
    return c


def set_hangman_stage(hangman_display: ft.Container, stage_text: str) -> None:

    hangman_display.opacity = 0
    hangman_display.content = ft.Text(
        stage_text,
        size=34,
        color="#FF4F4F",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        font_family="Courier New"
    )
    hangman_display.opacity = 1


def flash_and_shake(hangman_display: ft.Container, page: Any, flash_color: str = "#330000", scale_up: float = 1.15) -> None:

    orig_scale = getattr(hangman_display, "scale", ft.Scale(1.0))
    orig_bg = hangman_display.bgcolor

    hangman_display.scale = ft.Scale(scale_up)
    hangman_display.bgcolor = flash_color
    hangman_display.update()
    page.update()


    hangman_display.scale = orig_scale
    hangman_display.bgcolor = orig_bg
    hangman_display.update()
    page.update()
