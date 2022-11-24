const character = document.getElementsByClassName("char");
const back = document.getElementsByClassName("back");
alert(character[0].innerHTML)
if (character[0].innerHTML == '병아리') {
    // figure의 background-image를 images 폴더의 병아리.png로 변경
    back.style.backgroundImage = url('../static/images/병아리.png');
}
if (character[0].innerHTML == '고양이') {
    // figure의 background-image를 images 폴더의 고양이.png로 변경
    back.style.backgroundImage = url('../static/images/고양이.jpg');
}