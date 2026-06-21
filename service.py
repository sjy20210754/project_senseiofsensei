import duckdb
import pandas as pd
import repository as repo

def connect_database(path:str) -> duckdb. DuckDBPyConnection:
    """
    데이터베이스 연결 생성
    """
    return duckdb.connect(path)

def initialize(con: duckdb.DuckDBPyConnection):
    """
    기본 데이터 베이스 저장
    """
    repo.create_table(con)
    count=repo.get_studentversions_count(con)
    if count <=0:
        repo.save_initial_data(con)
    else:
        print(f"학생 버전 데이터 개수 : {count}")

def get_studentlist(con: duckdb.DuckDBPyConnection)->pd.DataFrame:
    """
    전체 학생 조회
    """
    return repo.get_versionlist(con)

def find_student_detail(con: duckdb.DuckDBPyConnection, name:str, version:str)->pd.DataFrame:
    """
    학생 버전의 상세 정보 조회
    """
    return repo.find_version_all_info(con, name, version)

def find_student_terrain_rank(con: duckdb.DuckDBPyConnection, name:str, version:str)->pd.DataFrame:
    """
    학생 버전의 지형 상성 정보 조회
    """
    return repo.find_terrain_rank_by_student_version(con, name, version)

def get_bosslist(con: duckdb.DuckDBPyConnection)->pd.DataFrame:
    """
    전체 보스 조회
    """
    return repo.get_bosslist(con)

def find_boss_hp(con: duckdb.DuckDBPyConnection, name:str)->pd.DataFrame:
    """
    보스 난이도의 체력 조회
    """
    return repo.get_hp_list_by_name(con, name)

def find_counter_of_boss(con: duckdb.DuckDBPyConnection, name:str, defense:str, terrain:str)->pd.DataFrame:
    """
    보스 방어타입에 강한 딜러 학생 조회
    """
    return repo.find_counterversions_by_bossdefensetype(con, name, defense, terrain)


