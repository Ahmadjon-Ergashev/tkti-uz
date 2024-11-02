$(document).ready(function () {
    // Function to load data based on position and department
    function loadAdministrationData(position, department) {
        let base_url = window.location.origin;

        $.ajax({
            type: "GET",
            url: base_url + "/api/department/administration/",
            data: {position: position, department: department},
            success: function (data) {
                $("#administration_item").empty();
                data.map((item) => {
                    let card_item = `
                        <tr>
                            <td>${item.f_name}</td>
                            <td>${item.position.name}</td>
                            <td>${item.email}</td>
                            <td>
                                <a type="button" class="text-primary"
                                   data-bs-toggle="offcanvas"
                                   data-bs-target="#cv_${item.id}"
                                   aria-controls="cv_${item.id}">
                                    ${item.view}
                                </a>
                                <div class="offcanvas offcanvas-start w-100 w-75-m w-75-l" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1"
                                     id="cv_${item.id}" aria-labelledby="offcanvasScrollingLabel">
                                    <div class="offcanvas-header">
                                        <h5 class="offcanvas-title" id="cv_${item.id}">${item.view}</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                                    </div>
                                    <div class="offcanvas-body">
                                        <iframe
                                                src="${item.cv}"
                                                width="100%" height="100%">
                                        </iframe>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    `;
                    $("#administration_item").append(card_item);
                });
            }
        });
    }

    // Attach click event to elements
    $('.department-admininstration[data-position]').click(function () {
        let position = $(this).data('position');
        let department = $(this).data('department');
        loadAdministrationData(position, department);
    });

    // Trigger click on the first department item to load default data
    $('.department-admininstration[data-position]').first().trigger('click');
});
