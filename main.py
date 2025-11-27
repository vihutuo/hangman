import flet as ft
import random
from words import words

random.shuffle(words)

def HangmanView(page: ft.Page, leaderboard, word_index=0):
    if word_index >= len(words):
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    ft.Text("🎉 All words completed!", size=40, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Final Score: {leaderboard['score']}", size=28),
                    ft.ElevatedButton(
                        "🏠 Back to Home",
                        on_click=lambda e: HomeView(page, leaderboard)
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )
        page.update()
        return

    secret_word = words[word_index].upper()
    guessed_letters = []
    attempts = 5

    hearts = ft.Text(size=28, color="red")
    word_display = ft.Text(size=28, weight=ft.FontWeight.BOLD)
    message = ft.Text(size=20)
    score_text = ft.Text(f"Score: {leaderboard['score']}", size=22, color="yellow")

    hangman_stages = [
        "",
        "O",
        "O\n |",
        "O\n/|",
        "O\n/|\\",
        "O\n/|\\\n/",
        "O\n/|\\\n/ \\"
    ]
    hangman_display = ft.Container(
        content=ft.Text(
            "",
            size=32,
            color="white",
            text_align=ft.TextAlign.CENTER
        ),
        height=140,
        alignment=ft.alignment.top_center
    )

    def update_ui():
        display = ""
        for letter in secret_word:
            if letter in guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        word_display.value = display
        hearts.value = "❤ " * attempts
        stage_index = max(0, 5 - attempts)
        hangman_display.content.value = hangman_stages[stage_index]
        score_text.value = f"Score: {leaderboard['score']}"
        page.update()

    def check_word():
        nonlocal attempts
        if set(secret_word) <= set(guessed_letters):
            leaderboard["score"] += 5
            message.value = "🎉 Correct! +5 points"
            page.update()
            HangmanView(page, leaderboard, word_index + 1)
            return

        if attempts <= 0:
            leaderboard["score"] -= 1
            if leaderboard["score"] < 0:
                leaderboard["score"] = 0

            message.value = f"❌ You lost! The word was: {secret_word}"
            page.update()
            HangmanView(page, leaderboard, word_index + 1)
            return

    def letter_click(e):
        nonlocal attempts
        letter = e.control.text
        e.control.disabled = True
        guessed_letters.append(letter)
        if letter not in secret_word:
            attempts -= 1
            message.value = "❌ Wrong letter!"
        else:
            message.value = "✔ Correct!"
        update_ui()
        check_word()

    def restart_word(e):
        nonlocal guessed_letters, attempts
        guessed_letters = []
        attempts = 5
        message.value = ""
        for btn in keyboard_buttons:
            btn.disabled = False
        update_ui()

    keyboard_buttons = []
    rows = []
    row = []

    for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        btn = ft.ElevatedButton(letter, width=36, height=36, on_click=letter_click)
        keyboard_buttons.append(btn)
        row.append(btn)
        if (i + 1) % 9 == 0:
            rows.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER, spacing=5))
            row = []

    if row:
        rows.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER, spacing=5))

    restart_btn = ft.ElevatedButton("🔄 Restart Word", on_click=restart_word)
    back_btn = ft.ElevatedButton("🏠 Back to Home", on_click=lambda e: HomeView(page, leaderboard))

    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Row(
                    [back_btn, score_text],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Text(f"Word {word_index + 1} / {len(words)}", size=24),
                ft.Text("HANGMAN GAME", size=36, weight=ft.FontWeight.BOLD),
                hangman_display,
                hearts,
                word_display,
                ft.Column(rows, spacing=4),
                restart_btn,
                message,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            expand=True
        )
    )

    update_ui()

def HomeView(page: ft.Page, leaderboard):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Welcome to Hangman Game", size=40, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "▶ Play Hangman",
                    on_click=lambda e: HangmanView(page, leaderboard),
                    width=200,
                    height=50
                ),
                ft.Text(f"Current Score: {leaderboard['score']}", size=22, color="yellow")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )
    page.update()

def main(page: ft.Page):
    page.title = "Hangman Game"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    leaderboard = {"score": 0}
    HomeView(page, leaderboard)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)