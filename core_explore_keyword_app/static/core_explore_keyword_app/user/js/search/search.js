/**
 * Search
 */

/**
 * Show / hide placeholder
 */
function showHidePlaceholder($tagit){
   var $input = $tagit.data("ui-tagit").tagInput,
       placeholderText = $tagit.data("ui-tagit").options.placeholderText;

    if ($tagit.tagit("assignedTags").length > 0) {
        $input.removeAttr('placeholder');
    } else {
        $input.attr('placeholder', placeholderText);
    }
}

/**
 * Initialize auto submission
 */
var initAutoSubmit = function() {
    $("#id_keywords").tagit({
        onTagAdded: function(event, ui) {
            fancyTreeSelectDelaySubmit();
        }
    });
}

/**
 * Initialize autocomplete
 */
var initAutocomplete = function () {
    $("#id_keywords").tagit({
        allowSpaces: false,
        placeholderText: 'Enter keywords, or leave blank to retrieve all records',
        afterTagRemoved: function (event, ui) {
            showHidePlaceholder($(this));
        },
        onTagAdded: function (event, ui) {
            showHidePlaceholder($(this));
        },
        autocomplete: ({
            search: function (event, ui) {
                $("#loading").addClass("isloading");
            },
            response: function (event, ui) {
                $("#loading").removeClass("isloading");
            },
            focus: function (event, ui) {
                this.value = ui.item.label;
            },
            source: function (request, response) {
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

            },
            minLength: 2,
            select: function (event, ui) {
                this.value = ui.item.label;
                $("#id_keywords").tagit("createTag", this.value);
                return false;
            }
        })
    })
};

/**
 * Called after any selection in the tree
 */
var fancyTreeSelectDelaySubmit = function(event, data){
    // clear the timer
    clearTimeout(timer);
    // submit the form after 3 sec
    timer = setTimeout(submitForm, 3000);
}

$(document).ready(function() {
    initAutocomplete();
    initAutoSubmit();
});