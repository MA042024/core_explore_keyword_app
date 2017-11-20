initAutocomplete = function() {
     $("#id_keywords").tagit({
        allowSpaces: false,
    })
}

$(document).ready(function() {
    initAutocomplete();
});