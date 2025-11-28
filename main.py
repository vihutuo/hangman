import flet as ft
import random
from words import words
from mymodules import player_name_ctrl
from mymodules.leaderboard_ctrl import create_leaderboard_table
from mymodules.hangman_anim import create_hangman_display, set_hangman_stage, flash_and_shake


def create_button(text, on_click, width=120, height=40):
    return ft.ElevatedButton(
        text,
        on_click=on_click,
        width=width,
        height=height,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Segoe UI", weight=ft.FontWeight.BOLD, size=16)
        )
    )

def create_stat_text(label, value, color, size=24, font="Segoe UI"):
    return ft.Text(
        f"{label}: {value}",
        size=size,
        color=color,
        weight=ft.FontWeight.BOLD,
        font_family=font
    )

def HomeView(page: ft.Page, leaderboard):
    leaderboard.setdefault("high_score", leaderboard["score"])
    leaderboard_table = create_leaderboard_table([{"name": "Player1", "score": leaderboard.get("high_score", 0)}])

    rules_list = [
        "Guess the secret word letter by letter.",
        "You have 6 attempts for each word.",
        "Each correct word gives you 5 points.",
        "Using a hint reduces your hint count by 1.",
        "Try to get the highest score possible!"
    ]
    rules_table = ft.Container(
        content=ft.Column(
            [
                ft.Text("📜 Rules", size=20, weight=ft.FontWeight.BOLD, color="#FFD369", font_family="Segoe UI"),
                ft.Divider(thickness=2, color="#FFD369"),
                *[ft.Text(f"• {rule}", size=16, color="#FFFFFF", font_family="Segoe UI") for rule in rules_list]
            ],
            spacing=8
        ),
        padding=15, bgcolor="#1A1A1A", border=ft.border.all(2, "#FFD369"), border_radius=10, width=350
    )

    def start_easy(e):
        selected_words = random.sample(words, min(10, len(words)))
        HangmanView(page, leaderboard, word_list=selected_words)

    def start_hard(e):
        selected_words = random.sample(words, min(25, len(words)))
        HangmanView(page, leaderboard, word_list=selected_words)

    page.controls.clear()
    page.add(
        ft.Column([
            ft.Text("👻 HANGMAN GAME 👻", size=48, weight=ft.FontWeight.BOLD, color="#FF7A7A", font_family="Impact"),
            ft.Row([
                create_button("▶ Play Hangman (Easy)", start_easy, width=180, height=50),
                create_button("▶ Play Hangman (Hard)", start_hard, width=180, height=50)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=20),
            ft.Row([leaderboard_table, ft.Container(width=50), rules_table],
                   alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
        )
    )
    page.update()


def HangmanView(page: ft.Page, leaderboard, word_index=0, word_list=None):
    if word_list is None:
        word_list = random.sample(words, len(words))
    if word_index >= len(word_list):
        page.controls.clear()
        page.add(ft.Column([
            ft.Text("🎉 All words completed!", size=40, weight=ft.FontWeight.BOLD, color="#FFD369", font_family="Impact"),
            create_button("🏠 Back to Home", lambda e: HomeView(page, leaderboard))
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=15))
        page.update()
        return

    secret_word = word_list[word_index].upper()
    guessed_letters = []
    attempts = 6
    hints = leaderboard.get("hints", 3)
    leaderboard["hints"] = hints
    score = leaderboard["score"]
    hangman_stages = ["", "O", "O\n |", "O\n/|", "O\n/|\\", "O\n/|\\\n/", "O\n/|\\\n/ \\"]

    # USE the animation module to create the hangman display
    hangman_display = create_hangman_display(width=260, height=200)

    message = ft.Text("", size=24, color="#FFD369", weight=ft.FontWeight.BOLD, font_family="Segoe UI")
    hearts = ft.Text("❤ " * attempts, size=32, color="#FF2B2B", weight=ft.FontWeight.BOLD, font_family="Courier New")
    tiles_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8)

    score_text = create_stat_text("Score", score, "#FFDD55")
    attempts_text = create_stat_text("Attempts", attempts, "#FF4F4F")
    hints_text = create_stat_text("Hints", hints, "#00FFFF")

    def update_ui():
        tiles_row.controls.clear()
        for l in secret_word:
            tiles_row.controls.append(
                ft.Container(ft.Text(l if l in guessed_letters else "", size=32, weight=ft.FontWeight.BOLD,
                                     color="#FFFFFF", font_family="Courier New"),
                             width=50, height=50, border=ft.border.all(2, "#FFD369"),
                             border_radius=5, alignment=ft.alignment.center, bgcolor="#1A1A1A")
            )

        # use helper to set stage (fade-in). then update the container/page so animation happens
        set_hangman_stage(hangman_display, hangman_stages[6 - attempts])
        hangman_display.update()

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

            # call the shared flash_and_shake animation (module handles update calls)
            flash_and_shake(hangman_display, page)

        else:
            message.value = "✔ Correct!"
        update_ui()
        check_word()

    def restart_word(e): HangmanView(page, leaderboard, word_index, word_list)
    def next_word(e): HangmanView(page, leaderboard, word_index + 1, word_list)
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
    for i, l in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        btn = ft.ElevatedButton(l, width=40, height=40,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8),
                                                     text_style=ft.TextStyle(font_family="Courier New",
                                                                             weight=ft.FontWeight.BOLD, size=16)),
                                on_click=letter_click)
        keyboard_buttons.append(btn)
        row.append(btn)
        if (i + 1) % 9 == 0:
            rows.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER, spacing=5))
            row = []
    if row: rows.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER, spacing=5))

    next_btn = create_button("➡ Next Word", next_word, width=120)
    next_btn.disabled = True
    buttons_column = ft.Column([create_button("💡 Hint", hint_word), create_button("🔄 Restart", restart_word),
                                next_btn, create_button("🏠 Home", lambda e: HomeView(page, leaderboard))],
                               alignment=ft.MainAxisAlignment.START, spacing=15)

    # Style player name
    player_name_control = player_name_ctrl.PlayerNameControl("Player1", None)
    player_name_control.name_text.size = 28
    player_name_control.name_text.weight = ft.FontWeight.BOLD
    player_name_control.name_text.color = "#FFD369"

    message_column = ft.Column([
        ft.Row(
            [player_name_control],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        ft.Container(
            content=message,
            width=250,
            height=100,
            alignment=ft.alignment.center_left,
            padding=ft.Padding(10, 10, 10, 10),
            bgcolor="#1A1A1A",
            border_radius=10,
            border=ft.border.all(2, "#FFD369")
        )
    ],
        alignment=ft.MainAxisAlignment.START)

    center_column = ft.Column([ft.Text(f"Word {word_index+1}/{len(word_list)}", size=28, color="#FFFFFF", font_family="Impact"),
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
    page.bgcolor = "#0D0D0D"  # dark background
    page.theme_mode = ft.ThemeMode.DARK  # dark theme enabled
    page.bgimage = ft.DecorationImage(
        src="background.jpg",
        fit=ft.ImageFit.COVER,
        repeat=ft.ImageRepeat.NO_REPEAT,
        opacity=0.15
    )
    page.theme = ft.Theme(font_family="Segoe UI")  # font
    HomeView(page, {"score": 0, "hints": 3})


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
