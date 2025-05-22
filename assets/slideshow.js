document.getElementsByClassName("carousel-item").item(0).classList.add("active");

let total = document.getElementsByClassName("carousel-item").length;
let current = 0;

document.getElementById("moveRight").addEventListener("click", function() {
  let next=current;
  current= current+1;
  setSlide(next, current);
});

document.getElementById("moveLeft").addEventListener("click", function() {
  let prev=current;
  current = current- 1;
  setSlide(prev, current);
});
function setSlide(prev, next){
  let slide= current;
  if(next>total-1){
    slide=0;
    current=0;
  }
  if(next<0){
    slide=total - 1;
    current=total - 1;
  }
  document.getElementsByClassName("carousel-item").item(prev).classList.remove("active");
  document.getElementsByClassName("carousel-item").item(slide).classList.add("active");
}