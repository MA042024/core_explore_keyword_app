/**
 */
let $operatorDeleteModal = $("#operator-delete-modal");
let $operatorDeleteId = $("#operator-id");
let $operatorDeleteModalNames = $operatorDeleteModal.find(".operator-name");

let btnDelete = ".btn-delete-operator";
let btnSubmit = "#btn-delete-operator";

let showDeletePopUp = function(event) {
	let $target = $(event.target);

	$operatorDeleteId.val($target.parents("tr").attr("id"));
	$operatorDeleteModalNames.each(function() {
		$(this).text($target.parents("tr").children("td:eq(0)").text());
	});
	$operatorDeleteModal.modal("show");
};

let submitDeletePopUp = function() {
	$.ajax({
        url : searchOperatorsDeleteUrl,
        type : "POST",
		data: {
        	"id": $operatorDeleteId.val()
		},
        complete: function() {  // Execute wether error or success is returned
			window.location.reload();
		}
    });
};

$(document).on("click", btnDelete, showDeletePopUp);
$(document).on("click", btnSubmit, submitDeletePopUp);
