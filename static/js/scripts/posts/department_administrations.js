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
                            <td><a href="${item.cv}" target="_blank">${item.view}</a></td>
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
