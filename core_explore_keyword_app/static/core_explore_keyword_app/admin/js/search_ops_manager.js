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

let separator = "\n";

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
	let operator = {
		id: null,
		name: null,
		xpath_list: null
	};

	if($target.hasClass("btn-edit-operator")) {
		let $targetParent = $target.parents("tr");

		operator.id = $targetParent.attr("id");
		operator.name = $targetParent.children("td:eq(0)").text();
		operator.xpath_list = $targetParent.find("td:eq(1) li");
	}

	configurePopUp(operator);
	$operatorConfigModal.modal("show");
};

let configurePopUp = function(operator) {
	resetPopUp();
	if(operator.id === null) {
		$operatorConfigModalTitle.text("Create");
		$operatorConfigModalNameField.val("");
		$operatorConfigModalXPathField.val("");
		$operatorConfigModalIdField.val("");
	} else {
		$operatorConfigModalTitle.text("Edit");
		$operatorConfigModalIdField.val(operator.id);
		$operatorConfigModalNameField.val(operator.name);

		let xpath_list = "";
		$(operator.xpath_list).each(function() {
			xpath_list += $.trim($(this).text())+separator;
		});

		$operatorConfigModalXPathField.val(xpath_list);
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
        url : "/admin/operators/edit",
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
