var editor;
var instances = [];
var services = [];
var enums = [];

require(['/assets/vs/editor/editor.main'], function() {

  monaco.editor.defineTheme('vsLight', {base: 'vs'});
  monaco.editor.defineTheme('vsDark', {base: 'vs-dark'});
  
  monaco.editor.defineTheme('studio', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      {token: 'keyword', foreground: 'f86d7c', fontStyle: "bold"},
      {token: 'global', foreground: '84d6f7', fontStyle: "bold"},
      {token: 'type', foreground: '84d6f7'},
      {token: 'string', foreground: 'adf195'},
      {token: 'number', foreground: 'ffc600'},
      {token: 'number.float', foreground: 'ffc600'},
      {token: 'number.hex', foreground: 'ffc600'},
      {token: 'operator', foreground: 'cccccc'},
      {token: 'comment', foreground: '666666'},
      {token: 'comment.todo', fontStyle: "bold"},
    ],
    colors: {
      'editor.background': '#252525',
      'editor.foreground': '#cccccc',
    }
  });

  editor = monaco.editor.create(document.getElementById('container'), {
    language: 'json',
    theme: "studio",
    folding: true,
    scrollbar: {
      useShadows: false,
      verticalHasArrows: true,
    },
    automaticLayout: true,
    dragAndDrop: true,
    links: true,
    readOnly: true,
    minimap: {enabled: false,},
    showFoldingControls: "always",
    smoothScrolling: true,
    colorDecorators: true,
    lineNumbers: "on",
    lineNumbersMinChars: 3,
    roundedSelection: true,
    scrollBeyondLastLine: false,
    acceptSuggestionOnEnter: "on",
    autoClosingBrackets: "always",
    detectIndentation: true,
    autoIndent: "full",
    insertSpaces: false,
    cursorBlinking: "phase",
    formatOnPaste: true,
    formatOnType: true,
    snippetSuggestions: "bottom",
    stickyTabStops: true,
    wordBasedSuggestionsOnlySameLanguage: false,
  });

});

var getText = function () {return editor.getValue();}
var setText = function (x) {editor.setValue(x);}
var setTheme = function (themeName) {monaco.editor.setTheme(themeName)}

var setImage = function (x) {
  document.getElementsByClassName("lines-content monaco-editor-background")[0].style.backgroundImage = "url=(" + x + ")";
  document.getElementsByClassName("margin")[0].style.backgroundImage = "url=(" + x + ")";
}

var switchMinimap = function (flag) {editor.updateOptions({minimap: {enabled: flag,}});}
var switchReadonly = function (flag) {editor.updateOptions({readOnly: flag,});}
var switchRenderWhitespace = function (op) {editor.updateOptions({renderWhitespace: op,});}
var switchLinks = function (flag) {editor.updateOptions({links: flag,});}
var switchLineHeight = function (num) {editor.updateOptions({lineHeight: num,});}
var switchFontSize = function (num) {editor.updateOptions({fontSize: num,});}
var switchFolding = function (flag) {editor.updateOptions({folding: flag,});}
var switchAutoIndent = function (flag) {editor.updateOptions({autoIndent: flag,});}
var switchFontFamily = function (name) {editor.updateOptions({fontFamily: name,});}
var switchFontLigatures = function (flag) {editor.updateOptions({fontLigatures: flag,});}

var showErr = function (line, column, endline, endcolumn, errMessage) {
  editor.revealPositionInCenter({ lineNumber: line, column: column });
  editor.deltaDecorations([], [
    {
      range: new monaco.Range(line, column, endline, endcolumn),
      options: {
        inlineClassName: 'squiggly-error',
        hoverMessage: {value: errMessage,},
      },
    },
  ]);
}

var setScroll = function (line) {editor.revealLineInCenter({ lineNumber: line });}

const resizeObserver = new ResizeObserver(_ => {
  try {
    editor.layout();
  }
  catch {}
});
resizeObserver.observe(document.getElementById("container"));
try {
  editor.layout();
}
catch {}