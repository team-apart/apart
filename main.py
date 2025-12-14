from fastapi import FastAPI, Form,Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict
from typing import List, Dict, Any

from websockets.sync.client import connect_socks_proxy

from db import deal_db as db
from db import fav_db as fav_db
from db import search_db as search_db
from db import learn_db as learn_db
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
@app.get("/")
def page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get('/getDongs')
def get_dongs():
    data=db.get_dongs();
    result_dict=defaultdict(list)
    for item in data:
        result_dict[item["GU_NM"]].append(item["DONG_NM"])
    result=[{"name":guName,"dong":dongName} for guName,dongName in result_dict.items()]
    return result

@app.get('/getApart')
def get_Apart():
    data=db.get_apart();
    result_dict=defaultdict(list)
    for item in data:
        result_dict[item["DONG_NM"]].append(item["APART_NM"])
    result=[{"name":DONG_NM,"apart": [DONG_NM + " " + apt for apt in APART_NM]}
    for DONG_NM,APART_NM in result_dict.items()]
    # print('result18',result)
    return result

def group_deals(raw: List[Any]) -> List[Dict[str, Any]]:
    # print('raw',raw)
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
        id=r.get('ID')
        dong = r.get("DONG_NM")
        apt = r.get("APART_NM")
        area = r.get("SIZE")
        fav=r.get("FAVORITE")

        key = (dong, apt, area)

        if key not in grouped:
            grouped[key] = {
                "id":id,
                "dong": dong,
                "apart": apt,
                "area": area,
                "fav":fav,
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
    # print('payload',payload)
    data=db.get_deal(payload)
    # print('data',data)
    result=group_deals(data)
    # print('result=',result)
    return result

@app.post('/quick')
async def get_Deal_apart(payload: str=Body(...)):
    # print(payload)
    data=search_db.get_deal_apart(payload)
    result=group_deals(data)
    return result



@app.post('/favorite')
async def save_fav(favorite:str=Body(...)):
    print('favorite',favorite)
    data=fav_db.write_fav(favorite)
    return data

@app.post('/favorite_del')
async def save_fav(favorite:str=Body(...)):
    # print('favorite',favorite)
    data=fav_db.remove_fav(favorite)
    return data


@app.get('/getFavorite')
async def get_fav():
    favorite=fav_db.get_fav()
    # print('favorite',favorite)
    # result = group_deals(favorite)
    # # print('result=',result)
    return favorite
# ---------------------------------------------------------------











