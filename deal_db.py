import pymysql as mysql
from pymysql import IntegrityError
from pymysql.cursors import DictCursor


def deal_count():
    print("deal count")
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port=3338,
                            user='root',
                            password='1212',
                            db='deal_db',
                            cursorclass=DictCursor
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = """
                select count(dealdate) as count
                from dealapart;

              """;

        result = cursor.execute(sql);
        print(result);  # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1:
            print("데이터 검색 성공!!! ")
        row = cursor.fetchone();  # 전체 목록 다
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력
    return row;