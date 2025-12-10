
// 검색창 요소(.search) 찾기.
const searchEl = document.querySelector('.search');
const searchInputEl = document.querySelector('.input');
const regionEl=document.querySelector('.region')

const selectDong=document.querySelector('.selectDong')
const dongTable=document.querySelector('.dongTable')
const dongTbody=dongTable.querySelector('.dongTbody')

const selectApart=document.querySelector('.selectApart')
const apartTable=document.querySelector('.apartTable')
const apartTbody=apartTable.querySelector('.apartTbody')

const selectDeal=document.querySelector('.selectDeal')
const dealTable=document.querySelector('.dealTable')
const dealTbody=dealTable.querySelector('.dealTbody')

const goNext=document.querySelector('.goNext')

const left=goNext.querySelector('.leftArrow')
const leftBtn=left.querySelector('img')
leftBtn.style.display="none"
const right=goNext.querySelector('.rightArrow')
const rightBtn=right.querySelector('img')
const status=document.querySelector('.status')
leftBtn.style.display="none"
rightBtn.style.display="none"
//const table=document.querySelector('table')
//// 검색창 요소를 클릭하면 실행.
searchEl.addEventListener('click', function () {
  searchInputEl.focus();
})

// 검색창 요소 내부 실제 input 요소에 포커스되면 실행.
searchInputEl.addEventListener('focus', function () {
  searchEl.classList.add('focused')
  searchInputEl.setAttribute('placeholder', '아파트명을 입력하세요')
})
// 검색창 요소 내부 실제 input 요소에서 포커스가 해제(블러)되면 실행.
searchInputEl.addEventListener('blur', function () {
  searchEl.classList.remove('focused')
  searchInputEl.setAttribute('placeholder', '')
})
searchInputEl.addEventListener('change', async function (e) {
    const result=await axios.post('http://localhost:8000/quick',this.value)


    createDealTable(result.data)
    searchInputEl.value=""

})


leftBtn.addEventListener('click',function(){
if(status.innerHTML>0 && status.innerHTML<=1){
    leftBtn.style.display="none"
    rightBtn.style.display="none"

    selectDong.classList.remove('display')
}
if(status.innerHTML>1 && status.innerHTML<=2){
    selectDong.classList.add('display')
    selectApart.classList.remove('display')
    selectDeal.classList.remove('display')
    if(selectedDong.length>=1){
        rightBtn.style.display="block"
        }
    }
if(status.innerHTML>2 && status.innerHTML<=3){
selectApart.classList.add('display')
selectDeal.classList.remove('display')
if(selectedDong.length>=1){
        rightBtn.style.display="block"
        }
}

if(status.innerHTML>0)status.innerHTML-=1
if(status.innerHTML<1) {
    selectApart.classList.remove('display')
}

})
rightBtn.addEventListener('click',function(){
    if(status.innerHTML<3)status.innerHTML=1+parseInt(status.innerHTML)
    if(status.innerHTML>0 && status.innerHTML<=1){
        selectDong.classList.add('display')
        rightBtn.style.display="none"

    }
    if(status.innerHTML>1 && status.innerHTML<=2){
     rightBtn.style.display="none"
        selectedApartCommit()

    }
    if(status.innerHTML>2 && status.innerHTML<=3){
     rightBtn.style.display="none"
        selectedDealCommit()
        selectApart.classList.remove('display')

    }



})
const selectedGu=[]
const selectedDong=[]
const selectedApart=[]


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
})}

function selectGU(gu){
if(!selectedGu.includes(gu)){
    selectedGu.push(gu)
    }else{
    selectedGu.splice(selectedGu.indexOf(gu),1)
}}

function selectDONG(dong){

if(!selectedDong.includes(dong)){
    selectedDong.push(dong)
    }else{
    selectedDong.splice(selectedDong.indexOf(dong),1)
    }

}
function selectAPT(apt){
    if(!selectedApart.includes(apt)){
        selectedApart.push(apt)

    }else{
        selectedGu.splice(selectedApart.indexOf(apt),1)
}}
async function selectedDongCommit(){
    status.innerText=1
    const tableValues=[];
    dongTbody.innerHTML="";
    leftBtn.style.display="block"




try{
    const dongs=await axios.get('http://localhost:8000/getDongs')
    const results=selectedGu.map(gu=>dongs.data.filter(dong=>dong.name===gu))
    results.forEach(result=>result.forEach(re=>{tableValues.push(re)}))
    createDongTable(tableValues)
}catch(e){console.error(e)}
}

function createDongTable(values){
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
    image.src="/static/img/mascot/"+value.name+".png";
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
            selectedDong.splice(selectedDong.indexOf(don),1)

        }else{
            div.classList.add('selected')
            selectDONG(don)
            }
            if(selectedDong.length>=1){
            rightBtn.style.display="block"
            }else{
            rightBtn.style.display="none"
            }
            })
    })


    dongTbody.append(tr);
    dongTable.append(dongTbody)
    selectDong.append(dongTable)
    selectDong.classList.add('display')
    selectApart.classList.remove('display')
    })
}


async function selectedApartCommit(){
    // status.innerText=2
    const tableValues=[];
    apartTbody.innerHTML="";
    console.log('selectedDong',selectedDong)
try{
    const aparts=await axios.get('http://localhost:8000/getApart')
    console.log('aparts',aparts)
    const results=selectedDong.map(dong=>aparts.data.filter(apart=>apart.name===dong))


    console.log('results',results)
    results.forEach(result=>result.forEach(re=>{tableValues.push(re)}))
    createApartTable(tableValues)
}catch(e){console.error(e)}
}
function createApartTable(values){
    console.log('values',values)
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
//    image.src="/static/img/mascot/"+value.name+".png";
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
    value.apart.forEach(apt=>{
    const div=document.createElement('div');
    div.classList.add('dong')
    div.style.padding="5px 10px";
    div.style.margin="0 5px;"
    div.innerText=apt.replace(value.name,"");
    dongname.append(div);
    tr.append(dongname);
    div.addEventListener('click',()=>{
        if(div.classList.contains('selected')){
            div.classList.remove(('selected'))
            selectedApart.splice(selectedDong.indexOf(apt),1)
        }else{
            div.classList.add('selected')
            selectAPT(apt)
            }
            if(selectedApart.length>=1){
            rightBtn.style.display="block"
            }else{
            rightBtn.style.display="none"
            }
            })
    })

    apartTbody.append(tr);
    apartTable.append(apartTbody)
    selectApart.append(apartTable)




    selectDong.classList.remove('display')
    selectApart.classList.add('display')
    })
}

async function selectedDealCommit(){
    // status.innerText=2
    const tableValues=[];
    dealTbody.innerHTML="";

try{

    const deals=await axios.post('http://localhost:8000/getDeals',selectedApart)
    totaldeals=deals['data']
//    const results=selectedApart.map(apt=>deals.data.filter(deal=>deal.aptName.replace(deal.dongName,"")===apt))
//
//
//    console.log('results',results)
//    results.forEach(result=>result.forEach(re=>{tableValues.push(re)}))
//    console('tableValues',tableValues)
    createDealTable(totaldeals)
}catch(e){console.error(e)}
}
//------------------------------------------------------------------------------
function createDealTable(values){
    console.log('values',values)
    const tag=values.map(value=>{
    const tr=document.createElement('tr')
    tr.style.display="flex";
    tr.style.alignItems="flex-end";

    const td=document.createElement('td')
    const image=document.createElement('img')
    td.style.fontSize="20px"
    td.style.border="2px solid black"
    td.style.height="200px";
    td.style.width="200px";
    td.style.textAlign="center";

//    td///////////////////////////////////////동 입력
    p=document.createElement('p')
    p.innerText=value.apart.replace(value.dong,"")
    td.append(p)
    p=document.createElement('p')
    p.innerText=value.area+"평형"
    td.append(p)
//    image.src="/static/img/mascot/"+value.name+".png";
    image.style.width="200px";
    td.append(image)
    tr.append(td)


    const dealInfo=document.createElement('td')//////그래프 div
    dealInfo.style.verticalAlign="top";
    dealInfo.style.display="flex";
    dealInfo.style.justifyContent="flex-start";
    dealInfo.style.alignItems="flex-end"
    dealInfo.style.width='1000px';
    dealInfo.style.flexWrap="wrap"
//    dealInfo.style.background="green"
//    dealInfo.style.lineHeight="1.2";
//    dealInfo.innerText='aaa'
    value.deals.sort((a, b) => {
      if (a.year === b.year) {
        return a.month - b.month; // 같은 year일 때 month 비교
      }
      return a.year - b.year; // year 먼저 비교
    });

const maxValue = value.deals.reduce((max, item) => item.avg > max ? item.avg : max, -Infinity);
const minValue = value.deals.reduce((min, item) => item.avg < min ? item.avg : min, -Infinity);





    value.deals.forEach(deal=>{

    bar=document.createElement('div');
    bar.style.marginLeft="10px";
    bar.style.background="blue";
    if((maxValue/1000)<100) {
        bar.style.height=(deal.avg/1000+80).toString()+"px"
    }else if((maxValue/1000)>200){
        bar.style.height=(deal.avg/1000-100).toString()+"px"
    }else if((maxValue/1000)>170){
        bar.style.height=(deal.avg/1000-70).toString()+"px"
    }else if((minValue/1000)<80){
        bar.style.height=(deal.avg/1000+60).toString()+"px"
    }else if((minValue/1000)<110){
        bar.style.height=(deal.avg/1000+30).toString()+"px"
    }else
    {
        bar.style.height=(deal.avg/1000).toString()+"px"
    }


    bar.style.width="50px"
    bar.style.display="flex"
    bar.style.flexDirection="column"
    bar.style.alignItems="center"
    bar.style.justifyContent="space-between"
    bar.style.color="white"
    value=document.createElement('div')

    value.style.fontSize="1.2rem"
    value.style.color="red"
    value.style.fontWeight="bold"
    value.innerText=parseFloat(deal.avg/10000).toFixed(1)
    period=document.createElement('div')

    year=document.createElement('div')
    year.innerText=deal.year
    period.append(year)
    month=document.createElement('div')
    month.innerText=deal.month+"월"
    month.style.alignText="center"
    period.append(month)
    bar.append(value)
    bar.append(period)
    dealInfo.append(bar);

    tr.append(dealInfo);

    })

    dealTbody.append(tr);
    dealTable.append(dealTbody)
    selectDeal.append(dealTable)




//    selectApart.classList.remove('display')
    selectDeal.classList.add('display')
    })
}