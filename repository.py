import duckdb
import pandas as pd

def create_table(con: duckdb.DuckDBPyConnection):
    """
    DuckDB 테이블 생성
    """
    print('DuckDB 테이블 생성 시작')
    query="""
        -- 보스 프로필
        CREATE TABLE IF NOT EXISTS boss
        (
            name VARCHAR NOT NULL PRIMARY KEY,
            attack VARCHAR NOT NULL
        );
        -- 지형
        CREATE TABLE IF NOT EXISTS terrain
        (
            terrain VARCHAR NOT NULL PRIMARY KEY
        );
        -- 학생 프로필
        CREATE TABLE IF NOT EXISTS student
        (
            name VARCHAR NOT NULL PRIMARY KEY,
            fullname VARCHAR NOT NULL,
            school VARCHAR NOT NULL,
            club VARCHAR NOT NULL
        );
        -- 편성 부대
        CREATE TABLE IF NOT EXISTS squad
        (
            title VARCHAR NOT NULL PRIMARY KEY,
            boss VARCHAR NOT NULL,
        );
        -- 보스 지형
        CREATE TABLE IF NOT EXISTS boss_stage
        (
            name VARCHAR NOT NULL,
            terrain VARCHAR NOT NULL,
            PRIMARY KEY (name, terrain),
            FOREIGN KEY (name) REFERENCES boss (name),
            FOREIGN KEY (terrain) REFERENCES terrain (terrain)
        );
        -- 보스 방어 타입
        CREATE TABLE IF NOT EXISTS defense_type
        (
            name VARCHAR NOT NULL,
            defense VARCHAR NOT NULL,
            weakattack VARCHAR NOT NULL,
            PRIMARY KEY (name, defense),
            FOREIGN KEY (name) REFERENCES boss (name)
        );
        -- 보스 난이도
        CREATE TABLE IF NOT EXISTS difficulty
        (
            name VARCHAR NOT NULL,
            difficulty VARCHAR NOT NULL,
            hp BIGINT NOT NULL,
            PRIMARY KEY (name, difficulty),
            FOREIGN KEY (name) REFERENCES boss (name)
        );
        -- 학생 버전
        CREATE TABLE IF NOT EXISTS version
        (
            name VARCHAR NOT NULL,
            version VARCHAR NOT NULL,
            attack VARCHAR NOT NULL,
            defense VARCHAR NOT NULL,
            combat_class VARCHAR NOT NULL,
            role VARCHAR NOT NULL,
            position VARCHAR NOT NULL,
            ex_skill VARCHAR NOT NULL,
            cost INT NOT NULL,
            normal_skill VARCHAR NOT NULL,
            passive_skill VARCHAR NOT NULL,
            sub_skill VARCHAR NOT NULL,
            PRIMARY KEY (name, version),
            FOREIGN KEY (name) REFERENCES student (name)
        );
        -- 지형 랭크
        CREATE TABLE IF NOT EXISTS terrain_rank
        (
            name VARCHAR NOT NULL,
            version VARCHAR NOT NULL,
            terrain VARCHAR NOT NULL,
            rank VARCHAR NOT NULL,
            PRIMARY KEY (name, version, terrain),
            FOREIGN KEY (name, version) REFERENCES version (name, version),
            FOREIGN KEY (terrain) REFERENCES terrain (terrain)
        );
        -- 편성 멤버
        CREATE TABLE IF NOT EXISTS member
        (
            name VARCHAR NOT NULL,
            version VARCHAR NOT NULL,
            title VARCHAR NOT NULL,
            slot INT NOT NULL,
            PRIMARY KEY (name, version, title),
            FOREIGN KEY (name, version) REFERENCES version (name, version),
            FOREIGN KEY (title) REFERENCES squad (title)
        );
    """
    con.execute(query)
    print('DuckDB 테이블 생성 완료')

def save_initial_data(con: duckdb.DuckDBPyConnection):
    """
    기본 데이터 저장
    """
    print('기본 데이터 저장')
    query="""
        -- 보스 프로필
        COPY boss FROM 'data/boss.csv' (HEADER, DELIMITER ',');
        -- 지형
        COPY terrain FROM 'data/terrain.csv' (HEADER, DELIMITER ',');
        -- 학생 프로필
        COPY student FROM 'data/student.csv' (HEADER, DELIMITER ',');
        -- 편성 부대
        
        -- 보스 지형
        COPY boss_stage FROM 'data/boss_stage.csv' (HEADER, DELIMITER ',');
        -- 보스 방어 타입
        COPY defense_type FROM 'data/defense_type.csv' (HEADER, DELIMITER ',');
        -- 보스 난이도
        COPY difficulty FROM 'data/difficulty.csv' (HEADER, DELIMITER ',');
        -- 학생 버전
        COPY version FROM 'data/version.csv' (HEADER, DELIMITER ',');
        -- 지형 랭크
        COPY terrain_rank FROM 'data/terrain_rank.csv' (HEADER, DELIMITER ',');
        -- 편성 멤버

    """
    con.execute(query)
    print('기본 데이터 저장 완료')

def get_studentversions_count(con:duckdb.DuckDBPyConnection)->int:
    """
    학생 버전(version) 개수 반환
    """
    return con.execute("SELECT COUNT(*) FROM version").fetchone()[0]

