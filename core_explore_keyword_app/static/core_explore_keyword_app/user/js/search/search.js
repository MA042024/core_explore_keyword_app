/**
 * Search
 */
var timer;
const SELECT_ALL_LABEL = "Select All";
const UNSELECT_ALL_LABEL = "Unselect All";


/**
 * Show / hide placeholder
 */
function showHidePlaceholder($tagit){
   var $input = $tagit.data("ui-tagit").tagInput;
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

    $('#id_keywords').tagit().next('ul').find('li input.ui-widget-content').focus(function(e) {
        if (!e.originalEvent) return;
        // clear the timer when the tag it input is focused
        // avoiding unwanted submission
        clearTimeout(timer);
        timer = null;
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
    });
};

/**
 * Initialize select template all button
 */
var initSelectAllTemplate = function() {
    $(".selectAllTemplateButton").on("click", selectAllTemplate);
    $("input[id^='id_global_templates']").each(function(i) {
        $(this).on("change", checkIfAllTemplateSelected);
    });
    checkIfAllTemplateSelected();
}

/**
 * check if all templates are selected
 */
var checkIfAllTemplateSelected = function() {
    var allSelected = true;
    $("input[id^='id_global_templates']").each(function(i) {
        if($(this).prop("checked") == false) {
            allSelected = false;
            return false;
        }
    });

    if (allSelected) {
        $(".selectAllTemplateButton").html(UNSELECT_ALL_LABEL);
    } else {
        $(".selectAllTemplateButton").html(SELECT_ALL_LABEL);
    }
}

/**
 * Select all Template function
 */
var selectAllTemplate = function() {
    var selectAll = false;
    if ($(".selectAllTemplateButton").html().trim() == SELECT_ALL_LABEL) {
        selectAll = true;
        $(".selectAllTemplateButton").html(UNSELECT_ALL_LABEL);
    } else {
        $(".selectAllTemplateButton").html(SELECT_ALL_LABEL);
    }
    $("input[id^='id_global_templates']").each(function(i) {
        $(this).prop("checked", selectAll);
    });
}

/**
 * Called after any selection in the tree
 */
var fancyTreeSelectDelaySubmit = function(force=true){
    if (force) {
        delaySubmission();
    } else {
        if (timer)
            delaySubmission();
    }
}

/**
 * Delay submission
 */
var delaySubmission = function() {
    // clear the timer
    clearTimeout(timer);
    // submit the form after 3 sec
    timer = setTimeout(submitForm, 3000);
}

/**
 * Submit the form
 */
var submitForm = function () {
    $("#form_search").submit();
}

$(document).ready(function() {
    initAutocomplete();
    initAutoSubmit();
    initSelectAllTemplate();
});