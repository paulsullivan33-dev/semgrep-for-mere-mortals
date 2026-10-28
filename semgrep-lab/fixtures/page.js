// A small page script for the lab, with two classic mistakes
// planted in it: eval() on text from the page, and HTML built
// by dropping unescaped text into the page.

function runUserCode(code) {
  return eval(code);
}

function showGreeting(name) {
  var el = document.getElementById("greeting");
  el.innerHTML = "Hello, " + name;
}

function showFixedMessage() {
  var el = document.getElementById("greeting");
  el.innerHTML = "Welcome back.";
}
