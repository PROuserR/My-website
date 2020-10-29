//Pure javascript
var inputs = document.getElementsByTagName("input");
var textareas = document.getElementsByTagName("textarea")
var selects = document.getElementsByTagName("select")
var buttons = document.getElementsByTagName("button")


for(var i = 0; i < buttons.length; i++){
    if(buttons[i].innerHTML == "Sign In")
    {
        buttons[i].className = "btn btn-primary btn-lg"
    }
}

for (var i = 0; i < inputs.length; i++) {
    inputs[i].className = "form-control"
}

for (var i = 0; i < textareas.length; i++) {
    textareas[i].className = "form-control"
}

for (var i = 0; i < textareas.length; i++) {
    selects[i].className = "form-control"
}

$(function () {
    $('[data-toggle="popover"]').popover()
  })

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

anime({
  targets: '.shadow.p-3.mb-5.bg-white.rounded',
  translateX: 0,
  rotate: '1turn',
  backgroundColor: '#FFF',
  duration: 800
});
////////////////////////////////////////////////////
var colorsExamples = anime.timeline({
    endDelay: 500,
    easing: 'linear',
    direction: 'alternate',
    loop: true
  })
  .add({ targets: '.color-hex',  background: '#FFF' }, 0)
  .add({ targets: '.color-rgb',  background: 'rgb(255,255,0)' }, 0)
  .add({ targets: '.color-hsl',  background: 'hsl(0, 100%, 100%)' }, 0)
  .add({ targets: '.color-rgba', background: 'rgba(255,255,255, .2)' }, 0)
  .add({ targets: '.color-hsla', background: 'hsla(0, 100%, 100%, .2)' }, 0)
  .add({ targets: '.colors-demo .el', translateX: 270 }, 0);