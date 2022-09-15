/**
 */
let $operatorConfigModal;
let $operatorConfigModalTitle;
let $operatorConfigModalIdField;
let $operatorConfigModalNameField;
let $operatorConfigModalXPathField;
let $operatorConfigModalForm;
let $operatorConfigModalFormError;

let btnCreate = ".btn-create-operator";
let btnEdit = ".btn-edit-operator";
let btnSave = "#btn-save-operator";

let defaultError = "Unexpected error while submitting the form. Please contact an " +
	"admintrator.";

let init = function() {
	$operatorConfigModal = $("#operator-config-modal");
	$operatorConfigModalTitle = $operatorConfigModal.find("#operator-modal-action");
	$operatorConfigModalIdField = $operatorConfigModal.find("#id_document_id");
	$operatorConfigModalNameField = $operatorConfigModal.find("#id_name");
	$operatorConfigModalXPathField = $operatorConfigModal.find("#id_xpath_list");
	$operatorConfigModalForm = $operatorConfigModal.find("form");
	$operatorConfigModalFormError = $operatorConfigModal.find("#operator-modal-form-error");
};

let resetPopUp = function() {
	$operatorConfigModalForm.find(".form-group").each(function() {
		$(this).removeClass("has-error");
	});
	$operatorConfigModalForm.find(".alert-danger").each(function() {
		$(this).remove();
	});
	$(btnSave).attr("disabled", false);
	$(btnSave).addClass("btn-primary");
	$(btnSave).removeClass("btn-danger");
	$operatorConfigModalFormError.text("");
};

let showPopUp = function(event) {
	let $target = $(event.target);
	$targetParent = $target.parents("tr");
	let operatorId = null;

	if($targetParent.attr("id")) {
		operatorId = $targetParent.attr("id");
	}

	configurePopUp(operatorId);
	$operatorConfigModal.modal("show");
};

let configurePopUp = function(operatorId) {
	resetPopUp();
	if(operatorId === null) {
		$operatorConfigModalTitle.text("Create");
		$operatorConfigModalNameField.val("");
		$operatorConfigModalXPathField.val("");
		$operatorConfigModalIdField.val("");
	} else {
		$operatorConfigModalTitle.text("Edit");
        $.ajax({
            url : searchOperatorsEditUrl,
            type : "GET",
            dataType: "json",
            async: false,
            data: {"document_id":operatorId},
            success: function() {},
            error: function(data) {
                if("responseText" in data) {
                    try {
                        $operatorConfigModalForm.replaceWith($(data.responseText));
                        init();
                    } catch (error) {
                        displayErrorPopUp();
                    }
                } else {
                    displayErrorPopUp();
                }

            }
        });
	}
};

let displayErrorPopUp = function() {
	$operatorConfigModalForm.find(".form-group").each(function() {
		$(this).addClass("has-error");
	});
	$(btnSave).attr("disabled", true);
	$(btnSave).removeClass("btn-primary");
	$(btnSave).addClass("btn-danger");
	$operatorConfigModalFormError.text(defaultError);
};

let submitPopUp = function() {
	$.ajax({
        url : searchOperatorsEditUrl,
        type : "POST",
        dataType: "json",
		data: $operatorConfigModalForm.serialize(),
        success: function() {
			window.location.reload();
		},
		error: function(data) {
        	if("responseText" in data) {
				try {
					$operatorConfigModalForm.replaceWith($(data.responseText));
        			init();
				} catch (error) {
					displayErrorPopUp();
				}
			} else {
        		displayErrorPopUp();
			}

		}
    });
};

init();
$(document).on("click", btnCreate, showPopUp);
$(document).on("click", btnEdit, showPopUp);
$(document).on("click", btnSave, submitPopUp);
