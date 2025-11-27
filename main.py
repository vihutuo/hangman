import flet as ft
import random
from words import words

random.shuffle(words)

def create_button(text, on_click, width=120, height=40):
    return ft.ElevatedButton(text, on_click=on_click, width=width, height=height)

def create_stat_text(label, value, color):
    return ft.Text(f"{label}: {value}", size=24, color=color, weight=ft.FontWeight.BOLD, font_family="Comic Sans MS")

def HomeView(page: ft.Page, leaderboard):
    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("👻 HANGMAN GAME 👻", size=48, weight=ft.FontWeight.BOLD, color="#FF7A7A", font_family="Comic Sans MS"),
                    create_button("▶ Play Hangman", lambda e: HangmanView(page, leaderboard), width=220, height=50),
                    create_stat_text("Score", leaderboard["score"], "#FFD369"),
                    create_stat_text("Hints", leaderboard.get("hints", 3), "#00FFFF")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            expand=True,
            alignment=ft.alignment.center
        )
    )
    page.update()

def HangmanView(page: ft.Page, leaderboard, word_index=0):
    if word_index >= len(words):
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text("🎉 All words completed!", size=40, weight=ft.FontWeight.BOLD, color="#FFD369", font_family="Comic Sans MS"),
                create_button("🏠 Back to Home", lambda e: HomeView(page, leaderboard))
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
        )
        page.update()
        return

    secret_word = words[word_index].upper()
    guessed_letters = []
    attempts = 6
    hints = leaderboard.get("hints", 3)
    leaderboard["hints"] = hints
    score = leaderboard["score"]
    hangman_stages = ["", "O", "O\n |", "O\n/|", "O\n/|\\", "O\n/|\\\n/", "O\n/|\\\n/ \\"]

    hangman_display = ft.Container(width=260, height=200, alignment=ft.alignment.center,
                                   bgcolor="#1A1A1A", border_radius=15, padding=15, border=ft.border.all(3, "#FF4F4F"))
    message = ft.Text("", size=24, color="#FFD369", weight=ft.FontWeight.BOLD, font_family="Comic Sans MS")
    hearts = ft.Text("❤ " * attempts, size=32, color="#FF2B2B", weight=ft.FontWeight.BOLD, font_family="Comic Sans MS")
    tiles_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8)

    score_text = create_stat_text("Score", score, "#FFDD55")
    attempts_text = create_stat_text("Attempts", attempts, "#FF4F4F")
    hints_text = create_stat_text("Hints", hints, "#00FFFF")

    def update_ui():
        tiles_row.controls.clear()
        for letter in secret_word:
            display = letter if letter in guessed_letters else ""
            tiles_row.controls.append(
                ft.Container(ft.Text(display, size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF", font_family="Comic Sans MS"),
                             width=50, height=50, border=ft.border.all(2, "#FFD369"), border_radius=5, alignment=ft.alignment.center,
                             bgcolor="#1A1A1A"))
        stage_index = 6 - attempts
        hangman_display.content = ft.Text(hangman_stages[max(stage_index, 0)], size=38, color="#FF4F4F", weight=ft.FontWeight.BOLD,
                                         text_align=ft.TextAlign.CENTER, font_family="Comic Sans MS")
        score_text.value = f"Score: {score}"
        attempts_text.value = f"Attempts: {attempts}"
        hints_text.value = f"Hints: {hints}"
        hearts.value = "❤ " * attempts
        page.update()

    def check_word():
        nonlocal score, hints
        if all(l in guessed_letters for l in secret_word):
            score += 5
            hints += 1
            leaderboard["hints"] = hints
            message.value = f"🎉 Correct! +5 points | 💡 +1 Hint"
            next_btn.disabled = False
            for b in keyboard_buttons: b.disabled = True
            leaderboard["score"] = score
        elif attempts <= 0:
            message.value = f"❌ You lost! Word was: {secret_word}"
            next_btn.disabled = False
            for b in keyboard_buttons: b.disabled = True
        page.update()

    def letter_click(e):
        nonlocal attempts
        letter = e.control.text
        e.control.disabled = True
        guessed_letters.append(letter)
        if letter not in secret_word:
            attempts -= 1
            message.value = "❌ Wrong!"
        else:
            message.value = "✔ Correct!"
        update_ui()
        check_word()

    def restart_word(e): HangmanView(page, leaderboard, word_index)
    def next_word(e): HangmanView(page, leaderboard, word_index + 1)
    def hint_word(e):
        nonlocal hints
        if hints <= 0: return
        remaining = [l for l in secret_word if l not in guessed_letters]
        if remaining:
            guessed_letters.append(random.choice(remaining))
            hints -= 1
            leaderboard["hints"] = hints
            update_ui()

    keyboard_buttons = []
    rows = []
    row = []
    for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        btn = ft.ElevatedButton(letter, width=40, height=40, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                on_click=letter_click)
        keyboard_buttons.append(btn)
        row.append(btn)
        if (i + 1) % 9 == 0:
            rows.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER, spacing=5))
            row = []
    if row: rows.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER, spacing=5))

    next_btn = create_button("➡ Next Word", next_word, width=120, height=40)
    next_btn.disabled = True
    buttons_column = ft.Column([create_button("💡 Hint", hint_word), create_button("🔄 Restart", restart_word), next_btn, create_button("🏠 Home", lambda e: HomeView(page, leaderboard))],
                               alignment=ft.MainAxisAlignment.START, spacing=15)

    message_column = ft.Column([ft.Container(content=message, width=250, height=100, alignment=ft.alignment.center_left,
                                             padding=ft.Padding(10,10,10,10), bgcolor="#1A1A1A", border_radius=10, border=ft.border.all(2, "#FFD369"))],
                               alignment=ft.MainAxisAlignment.START)

    center_column = ft.Column([ft.Text(f"Word {word_index+1}/{len(words)}", size=28, color="#FFFFFF", font_family="Comic Sans MS"),
                               hangman_display, hearts, tiles_row,
                               ft.Row([score_text, attempts_text, hints_text], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                               ft.Column(rows, spacing=5)],
                              alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

    page.controls.clear()
    page.add(ft.Row([buttons_column, center_column, message_column],
                    alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=50))
    update_ui()

def main(page: ft.Page):
    page.title = "Hangman Game"
    page.bgcolor = "#0D0D0D"
    page.bgimage = ft.DecorationImage(src="background.jpg", fit=ft.ImageFit.COVER, repeat=ft.ImageRepeat.NO_REPEAT, opacity=0.15)
    page.theme = ft.Theme(font_family="Comic Sans MS")
    HomeView(page, {"score":0, "hints":3})

ft.app(target=main, view=ft.AppView.WEB_BROWSER)