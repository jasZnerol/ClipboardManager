// First, checks if it isn't implemented yet.
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

html_template = '<div id="cbm-item-{0}">{1}</div>'

function update_clipboard(clipboard) {
  document.getElementById("items").innerHTML = "";
  items = ""
  for (var i in clipboard) {
    // console.log(html_template.format(i, clipboard[i]));
    items += (html_template.format(i, clipboard[i]) + '\n');
  }
  document.getElementById("items").innerHTML = items;
}



$(document).ready(function () {
  eel.expose(update_clipboard);
});