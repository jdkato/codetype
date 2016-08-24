var name2Mode = {
  'Go': 'golang',
  'C': 'c_cpp',
  'C++': 'c_cpp',
  'C#': 'csharp',
  'Objective-C': 'objectivec'
}

function clearResults() {
    $('#inline').html('N/A');
    $('#block').html('N/A');
    $('#string').html('N/A');
    $('#lang-1').html('N/A');
    $('#lang-2').html('N/A');
    $('#lang-3').html('N/A');
}

function clearText() {
    editor.setValue('')
    clearResults();
}

function identify() {
  code = editor.getValue();
  $.ajax({
    type: 'POST',
    url: 'https://cypher-api.herokuapp.com/cypher',
    datatype: 'json',
    data: { text: code },
    success: function(data) {
      if (_.isEmpty(data)) {
          clearResults();
      } else {
        var langs = data.results;
        for(var i = 1; i < 4; ++i) {
            lang = langs[i - 1];
            if (lang)
                $('#lang-' + i).html(lang.replace(/\"/g, ''));
            else
                $('#lang-' + i).html('N/A');
        }
        if (langs[0] in name2Mode) {
          mode = name2Mode[langs[0]];
        } else {
          mode = langs[0].toLowerCase();
        }
        editor.session.setMode("ace/mode/" + mode)
      }
      console.log(JSON.stringify(data));
    },
    error: function(error) {
        console.log(error);
    }
  });
};
