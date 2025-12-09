from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
from typing import List, Dict, Any

from deal import deal_db as db
import chart_db as ch

# FastAPI 앱 인스턴스 생성
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000","http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 정적 파일 제공 (CSS/JS/이미지)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 로더 (templates 디렉터리 지정)
templates = Jinja2Templates(directory="templates")


# 기본 루트 엔드포인트
#@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}


@app.get('/getDongs')
def get_dongs():
    data=db.get_dongs();
    result_dict=defaultdict(list)
    for item in data:
        result_dict[item["guName"]].append(item["dongName"])
    result=[{"name":guName,"dong":dongName} for guName,dongName in result_dict.items()]
    return result

@app.get('/getApart')
def get_Apart():
    data=db.get_apart();
    result_dict=defaultdict(list)
    for item in data:
        result_dict[item["dongName"]].append(item["aptName"])
    result=[{"name":dongName,"apart":aptName} for dongName,aptName in result_dict.items()]
    return result
def group_deals(raw: List[Any]) -> List[Dict[str, Any]]:
    """
    raw: 입력이 [{...}, ...] 또는 [[{...}, ...], [{...}, ...], ...] 같은 1~2차원 리스트일 수 있음.
    반환: [{'dong':..., 'apart':..., 'area':..., 'deals':[{'year':..., 'month':..., 'avg': Decimal(...)}, ...]}, ...]
    """
    # 1) 입력 평탄화: raw 내부에 리스트가 있으면 모두 꺼내서 rows에 담음
    rows = []
    for item in raw:
        if isinstance(item, list):
            rows.extend(item)
        else:
            rows.append(item)

    # 2) 그룹화: (dongName, aptName, area)를 키로 묶음
    grouped = {}
    for r in rows:
        dong = r.get("dongName")
        apt = r.get("aptName")
        area = r.get("area")

        key = (dong, apt, area)

        if key not in grouped:
            grouped[key] = {
                "dong": dong,
                "apart": apt,
                "area": area,
                "deals": []
            }

        grouped[key]["deals"].append({
            "year": r.get("year"),
            "month": r.get("month"),
            "avg": r.get("average")  # Decimal 타입 그대로 보관
        })

    # 3) dict -> list 반환
    return list(grouped.values())



@app.post('/getDeals')
async def get_Deal(payload: List[str]):
    # print(payload)
    # data=request.selectedApartr
    # print('dealData',list(data))
    data=db.get_deal(payload)

    result=group_deals(data)
    print('result=',result)
    return result
    # print(data)
    # result_dict=defaultdict(list)
    # for item in data:
    #     result_dict[item["dongName"]].append(item["aptName"])
    # result=[{"name":dongName,"apart":aptName} for dongName,aptName in result_dict.items()]

    # return result


# 경로 파라미터 예시
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


# POST 요청 예시
# @app.post("/users/")
@app.get("/users/{user_id}/{user_name}/{user_age}")
def create_user(user_id: str, user_name: str, user_age: int):
    user = {
        "user_id": user_id,
        "user_name": user_name,
        "user_age": user_age
    }
    return {"user_created": user}


@app.get("/raw")
def raw_html():
    html = """
    <h>
    <head>
     <link rel="stylesheet" href="/static/css/main.css">
    </head>
      <body>
        <h1>Hello</h1>
        <p>템플릿 없이 직접 HTML</p>
      </body>
    </h                                                                      tml>
    """
    return HTMLResponse(content=html)


@app.get("/")
def page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/page")
def page2(request: Request):
    return templates.TemplateResponse(
        "page.html",
        {"request": request, "title": "템플릿 페이지", "items": ["사과", "배", "포도"]}
    )


@app.get("/page2/{item_id}")
def page3(request: Request, item_id: str):
    print("----", request.query_params)
    print(request.headers)
    data = {"request": request,
            "title": "템플릿에 값 넣기",
            "item_id": item_id}
    return templates.TemplateResponse("page2.html", data)


# http://127.0.0.1:8000/page2?item_id=root
@app.get("/page2")
def page4(request: Request):
    print("----", request.query_params)  # ---- item_id=root
    print(request.headers)
    data = {"request": request,
            "title": "템플릿에 값 넣기",
            "item_id": request.query_params["item_id"]}
    return templates.TemplateResponse("page2.html", data)


@app.get("/bbs")
def bbs(request: Request):
    return templates.TemplateResponse("bbs.html", {"request": request})


@app.get("/bbs/bbs_list")
def bbs_list(request: Request):
    rows = db.read_all();
    print("router --------")
    print(rows)
    print("router --------")
    data = {
        "request": request,
        "rows": rows
    }
    return templates.TemplateResponse("bbs_list.html", data)

@app.get("/bbs/bbs_read/{no}")
def bbs_one(request: Request, no: int ):
    row = db.read_one(no)
    print("router --------")
    print(row)
    print("router --------")
    data = {
        "request": request,
        "row": row
    }
    return templates.TemplateResponse("bbs_read.html", data)

@app.get("/bbs/bbs_search")
def bbs_list(request: Request, q: str ):
    rows = db.read_search(q);
    print("router --------")
    print(rows)
    print("router --------")
    data = {
        "request": request,
        "rows": rows
    }
    return templates.TemplateResponse("bbs_list.html", data)

# get : 게시판 쓸 수 있는 화면은 get요청으로!
@app.get("/bbs/bbs_insert")
def bbs_page(request: Request):
    return templates.TemplateResponse("bbs_insert.html", {"request": request})


# post : 게시판 쓴 내용을 db처리해달라고 요청하는 경우는 Post요청으로!
@app.post("/bbs/bbs_insert")
def bbs(request: Request,
        title: str = Form(...),
        content: str = Form(...),
        writer: str = Form(...)):
    db.create([title, content, writer]);
    return RedirectResponse(url="/bbs/bbs_list", status_code=303)
    # 303 get요청, 302는 post/set, 307/308은 메서드 유지


@app.get("/bbs/bbs_update/{no}")
def bbs_update_page(request: Request, no: int):
    row = db.read_one(no)
    return templates.TemplateResponse("bbs_update.html", {"request": request, "row": row})


@app.post("/bbs/bbs_update")
def bbs_update(request: Request,
        no : str = Form(...),
        title: str = Form(...),
        content: str = Form(...)
        ):
    db.update([title, content, no]);
    return RedirectResponse(url="/bbs/bbs_list", status_code=303)


@app.post("/bbs/bbs_delete/{no}")
def bbs_delete(request: Request, no : int):
    db.delete(no)
    return RedirectResponse(url="/bbs/bbs_list", status_code=303)


@app.get("/chart")
def chart(request: Request):
    return templates.TemplateResponse("chart.html", {"request": request})

@app.get("/chart/count")
def chart_count(request: Request):
    count = ch.read_count()
    print("router --------")
    print(count)
    return count;

@app.get("/chart/avg")
def chart_avg(request: Request):
    avg = ch.read_avg()
    print("router --------")
    print(avg)
    data = {"avg": avg}
    return data;

@app.get("/chart/all")
def chart_all(request: Request):
    all = ch.read_all()
    print("router --------")
    print(all)
    data = {"all": all}
    return data;



