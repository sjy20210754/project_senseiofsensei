import flet as ft

def create_boss_view(df, on_select, boss_counter)->ft.Control:
    detail_panel=ft.Container(
        bgcolor=ft.Colors.BLUE_50,
        expand=True
    )
    def on_click_boss(e, name:str, defense:str, attack:str, terrain:str):
        detail_df=on_select(name)
        hp_list=detail_df['hp'].tolist()
        counter_df=boss_counter(name, defense, terrain)
        counter_list=[]
        for _, row in counter_df.iterrows():
            card=ft.Text(f"{row['name']}({row['version']})")
            counter_list.append(card)
        detail_panel.content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            controls=[
                ft.Image(
                    src=f"assets/images/{name}.png"
                ),
                ft.Text(f"{name}", size=30, weight=ft.FontWeight.BOLD),
                ft.Text(f"{attack} {defense} {terrain}", size=20),
                ft.Text(f"Normal : {hp_list[0]}"),
                ft.Text(f"Hard : {hp_list[1]}"),
                ft.Text(f"VeryHard : {hp_list[2]}"),
                ft.Text(f"HardCore : {hp_list[3]}"),
                ft.Text(f"Extreme : {hp_list[4]}"),
                ft.Text(f"Insane : {hp_list[5]}"),
                ft.Text(f"Torment : {hp_list[6]}"),
                ft.Text("상성 좋은 딜러", size=30, weight=ft.FontWeight.BOLD),
                ft.Column(
                    controls=counter_list
                )
            ]
        )
    
    card_list=[]
    for _, row in df.iterrows():
        card=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(f"{row['name']}",weight=ft.FontWeight.BOLD,size=30),
                    ft.Text(f"{row['attack']} {row['defense']} {row['terrain']}"),
                    ft.Image(
                        src=f"assets/images/{row['name']}.png",
                        width=300,
                        height=100,
                        fit=ft.BoxFit.CONTAIN
                    ),
                ]
            ),
            on_click=lambda e, name=row['name'], defense=row['defense'], attack=row['attack'], terrain=row['terrain']: on_click_boss(e, name, defense, attack, terrain)
        )
        card_list.append(card)

    left=ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        controls=card_list
    )

    return ft.Row(
        expand=True,
        controls=[
            left, detail_panel
        ]
    )

    