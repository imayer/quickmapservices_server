(function(){
    var reportPopup = $(".report-problem-popup"),
        reportForm = reportPopup.find("form"),
        serviceNameElem = reportPopup.find(".modal-subtitle a"),
        serviceIdInput = reportPopup.find("#report_service_id"),
        currentServiceId,
        prevServiceId;

    reportPopup.modal();
    reportPopup.on('show.bs.modal', function (e) {
        currentServiceId = $(e.relatedTarget).data("service-id");
        if (prevServiceId && prevServiceId != currentServiceId)
            clearReport();
        serviceNameElem.text($(e.relatedTarget).data("service-title"));
        serviceNameElem.attr("href", $(e.relatedTarget).data("service-url"));
        serviceIdInput.val(currentServiceId);
    });

    reportPopup.on('hidden.bs.modal', function (e) {
        prevServiceId = currentServiceId;
    });

    function clearReport(){
        reportForm.find("input,select,textarea").each(function(){
            this.value = "";
            $(this).change();
            $(this).valid();
        });
        reportForm.validate().resetForm();
    }
})();