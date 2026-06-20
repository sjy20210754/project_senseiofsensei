import duckdb
import pandas as pd
import repository as repo

def connect_database(path:str) -> duckdb. DuckDBPyConnection:
    """
    데이터베이스 연결 생성
    """
    return duckdb.connect(path)

def initialize(con: duckdb.DuckDBPyConnection):
    repo.create_table(con)
    count=repo.get_studentversions_count(con)
    if count <=0:
        repo.save_initial_data(con)
    else:
        print(f"학생 버전 데이터 개수 : {count}")