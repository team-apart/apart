# python에서 db연결하여 crud처리하는 파일(모듈)
# crud기능 4개 넣을 예정

#1. 라이브러리 필요
import pymysql as mysql
from pymysql import IntegrityError
from pymysql.cursors import DictCursor
from typing import List

def get_dongs():
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
        sql = "select SIGUDONG.GU_NM,SIGUDONG.DONG_NM from SIGUDONG "
        result = cursor.execute(sql);
        print(result); # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1 :
            print("동 검색 성공!!! ")
            rows = cursor.fetchall();


        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return rows

def get_apart():
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
        sql = "select SIGUDONG.DONG_NM,APART.APART_NM from SIGUDONG inner join APART on SIGUDONG.DONG_CD=APART.DONG_CD"


        result = cursor.execute(sql);
        # print(result); # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1 :
            print("아파트 검색 성공!!! ")
            rows = cursor.fetchall();

        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    # print('rows',rows)
    return rows



def transform(arr):
    result = []
    for s in arr:
        parts = s.split(" ", 1)   # 앞 단어와 나머지를 분리 (최대 1번만 split)
        result.append([parts[0], s])  # [앞 단어, 전체 문자열] 형태로 추가
    return result



def get_deal(aparts:List[str]):
    arrs=transform(aparts)
    print('[아파트,아파트 네임]',arrs)

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
     #    sql = "select dong.dongName,apart.aptName from dong inner join apart on dong.dongId=apart.dongId"

        sql="""
            SELECT
            SIGUDONG.GU_NM,
            SIGUDONG.DONG_NM,
            APART.APART_NM,
            DEAL.SIZE,
            YEAR(DEAL.CONTRACT_YMD) AS year,
            MONTH(DEAL.CONTRACT_YMD) AS month,
            AVG(ROUND(DEAL.PRICE, 1)) AS average
            FROM DEAL 
            JOIN SIGUDONG ON DEAL.GU_CD=SIGUDONG.GU_CD AND DEAL.DONG_CD=SIGUDONG.DONG_CD
            JOIN APART ON SIGUDONG.GU_CD=APART.GU_CD AND SIGUDONG.DONG_CD=APART.DONG_CD
            WHERE  SIGUDONG.DONG_NM=%s
                AND APART.APART_NM=%s
            GROUP BY
                DEAL.GU_CD,
                DEAL.DONG_CD,
                DEAL.APART_CD,
                DEAL.SIZE,
                YEAR(DEAL.CONTRACT_YMD),
                MONTH(DEAL.CONTRACT_YMD)
                
            ORDER BY
                DEAL.APART_CD,
                DEAL.SIZE,
                YEAR(DEAL.CONTRACT_YMD) desc,
                MONTH(DEAL.CONTRACT_YMD) desc
            LIMIT 12
                """
        # print(sql)
        resultDealInfo=[]
        for arr in arrs:
            print('name',[arr[0],arr[1].replace(arr[0], "")])
            result = cursor.execute(sql,[arr[0],arr[1].replace(arr[0],"").strip()]);
            print('result',result); # insert, update, delete의 결과는 정수값!
            # 실행된 결과의 행수(레코드 개수)
            if result >= 1 :
                print("아파트 검색 성공!!! ")
                rows = cursor.fetchall();
                resultDealInfo.append(rows)

        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    print('resultDealInfo',resultDealInfo)
    return resultDealInfo


def get_deal_apart(apart: str):

    print(apart)

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
                DEAL.GU_CD,
                DEAL.DONG_CD,
                DEAL.APART_CD,
                DEAL.SIZE,
                DEAL.CONTRACT_YM,
                DEAL.CONTRACT_YMD,
                DEAL.average
            FROM (
                SELECT 
                DEAL.GU_CD,
                DEAL.DONG_CD,
                APART.APART_NM,
                DEAL.SIZE,
                YEAR(DEAL.CONTRACT_YMD) AS year,
                MONTH(DEAL.CONTRACT_YMD) AS month,
                AVG(ROUND(DEAL.PRICE, 1)) AS average,
                ROW_NUMBER() OVER (
                PARTITION BY DEAL.APART_CD, DEAL.SIZE
                ORDER BY YEAR(DEAL.CONTRACT_YMD) DESC, MONTH(DEAL.CONTRACT_YMD) DESC
                ) AS rn
            FROM DEAL JOIN APART ON DEAL.APART_CD=APART.APART_CD
            WHERE APART.APART_NM LIKE %s
            GROUP BY DEAL.GU_CD,
             DEAL.DONG_CD,
             DEAL.APART_CD,
             DEAL.SIZE,
             YEAR(DEAL.CONTRACT_YMD),
             MONTH(DEAL.CONTRACT_YMD)
            ) t
            WHERE rn <= 12
            ORDER BY APART_CD, SIZE, YEAR DESC, MONTH DESC;

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

# ----------------------------------------------------------










def create(data):
    try :
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(
                            host='localhost',
                            port= 3307,
                            user='root',
                            password='1212',
                            db='demo_db',
                            cursorclass=DictCursor
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "insert into bbs(title, content, writer) values (%s, %s, %s)";
        result = cursor.execute(sql, data);
        print(result); # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1 :
            print("데이터 입력 성공!!! ")
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력



# read는 하나 검색과 여러개 검색
def read_one(data):
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(
            host='localhost',
            port=3338,
            user='root',
            password='1212',
            db='demo_db',
            cursorclass=DictCursor
        )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "select * from bbs where no = %s";
        result = cursor.execute(sql, data);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 검색 성공!!! ")
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        row = cursor.fetchone();
        print("검색결과 row");
        print(row)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return row

def read_all():
    try:
        #2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(
            port=3338,
            user='root',
            password='1212',
            db='demo_db',
            cursorclass=DictCursor
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "select * from bbs ";

        result = cursor.execute(sql);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 검색 성공!!! ")
        rows = cursor.fetchall(); #전체 목록 다
        # rows = cursor.fetchmany(2); #전체 목록 중 2개만
        for row in rows:
            print('row',row)
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return rows;

def read_search(q):
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(
            host='localhost',
            port=3338,
            user='root',
            password='1212',
            db='demo_db',
            cursorclass=DictCursor
        )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "SELECT * FROM bbs WHERE title LIKE %s"

        result = cursor.execute(sql, ('%' + q + '%',))
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 검색 성공!!! ")
        rows = cursor.fetchall(); #전체 목록 다
        # rows = cursor.fetchmany(2); #전체 목록 중 2개만
        for row in rows:
            print(row)
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력

    return rows;

def update(data):
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(
            host='localhost',
            port=3338,
            user='root',
            password='1212',
            db='demo_db',
            cursorclass=DictCursor
        )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "update bbs set title = %s, content = %s where no = %s";
        result = cursor.execute(sql, data);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 수정 성공!!! ")
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력

def delete(data):
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(
            host='localhost',
            port=3338,
            user='root',
            password='1212',
            db='demo_db',
            cursorclass=DictCursor
        )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "delete from bbs where no = %s";
        result = cursor.execute(sql, data);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 삭제 성공!!! ")
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력

# if __name__ == '__main__':
#     create()