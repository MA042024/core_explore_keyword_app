/**
 * Search
 */
var timer;
const SELECT_ALL_LABEL = "Select All";
const UNSELECT_ALL_LABEL = "Unselect All";

const global_event = {
    input_id: 'id_global_templates',
    button_selector: '.selectAllGlobalTemplateButton'
}

const user_event = {
    input_id: 'id_user_templates',
    button_selector: '.selectAllUserTemplateButton'
}

/**
 * Show / hide placeholder
 */
function showHidePlaceholder($tagit){
   var $input = $tagit.data("ui-tagit").tagInput;
   placeholderText = $tagit.data("ui-tagit").options.placeholderText;

    if ($tagit.tagit("assignedTags").length > 0) {
        $input.removeAttr('placeholder');
        $(".tagit-new").css({"width": "auto"});
    } else {
        $input.attr('placeholder', placeholderText);
        $(".tagit-new").css({"width": "100%"});
    }
}

/**
 * Initialize auto submission
 */
var initAutoSubmit = function() {
    $("#id_keywords").tagit({
        onTagAdded: function(event, ui) {
            // delay submission after a tag is added
            fancyTreeSelectDelaySubmit();
        }
    });

    $('#id_keywords').tagit().next('ul').find('li input.ui-widget-content').focus(function(e) {
        if (!e.originalEvent) return;
        // avoid submission when a tag is focused
        clearTimeout(timer);
        timer = null;
    });

    $(".ui-autocomplete-input").on("keypress", () => {
        // avoid submission when user is typing
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
        afterTagAdded: function (event, ui) {
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
    // init the place holder and calc his width
    showHidePlaceholder($("#id_keywords").tagit());
};


/**
 * Initialize select template all button
 */
var initSelectAllTemplate = function() {
    $(".selectAllGlobalTemplateButton").on("click", global_event, selectAllTemplate);
    $(".selectAllUserTemplateButton").on("click", user_event, selectAllTemplate);
    $("input[id^='id_global_templates']").each(function(i) {
        $(this).on("change", global_event, checkIfAllTemplateSelected);
    });
    $("input[id^='id_user_templates']").each(function(i) {
        $(this).on("change", user_event, checkIfAllTemplateSelected);
    });
    checkIfAllTemplateSelected({ data: global_event });
    checkIfAllTemplateSelected({ data: user_event });
}

/**
 * check if all templates are selected
 */
var checkIfAllTemplateSelected = function(event) {
    var allSelected = true;
    $("input[id^=" + event.data.input_id + "]").each(function(i) {
        if($(this).prop("checked") == false) {
            allSelected = false;
            return false;
        }
    });

    if (allSelected) {
        $(event.data.button_selector).html(UNSELECT_ALL_LABEL);
    } else {
        $(event.data.button_selector).html(SELECT_ALL_LABEL);
    }
}

/**
 * Select all Template function
 */
var selectAllTemplate = function(event) {
    var selectAll = false;
    if ($(event.data.button_selector).html().trim() == SELECT_ALL_LABEL) {
        selectAll = true;
        $(event.data.button_selector).html(UNSELECT_ALL_LABEL);
    } else {
        $(event.data.button_selector).html(SELECT_ALL_LABEL);
    }
    $("input[id^=" + event.data.input_id + "]").each(function(i) {
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