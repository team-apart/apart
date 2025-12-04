// 검색창 요소(.search) 찾기.
const searchEl = document.querySelector('.search');
const searchInputEl = document.querySelector('.input');
const regionEl=document.querySelector('.region')
const select=document.querySelector('.select')
//const table=document.querySelector('table')
//// 검색창 요소를 클릭하면 실행.
searchEl.addEventListener('click', function () {
  searchInputEl.focus();
})

// 검색창 요소 내부 실제 input 요소에 포커스되면 실행.
searchInputEl.addEventListener('focus', function () {
  searchEl.classList.add('focused')
  searchInputEl.setAttribute('placeholder', '구, 동, 아파트명 검색')
})
// 검색창 요소 내부 실제 input 요소에서 포커스가 해제(블러)되면 실행.
searchInputEl.addEventListener('blur', function () {
  searchEl.classList.remove('focused')
  searchInputEl.setAttribute('placeholder', '')
})
const selectedGu=[]
const selectedDong=[]
const dongs=
[
{name:'강남',dong:['신사동','논현동','압구정동','청담동','삼성동','대치동','역삼동','도곡동','개포동','일원동','수서동','세곡동','자곡동','율현동']},
{name:'강동',dong:['강일동','상일동','명일동','고덕동','암사동','천호동','성내동','길동','둔촌동']},
{name:'강북',dong:['미아동','번동','수유동','우이동']},
{name:'강서',dong:['염창동','등촌동','화곡동','내발산동','가양동','마곡동','외발산동','공항동','과해동','오곡동','오쇠동','방화동','개화동']},
{name:'관악',dong:['봉천동','남현동','신림동']},
{name:'광진',dong:['중곡동','능동','구의동','광장동','자양동','화양동','군자동']},
{name:'구로',dong:['신도림동','구로동','가리봉동','고척동','개봉동','오류동',' 천왕동','항동','온수동','궁동']},
{name:'금천',dong:['가산동','독산동','시흥동']},
{name:'노원',dong:['월계동','공릉동','하계동','중계동','상계동']},
{name:'도봉',dong:['쌍문동','방학동','창동','도봉동']},
{name:'동대문',dong:['신설동','용두동','제기동','전농동','답십리동','장안동','청량리동','회기동','휘경동','이문동']},
{name:'동작',dong:['노량진동','본동','상도동','상도1동','흑석동','사당동','대방동','신대방동']},
{name:'마포',dong:['아현동','공덕동','신공덕동','염리동','도화동','마포동','용강동','토정동','대흥동','신수동','노고산동','구수동','현석동','신정동',
'대흥동','창천동','상수동','하중동','당인동','서교동','동교동','합정동','망원동','연남동','성산동','중동','상암동']},
{name:'서대문',dong:['충정로','합동','미근동','북아현동','천연동','냉천동','옥천동','영천동','현저동','대신동','대현동','신촌동',
'봉원동','창천동','연희동','흥제동','홍은동','남가좌동','북가좌동']},
{name:'서초',dong:['서초동','방배동','잠원동','반포동','방배동','양재동','우면동','원지동','내곡동','염곡동','신원동']},
{name:'성동',dong:['상왕십리동','하왕십리동','도선동','홍익동','마장동','사근동','행당동','응봉동','금호동',
'옥수동','성수동','송정동','용답동']},
{name:'성북',dong:['성북동','동소문동','삼선동','돈암동','동선동','안암동','보문동','정릉동','길음동','하월곡동','상월곡동','장위동','석관동']},
{name:'송파',dong:['풍납동','거여동','마천동','방이동','오금동','송파동','석촌동','삼전동','가락동','문정동','장지동','잠실동','신천동']},
{name:'양천',dong:['목동','신월동','신정동']},
{name:'영등포',dong:['당산동','당산동1가','당산동2가','당산동3가','당산동4가','당산동5가','당산동6가','대림동','도림동','문래동2가','문래동3가','문래동4가','문래동5가','문래동6가','신길동','양평동1가','양평동2가','양평동3가','양평동4가','양평동5가','양평동6가','여의도동','영등포동','영등포동1가','영등포동2가','영등포동3가','영등포동4가','영등포동5가','영등포동7가','영등포동8가']},
{name:'용산',dong:['후암동','용산동','갈월동','남영동','동자동','청파동','서계동','원효로','문배동','신계동','신창동','산천동','청암동','효창동','용문동','도원동','한강로1가','한강로2가',
'한강로3가','이촌동','이태원동','한남동','서빙고동','동빙고동','주성동','보광동']},
{name:'은평',dong:['녹번동','불광동','갈현동','구산동','대조동','응암동','역촌동','신사동','증산동','수색동','진관동']},
{name:'종로',dong:['평창동','구기동','무악동','교남동','평동','송월동','홍파동','교북동','행촌동','가희동','재동','계동','원서동','종로','청진동','서린동','수송동','중학동','공평동','관훈동','견지동','권농동','운니동',
'익선동','경운동','관철동','인사동','낙원동','와룡동','훈정동','묘동','봉익동','돈의동','장사동','관수동','인의동','예지동','원남동',
'효제동','연지동','충신동','이화동','연건동','동숭동','혜화동','명륜동','창신동','숭인동']},
{name:'중',dong:['소공동','북창동','태평로2가','남대문로','서소문동','정동','순화동','의주로1가','충정로1가',
'봉래동','회현동','남창동','남대문로','봉래동','충무로',
'순화동','명동','충무로','저동','남산동','태평로','무교동','다동',
'삼각동','남대문로','수하동','장교동','수표동','예장동','회현동','필동','남학동','주자동','장충동','묵정동','광희동','쌍림동',
'을지로','충무로','인현동','예관동',
'오장동','주교동','방산동','임정동','산림동','초동','인현동','저동2가','무학동','흥인동','신당동','황학동','중림동','의주로2가','만리동']},
{name:'중랑',dong:['면목동','상봉동','중화동','묵동','망우동','신내동']}
]

function addRegion(city){
const cities=Object.values(document.querySelectorAll('.'+city+''))


    cities.map(city=>{
    if(!selectedGu.includes(city.value)){
        selectedGu.push(city.value)
        city.checked=true
    }
    else
    {
    selectedGu.splice(selectedGu.indexOf(city.value),1)
    city.checked=false
    }
})
selectedGu.forEach(key=>console.log(key))
}
const tableValues=[]

function selectGU(gu){
//const id=selectedGu.indexOf(gu)
//console.log(id)
if(!selectedGu.includes(gu)){
        selectedGu.push(gu)
    }else{
    selectedGu.splice(selectedGu.indexOf(gu),1)
}


const results=selectedGu.map(gu=>dongs.filter(dong=>dong.name===gu))

results.map(result=>result.map(re=>{tableValues.push(re)}))
//console.log(tableValues)
//select.innerHTML=""
//
//createTable(tableValues)

}
function selectedCommit(){

select.innerHTML=""
createTable(tableValues)
}

function createTable(values){
const table=document.createElement('table')
const tbody=document.createElement('tbody')

const tag=values.map(value=>{
    const tr=document.createElement('tr')
    const td=document.createElement('td')

    const image=document.createElement('img')
    td.style.fontSize="20px"
    td.style.border="2px solid black"
    td.style.height="200px";
    td.style.width="200px";
    td.style.textAlign="center"
    td.innerText=value.name

    image.src="/static/img/mascot/"+value.name+"구.png";
    image.style.width="200px";
    td.append(image)
    tr.append(td)

    const dongname=document.createElement('td')
    dongname.style.verticalAlign="top";
    dongname.style.display="flex";
    dongname.style.justifyContent="flex-start";
    dongname.style.alignItems="flex-start"
    dongname.style.width='800px';
    dongname.style.flexWrap="wrap"

    value.dong.forEach(don=>{
    const div=document.createElement('div');
    div.classList.add('dong')
    div.style.padding="5px 10px";
    div.style.margin="0 5px;"
    div.innerText=don;
    dongname.append(div);
    tr.append(dongname);


    div.addEventListener('click',()=>{
        if(div.classList.contains('selected')){
            div.classList.remove(('selected'))
        }else{
            div.classList.add('selected')
            }
            })
    })
    tbody.append(tr);
    table.append(tbody)
    select.append(table)
    select.classList.add('display')
    })
}
