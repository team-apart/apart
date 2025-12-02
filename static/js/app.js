// 검색창 요소(.search) 찾기.
const searchEl = document.querySelector('.search');
const searchInputEl = document.querySelector('.input');
const regionEl=document.querySelector('.region')
//// 검색창 요소를 클릭하면 실행.
searchEl.addEventListener('click', function () {
  searchInputEl.focus();
})
regionEl.addEventListener('click',function(e){
alert(e.name)
})
// 검색창 요소 내부 실제 input 요소에 포커스되면 실행.
searchInputEl.addEventListener('focus', function () {
  searchEl.classList.add('focused')
  searchInputEl.setAttribute('placeholder', '통합검색')
})
// 검색창 요소 내부 실제 input 요소에서 포커스가 해제(블러)되면 실행.
searchInputEl.addEventListener('blur', function () {
  searchEl.classList.remove('focused')
  searchInputEl.setAttribute('placeholder', '')
})
const selectedGu=[]
function addRegion(city){
const cities=Object.values(document.querySelectorAll('.'+city+''))
//console.log(cities)

    cities.map(city=>{
    if(!selectedGu.includes(city.value)){
    selectedGu.push(city.value)
//    console.log('입력',selectedGu)
    }else{

//    console.log('삭제',city.value,selectedGu.indexOf(city.value))
    selectedGu.shift(selectedGu.indexOf(city.value))

    }
 console.log(selectedGu)
})}
function selectGU(gu){
console.log(gu)}