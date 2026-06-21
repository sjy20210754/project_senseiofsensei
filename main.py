import service
import flet as ft
from views.student_view import create_student_view
from views.boss_view import create_boss_view

def main(page: ft.page):
    page.title='Sensei of Sensei'
    #-------------------------------------------------------------------------------
    # region : DuckDB DDL
    #-------------------------------------------------------------------------------
    con=service.connect_database("data/sensei_of_sensei.db")
    service.initialize(con)
    #-------------------------------------------------------------------------------
    # region : student view
    #-------------------------------------------------------------------------------
    student_df=service.get_studentlist(con)

    def select_student(name:str, version:str):
        """
        뷰 내에서 학생 선택 시 선택한 학생의 상세 정보를 조회하기 위해 service.find_student_detail 함수를 실행
        """
        return service.find_student_detail(con, name, version)
    
    tab_students=create_student_view(student_df, select_student)
    #-------------------------------------------------------------------------------
    # region : boss view
    #-------------------------------------------------------------------------------
    boss_df=service.get_bosslist(con)

    def select_boss(name:str):
        """
        뷰 내에서 보스 선택 시 선택한 보스의 상세 정보를 조회하기 위해 service.find_boss_hp 함수를 실행
        """
        return service.find_boss_hp(con, name)
    
    def boss_counter(name:str, defense:str, terrain:str):
        """
        선택한 보스의 방어타입과 지형을 통해 해당 보스에 강한 딜러 학생을 조회할 수 있는 service.find_counter_of_boss 함수를 실행
        """
        return service.find_counter_of_boss(con, name, defense, terrain)
    
    tab_bosses=create_boss_view(boss_df, select_boss, boss_counter)

    #-------------------------------------------------------------------------------
    # region : tab
    #-------------------------------------------------------------------------------
    tabs=ft.Tabs(
        length=3,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="학생"),
                        ft.Tab(label="보스"),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        tab_students,
                        tab_bosses,
                    ]
                )
            ]
        )
    )

    page.add(
        tabs,
    )
    




if __name__ == "__main__":
    ft.run(main)
