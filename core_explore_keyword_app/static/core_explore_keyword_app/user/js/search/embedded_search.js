/**
 * Init the search bar with tagit once jquery is loaded.
 * @param method
 */
var defer_initSearchBar = function(){
    $.getScript(tagit_url, function() {
        $("#id_keywords").tagit({
            allowSpaces: false,
        })
    });
}

onjQueryReady(defer_initSearchBar);