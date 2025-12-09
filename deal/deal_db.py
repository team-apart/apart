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
            port=3336,
            user='root',
            password='1212',
            db='apart',
            cursorclass=DictCursor
        )
        cursor = con.cursor()
     # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "select gu.guName,dong.dongName from gu inner join dong on gu.guId=dong.guId"
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
            port=3336,
            user='root',
            password='1212',
            db='apart',
            cursorclass=DictCursor
        )
        cursor = con.cursor()
     # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "select dong.dongName,apart.aptName from dong inner join apart on dong.dongId=apart.dongId"


        result = cursor.execute(sql);
        print(result); # insert, update, delete의 결과는 정수값!
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
    return rows
def transform(arr):
    result = []
    for s in arr:
        parts = s.split(" ", 1)   # 앞 단어와 나머지를 분리 (최대 1번만 split)
        result.append([parts[0], s])  # [앞 단어, 전체 문자열] 형태로 추가
    return result



def get_deal(aparts:List[str]):
    arrs=transform(aparts)
    print(arrs)

    try:
        con = mysql.connect(
            host='localhost',
            port=3336,
            user='root',
            password='1212',
            db='apart',
            cursorclass=DictCursor
        )
        cursor = con.cursor()
     # 3. sql문 작성한 후 sql문을 db서버에 보내자.
     #    sql = "select dong.dongName,apart.aptName from dong inner join apart on dong.dongId=apart.dongId"

        sql="""
            SELECT
            deal.guName,
            deal.dongName,
            deal.aptName,
            deal.area,
            YEAR(deal.dealDate) AS year,
            MONTH(deal.dealDate) AS month,
            AVG(ROUND(deal.dealAmount, 1)) AS average
            FROM deal
            WHERE  deal.dongName=%s
                AND deal.aptName=%s
            GROUP BY
                deal.guName,
                deal.dongName,
                deal.aptName,
                deal.area,
                YEAR(deal.dealDate),
                MONTH(deal.dealDate)
                
            ORDER BY
                deal.aptName,
                deal.area,
                YEAR(deal.dealDate) desc,
                MONTH(deal.dealDate) desc
            LIMIT 12
                """

        resultDealInfo=[]
        for arr in arrs:
            result = cursor.execute(sql,arr);
            print(result); # insert, update, delete의 결과는 정수값!
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


# ----------------------------------------------------------
def create(data):
    try :
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(
                            host='localhost',
                            port= 3338,
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