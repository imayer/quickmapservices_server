// QMS add form
var QMSAddForm = (function(){
    var qmsAddForm = $(".qms-add-service");

    var boundaryMap = null;

    function isFormFilled(form){
        var result = false;
        form.find("input, select").each(function(){
            if ($(this).val()) {
                result = true;
                return false;
            }
        });
        return result;
    }

    function bindBoundaryLinks() {
        var links = $(".service-boundary-link");

        links.on("click", function(e) {
            var mapDiv = $(e.target).parent().siblings(".service-boundary-map-container");

            if( $("#boundary-map-control").length == 0 ) {
                var mapControl = $('<div id="boundary-map-control"></div>').addClass('service-boundary-map').appendTo(mapDiv);

                var closeMapContainerButton = $('<div class="close-map-container-link"></div>').html('x').appendTo(mapDiv);
                closeMapContainerButton.on("click", function(e) {
                    mapDiv.hide(400);
                });

                // init leaflet map
                boundary_map = L.map('boundary-map-control').setView([55, 44], 2)
                L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png",
                    {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}
                ).addTo(boundary_map);

                var rectangle = L.rectangle([[30.0, 0.0], [70.0, 100.0]]).addTo(boundary_map);

                rectangle.editing.enable();

                rectangle.on('edit', function() {
                    $(e.target).parent().siblings('textarea').val( JSON.stringify( rectangle.toGeoJSON() ) );
                });
            }

            mapDiv.show(400, function() {
                boundary_map.invalidateSize();
            });


        });
    }

    var me = {
        init: function(){
            // binds links for displaying map control for bounding box of service
            bindBoundaryLinks();

            qmsAddForm.each(function(){
                var form = $(this),
                    licenseForm = form.find(".qms-add-service__license-form"),
                    licenseInfo = form.find(".qms-add-service__license-info");

                licenseForm.on("innerForm.save", function(){
                    if (isFormFilled(licenseForm)){
                        licenseInfo.addClass("filled");
                    } else{
                        licenseInfo.removeClass("filled");
                    }
                });

                form.on("submit", function(e){
                    if (form.valid()) {
                        if (!isFormFilled(licenseForm)) {
                            return confirm(noLicenseConfirmText);
                        } else {
                            return true;
                        }
                    } else {
                        return false;
                    }
                });
            })
        }
    }

    if (qmsAddForm.length)
        me.init();

    return me;
})();