import flet as ft

def create_student_view(df, on_select)->ft.Control:
    detail_panel=ft.Container(
        bgcolor=ft.Colors.BLUE_50,
        expand=True
    )
    def on_click_student(e, name:str, version:str):
        detail_df=on_select(name, version)
        info=detail_df.iloc[0]
        terrain_ranks=detail_df['rank'].tolist()
        detail_panel.content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            controls=[
                ft.Image(
                    src=f"{info['memory_image_path']}"
                ),
                ft.Text(f"{info['fullname']}({info['version']})",size=30, weight=ft.FontWeight.BOLD),
                ft.Text(f"{info['school']} - {info['club']}", size=20),
                ft.Row(
                    controls=[
                        ft.Text(f"{info['combat_class']}",size=30),
                        ft.Column(
                            controls=[
                                ft.Text(f"{info['role']}",size=15),
                                ft.Text(f"{info['position']}",size=15)
                            ],
                            spacing=1
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(f"{info['attack']}",size=15),
                                ft.Text(f"{info['defense']}",size=15)
                            ],
                            spacing=1
                        ),
                        ft.Text(f"시가지 : {terrain_ranks[0]} 실내 : {terrain_ranks[1]} 야외 : {terrain_ranks[2]}",size=30)
                    ]
                ),
                ft.Text(f"Ex 스킬 : {info['ex_skill']}"),
                ft.Text(f"기본 스킬 : {info['normal_skill']}"),
                ft.Text(f"강화 스킬 : {info['passive_skill']}"),
                ft.Text(f"서브 스킬 : {info['sub_skill']}")
            ]
        )

        e.page.update()

    card_list=[]
    for _, row in df.iterrows():
        if row['attack']=='폭발':
            bg_color=ft.Colors.RED_900
        elif row['attack']=='관통':
            bg_color=ft.Colors.ORANGE
        elif row['attack']=='신비':
            bg_color=ft.Colors.BLUE
        elif row['attack']=='진동':
            bg_color=ft.Colors.PURPLE_500
        card=ft.Container(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        src=f"{row['image_path']}",
                        width=100,
                        height=100,
                        fit=ft.BoxFit.CONTAIN
                    ),
                    ft.Text(f"{row['name']}({row['version']})",weight=ft.FontWeight.BOLD,size=9,)
                ],
                spacing=1
            ),
            bgcolor=bg_color,
            on_click=lambda e, name=row['name'], version=row['version']: on_click_student(e, name, version)
        )
        card_list.append(card)
    
    grid=ft.GridView(
        expand=True,
        runs_count=6,
        spacing=30,
        run_spacing=15,
        controls=card_list,
        padding=ft.Padding(0,0,0,50)
    )

    return ft.Row(
        expand=True,
        controls=[
            grid,
            detail_panel
        ]
    )