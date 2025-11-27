import flet as ft

def create_leaderboard_table(leaderboard_data: list[dict]):
    sorted_data = sorted(leaderboard_data, key=lambda x: x["score"], reverse=True)

    rows = []
    for i, entry in enumerate(sorted_data, start=1):
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(i), size=20)),
                    ft.DataCell(ft.Text(entry["name"], size=20)),
                    ft.DataCell(ft.Text(str(entry["score"]), size=20)),
                ]
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Rank", size=22, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Player Name", size=22, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Highest Score", size=22, weight=ft.FontWeight.BOLD)),
        ],
        rows=rows,
        column_spacing=40,
        heading_row_color="#303030",
        border=ft.border.all(1, "#BBBBBB"),
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("🏆 Leaderboard", size=40, weight=ft.FontWeight.BOLD, color="#FFD369"),
                table,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=20,
        bgcolor="#1A1A1A",
        border_radius=15,
    )
