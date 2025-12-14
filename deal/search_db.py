# python에서 db연결하여 crud처리하는 파일(모듈)
# crud기능 4개 넣을 예정

#1. 라이브러리 필요
import pymysql as mysql
from pymysql import IntegrityError
from pymysql.cursors import DictCursor
from typing import List

def get_deal_apart(apart: str):

    print('apart',apart)

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

        sql="""
           SELECT  
    t.ID,
    t.GU_NM,
    t.DONG_NM,
    t.APART_NM,
    FLOOR(t.SIZE) AS SIZE,
    t.year,
    t.month,
    t.average
FROM (
    SELECT 
        DEAL.ID,
        SIGUDONG.GU_NM,
        SIGUDONG.DONG_NM,
        APART.APART_NM,
        DEAL.APART_CD,
        DEAL.SIZE,
        YEAR(DEAL.CONTRACT_YMD) AS year,
        MONTH(DEAL.CONTRACT_YMD) AS month,
        AVG(ROUND(DEAL.PRICE, 1)) AS average,
        ROW_NUMBER() OVER (
            PARTITION BY DEAL.APART_CD, DEAL.SIZE
            ORDER BY YEAR(DEAL.CONTRACT_YMD) DESC, MONTH(DEAL.CONTRACT_YMD) DESC
        ) AS rn
    FROM DEAL 
    JOIN APART ON DEAL.APART_CD = APART.APART_CD
    JOIN SIGUDONG ON SIGUDONG.DONG_CD = DEAL.DONG_CD
    WHERE APART.APART_NM LIKE %s
    GROUP BY 
        DEAL.ID,
        SIGUDONG.GU_NM,
        SIGUDONG.DONG_NM,
        APART.APART_NM,
        DEAL.APART_CD,
        DEAL.SIZE,
        YEAR(DEAL.CONTRACT_YMD),
        MONTH(DEAL.CONTRACT_YMD)
) t
WHERE t.rn <= 12
ORDER BY t.APART_NM, t.SIZE, t.year DESC, t.month DESC;



        """

        result = cursor.execute(sql, ("%"+apart));
        # print(result) # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("아파트 검색 성공!!! ")
            rows = cursor.fetchall();


        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    # print('resultDealInfo', rows)
    return rows
# -----------------------------------------------------------------------------
