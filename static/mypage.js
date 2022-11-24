const character = document.getElementsByClassName("char");
const back = document.getElementsByClassName("back");
const backgroundImage = 0;
if (character[0].innerHTML == '병아리') {
    back[0].style.backgroundImage = "url('../static/images/병아리.png')";
}
if (character[0].innerHTML == '고양이') {
    back[0].style.backgroundImage = "url('../static/images/고양이.jpg')";
}
if (character[0].innerHTML == '호랑이') {
    back[0].style.backgroundImage = "url('../static/images/호랑이.jpeg')";
}
if (character[0].innerHTML == '강아지') {
    back[0].style.backgroundImage = "url('../static/images/강아지.jpg')";
}
if (character[0].innerHTML == '공작새') {
    back[0].style.backgroundImage = "url('../static/images/공작새.jpg')";
}