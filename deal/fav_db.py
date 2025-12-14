# python에서 db연결하여 crud처리하는 파일(모듈)
# crud기능 4개 넣을 예정

#1. 라이브러리 필요
import pymysql as mysql
from pymysql import IntegrityError
from pymysql.cursors import DictCursor
from typing import List

def write_fav(favorite:str):
    print(favorite)
    try:
        con = mysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='1234',
            db='apart2',
            cursorclass=DictCursor
        )
        cursor = con.cursor()
     # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "INSERT INTO FAVORITE (FAVORITE)VALUES(%s)"
        result = cursor.execute(sql,(favorite,));
        print(result); # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1 :
            print("FAV 입력 성공!!! ")
            # rows = cursor.fetchall();


        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return result

def remove_fav(favorite:str):
    print(favorite)
    try:
        con = mysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='1234',
            db='apart2',
            cursorclass=DictCursor
        )
        cursor = con.cursor()
     # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "DELETE FROM FAVORITE WHERE FAVORITE=%s"
        result = cursor.execute(sql,favorite);
        print(result); # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1 :
            print("FAV 입력 성공!!! ")
            # rows = cursor.fetchall();


        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return result

def get_fav():
    try:
        con = mysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='1234',
            db='apart2',
            cursorclass=DictCursor
        )
        cursor = con.cursor()
        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql ="""
        SELECT 
            DEAL.ID,
            SIGUDONG.GU_NM,
            SIGUDONG.DONG_NM,
            APART.APART_NM,
            FLOOR(DEAL.SIZE) AS SIZE,
            YEAR(DEAL.CONTRACT_YMD) AS year,
            MONTH(DEAL.CONTRACT_YMD) AS month,
            AVG(ROUND(DEAL.PRICE, 1)) AS average,
            FAVORITE.FAVORITE
        FROM DEAL 
            join favorite on favorite.favorite=deal.id
            join apart on apart.APART_CD=deal.apart_cd
            join sigudong on sigudong.DONG_CD=deal.DONG_CD
        GROUP BY
            DEAL.ID,
            SIGUDONG.GU_NM,
            SIGUDONG.DONG_NM,
            APART.APART_NM,
            DEAL.SIZE,
           DEAL.CONTRACT_YMD,
            DEAL.CONTRACT_YMD,
            DEAL.PRICE, 1,
            FAVORITE.FAVORITE
        """
        result = cursor.execute(sql,);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("FAV GET 성공!!! ")
            rows = cursor.fetchall();

        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return rows
# -----------------------------------------------------------------------------
