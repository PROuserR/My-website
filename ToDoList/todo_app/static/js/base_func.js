//Pure javascript
var inputs = document.getElementsByTagName("input");
var textareas = document.getElementsByTagName("textarea")
var selects = document.getElementsByTagName("select")

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