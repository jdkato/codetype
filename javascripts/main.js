function clearResults() {
    $('#inline').html('N/A');
    $('#block').html('N/A');
    $('#string').html('N/A');
    $('#lang-1').html('N/A');
    $('#lang-2').html('N/A');
    $('#lang-3').html('N/A');
}

function clearText() {
    $('#text').val('');
    clearResults();
}

function identify() {
    $.ajax({
        type: 'POST',
        url: 'https://cypher-api.herokuapp.com/cypher',
        datatype: 'json',
        data: { text: $('#text').val() },
        success: function(data) {
            if (_.isEmpty(data)) {
                clearResults();
            } else {
                langs = data.results;
                for(var i = 1; i < 4; ++i) {
                    lang = langs[i - 1];
                    if (lang)
                        $('#lang-' + i).html(lang.replace(/\"/g, ''));
                    else
                        $('#lang-' + i).html('N/A');
                }
                $('#inline').html(data.inlineCount);
                $('#block').html(data.blockCount);
                $('#string').html(data.stringCount);
            }
            console.log(JSON.stringify(data));
        },
        error: function(error) {
            console.log(error);
        }
    });
};
