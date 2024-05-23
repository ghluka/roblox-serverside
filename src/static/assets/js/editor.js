
var GetText;
var SetText;
var ClearText;
var SetTheme;

ace.require("ace/ext/language_tools");
var editor = ace.edit("editor");
editor.setTheme("ace/theme/tomorrow_night_eighties");
editor.session.setMode("ace/mode/lua");
editor.setOption("enableLiveAutocompletion", true);
editor.setOption("cursorStyle", "smooth");
editor.setShowPrintMargin(false);
document.getElementById('editor').style.fontSize='13px';

GetText = function()
{
    return editor.getValue();
}

SetText = function(x)
{
  editor.setValue(x);
  editor.session.setValue(x);
}

ClearText = function()
{
  editor.setValue("");
}

SetTheme = function(th)
{
  editor.setTheme("ace/theme/" + th);
}

document.oncontextmenu = function()
{
  return false;
}