
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

const goNext=document.querySelector('.goNext')
const left=goNext.querySelector('.leftArrow')
const leftBtn=left.querySelector('img')
const right=goNext.querySelector('.rightArrow')
const righttBtn=right.querySelector('img')
const status=document.querySelector('.status')
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
if(status){
goNext.style="none"
}
left.addEventListener('click',function(){
    selectApart.classList.remove('display')
    selectDong.classList.add('display')
    status.innerText=1
})
right.addEventListener('click',function(){
selectDong.classList.remove('display')
selectApart.classList.add('display')
})
const selectedGu=[]
const selectedDong=[]


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
}}

async function selectedDongCommit(){
 status.innerText=1
    const tableValues=[];
    dongTbody.innerHTML="";
//    console.log('tableValues',tableValues)
try{
    const dongs=await axios.get('http://localhost:8000/getDongs')
//    console.log('new_dongs',dongs.data)
    const results=selectedGu.map(gu=>dongs.data.filter(dong=>dong.name===gu))
//    console.log('results',results.data)
//     console.log('new_dongs',new_dongs.data)
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
            })
    })

//    apartTbody.append(tr);
//    apartTable.append(apartTbody)
//    selectApart.append(apartTable)

    dongTbody.append(tr);
    dongTable.append(dongTbody)
    selectDong.append(dongTable)
    selectDong.classList.add('display')
    selectApart.classList.remove('display')
    })
}


async function selectedApartCommit(){
    status.innerText=2
    const tableValues=[];
    apartTbody.innerHTML="";
    console.log('selectedDong',selectedDong)
try{
    const aparts=await axios.get('http://localhost:8000/getApart')
    console.log('aparts',aparts)
    const results=selectedDong.map(dong=>aparts.data.filter(apart=>apart.name===dong))


    console.log('results',results)
//     console.log('new_dongs',new_dongs.data)
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
        }else{
            div.classList.add('selected')
            }
            })
    })

    apartTbody.append(tr);
    apartTable.append(apartTbody)
    selectApart.append(apartTable)

//    dongTbody.append(tr);
//    dongTable.append(dongTbody)
//    selectDong.append(dongTable)



    selectDong.classList.remove('display')
    selectApart.classList.add('display')
    })
}
