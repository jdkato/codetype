function clearText() {
    $('#text').val('');
    $('#inline').html('N/A');
    $('#block').html('N/A');
    $('#string').html('N/A');
    $('#lang-1').html('N/A');
    $('#lang-2').html('N/A');
    $('#lang-3').html('N/A');
}

var identify = function() {
    $.ajax({
        type: 'GET',
        url: 'http://localhost:5000/cypher',
        datatype: 'json',
        data: { text: $('#text').val() },
        success: function(data) {
            if (_.isEmpty(data)) {
                clearText();
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
                console.log(JSON.stringify(data));
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
};

$(document).ready(function() {
    var textarea = $('#text');
    textarea.bind(
        'input propertychange',
        _.debounce(identify, 500, { maxWait: 500 })
    );
});
