var identify = function() {
    $.ajax({
        type: "GET",
        url: 'http://localhost:5000/cypher',
        datatype: 'json',
        data: { text: $('#text').val() },
        success: function(data) {
            langs = data.results;
            for(var i = 1; i < 4; ++i) {
                lang = langs[i - 1];
                if (lang)
                    $("#lang-" + i).html(lang.replace(/\"/g, ""));
                else
                    $("#lang-" + i).html("N/A");
            }
            $("#inline").html(data["inline-comments"]);
            $("#block").html(data["block-comments"]);
            console.log(JSON.stringify(data));
        },
        error: function(error) {
            console.log(error);
        }
    });
};

$(document).ready(function() {
    var textarea = $("#text");
    textarea.bind(
        'input propertychange',
        _.debounce(identify, 500, { maxWait: 500 })
    );
});
