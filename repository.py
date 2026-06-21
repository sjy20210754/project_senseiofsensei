import duckdb
import pandas as pd

#-------------------------------------------------------------------------------
# region : DuckDB DDL & 기본 데이터 생성
#-------------------------------------------------------------------------------
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
            attack VARCHAR NOT NULL,
            image_path VARCHAR NOT NULL
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
            image_path VARCHAR NOT NULL,
            memory_image_path VARCHAR NOT NULL,
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
        COPY boss FROM 'data/boss.csv' (HEADER, DELIMITER ', ');
        -- 지형
        COPY terrain FROM 'data/terrain.csv' (HEADER, DELIMITER ', ');
        -- 학생 프로필
        COPY student FROM 'data/student.csv' (HEADER, DELIMITER ', ');
        -- 보스 지형
        COPY boss_stage FROM 'data/boss_stage.csv' (HEADER, DELIMITER ', ');
        -- 보스 방어 타입
        COPY defense_type FROM 'data/defense_type.csv' (HEADER, DELIMITER ', ');
        -- 보스 난이도
        COPY difficulty FROM 'data/difficulty.csv' (HEADER, DELIMITER ', ');
        -- 학생 버전
        COPY version FROM 'data/version.csv' (HEADER, DELIMITER ', ');
        -- 지형 랭크
        COPY terrain_rank FROM 'data/terrain_rank.csv' (HEADER, DELIMITER ', ');
    """
    con.execute(query)
    print('기본 데이터 저장 완료')

#-------------------------------------------------------------------------------
# region : version (학생 버전)
#-------------------------------------------------------------------------------
def get_studentversions_count(con:duckdb.DuckDBPyConnection)->int:
    """
    학생 버전(version) 개수 반환
    """
    return con.execute("SELECT COUNT(*) FROM version").fetchone()[0]

def get_versionlist(con:duckdb.DuckDBPyConnection)->pd.DataFrame:
    """
    뷰의 학생 버전(version) 리스트 반환
    """
    return con.execute("SELECT name, version, attack, defense, image_path FROM version").df()

#-------------------------------------------------------------------------------
# region : terrain_rank (학생 지역 상성)
#-------------------------------------------------------------------------------
def find_terrain_rank_by_student_version(con:duckdb.DuckDBPyConnection, name:str, version:str)->pd.DataFrame:
    """
    학생 버전의 지역별 상성 반환
    """
    return con.execute("""SELECT rank 
                       FROM terrain_rank t 
                       WHERE t.name=? AND t.version=?""",[name,version]).df()

#-------------------------------------------------------------------------------
# region : difficulty (보스 난이도)
#-------------------------------------------------------------------------------
def get_hp_list_by_name(con:duckdb.DuckDBPyConnection, name:str)->pd.DataFrame:
    """
    보스 난이도 별 체력 반환
    """
    return con.execute("""SELECT difficulty, hp 
                       FROM difficulty d
                       WHERE d.name=?
                       ORDER BY d.hp""",[name]).df()

#-------------------------------------------------------------------------------
# region : join
#-------------------------------------------------------------------------------
def find_counterversions_by_bossdefensetype(con: duckdb.DuckDBPyConnection, name:str, defense:str, terrain:str)->pd.DataFrame:
    """
    JOIN defense_type, version, terrain_rank
    보스 방어타입에 강한 딜러 학생 버전 리스트 반환
    """
    query="""
        SELECT
            v.name,
            v.version
        FROM defense_type d
        JOIN version v ON d.weakattack = v.attack
        JOIN terrain_rank t ON (v.name=t.name AND v.version=t.version)
        WHERE d.name=? AND d.defense=? AND t.terrain=? AND v.combat_class='STRIKER' AND v.role='딜러' AND (t.rank='S' OR t.rank='A')
    """
    return con.execute(query,[name,defense,terrain]).df()

def get_bosslist(con: duckdb.DuckDBPyConnection)->pd.DataFrame:
    """
    JOIN defense_type, boss, boss_stage
    보스 종류, 방어타입, 지형에 따른 보스 리스트
    """
    query="""
        SELECT
            d.name,
            d.defense,
            b.attack,
            s.terrain,
            b.image_path
        FROM defense_type d
        JOIN boss b ON d.name=b.name
        JOIN boss_stage s ON b.name=s.name
        ORDER BY d.name, s.terrain ASC
    """
    return con.execute(query).df()

def find_version_all_info(con: duckdb.DuckDBPyConnection, name:str, version:str)->pd.DataFrame:
    """
    JOIN student, version, terrain_rank
    학생 버전(version)의 상세 정보(이름, 학교, 동아리, 공격타입, 방어타입, 스킬 등)
    """
    query="""
        SELECT
            s.name,
            s.fullname,
            s.school,
            s.club,
            v.version,
            v.attack,
            v.defense,
            v.combat_class,
            v.role,
            v.position,
            v.ex_skill,
            v.cost,
            v.normal_skill,
            v.passive_skill,
            v.sub_skill,
            v.memory_image_path,
            t.terrain,
            t.rank
        FROM student s
        JOIN version v ON s.name=v.name
        JOIN terrain_rank t ON (v.name=t.name AND v.version=t.version)
        WHERE s.name=? AND v.version=?
        ORDER BY t.terrain ASC
    """
    return con.execute(query,[name, version]).df()

