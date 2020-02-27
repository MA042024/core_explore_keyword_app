var getAutocompleteSource = function (request, response){
    $.ajax({
        type: 'POST',
        url: suggestionsURL,
        data: $("#form_search").serialize() + '&term=' + request.term,
        dataType: 'json',
        success: function (data) {
            response($.map(data.suggestions, function (item) {
                if (item.label != undefined) {
                    return {
                        label: item.label,
                        value: item.label
                    }
                }
            }));
        }
    });
}