$(document).ready(function () {
    let $base_url = window.location.origin
    administrations_detail("rektor");

    function administrations_detail(position) {
        $.ajax({
            type: "GET",
            url: `${$base_url}/api/posts/administrations/`,
            data: {position: position},
            success: function (data) {
                $("#administrations_list").empty(); // Clear the existing list

                data.map((object) => {
                    // Create the main card structure
                    let card_item = `
                <div class="row">
                    <div class="col-12 col-md-8 border-end p-3">
                        <div class="row" id="administration_images_${object.id}"></div> <!-- Images will be appended here -->
                    </div>
                    <div class="col-12 col-md-4 p-1">
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">
                                <span class="fs-6"><b>${object.f_name}</b></span>
                                <br>
                                <small class="text-secondary">${object.position}</small>
                                <br>
                                <hr class="hr">
                                <small class="text-secondary">
                                    <i class="fas fa-envelope me-1"></i> ${object.email}
                                </small>
                                <br>
                                <small class="text-secondary">
                                    <i class="fas fa-phone me-1"></i> ${object.phone}
                                </small>
                                <br>
                                <small class="text-secondary">
                                    <i class="fas fa-calendar-alt me-1"></i> ${object.admission_days}
                                </small>
                                <br>
                                <small class="text-secondary">
                                    <i class="fas fa-map-marker-alt me-1"></i> ${object.address}
                                </small>
                                <br>
                                <hr>
                                <div class="social-networks" id="social_networks_${object.id}"></div> <!-- Social networks will be appended here -->
                            </li>
                        </ul>
                    </div>
                    <div class="col-12 px-0 border-top py-3">
                        <div class="accordion accordion-flush w-100" id="accordionExample">
                            <div class="accordion-item">
                                <h2 class="accordion-header">
                                    <button class="accordion-button" type="button"
                                            data-bs-toggle="collapse"
                                            data-bs-target="#collapseOne${object.id}"
                                            aria-expanded="true"
                                            aria-controls="collapseOne">
                                        <b>${object.short_info_title}</b>
                                    </button>
                                </h2>
                                <div id="collapseOne${object.id}" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                    <div class="accordion-body text-start">
                                        ${object.short_info}
                                    </div>
                                </div>
                            </div>
                            <div class="accordion-item">
                                <h2 class="accordion-header">
                                    <button class="accordion-button" type="button"
                                            data-bs-toggle="collapse"
                                            data-bs-target="#collapseTwo${object.id}"
                                            aria-expanded="true"
                                            aria-controls="collapseTwo">
                                        <b>${object.scientific_direction_title}</b>
                                    </button>
                                </h2>
                                <div id="collapseTwo${object.id}" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                    <div class="accordion-body text-start">
                                        ${object.scientific_direction}
                                    </div>
                                </div>
                            </div>
                            <div class="accordion-item">
                                <h2 class="accordion-header">
                                    <button class="accordion-button" type="button"
                                            data-bs-toggle="collapse"
                                            data-bs-target="#collapseThree${object.id}"
                                            aria-expanded="true"
                                            aria-controls="collapseThree">
                                        <b>${object.main_tasks_in_position_title}</b>
                                    </button>
                                </h2>
                                <div id="collapseThree${object.id}" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                    <div class="accordion-body text-start">
                                        ${object.main_tasks_in_position}
                                    </div>
                                </div>
                            </div>
                            <div class="accordion-item">
                                <h2 class="accordion-header">
                                    <button class="accordion-button" type="button"
                                            data-bs-toggle="collapse"
                                            data-bs-target="#collapseFour${object.id}"
                                            aria-expanded="true"
                                            aria-controls="collapseFour">
                                        <b>${object.scientific_activity_title}</b>
                                    </button>
                                </h2>
                                <div id="collapseFour${object.id}" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                    <div class="accordion-body text-start">
                                        ${object.scientific_activity}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;

                    // Append the card to the list
                    $("#administrations_list").append(card_item);

                    // Dynamically append the images
                    object.images.forEach((image) => {
                        let image_item = `
                        <div class="col-12 col-md-4 p-1">
                            <div class="administration_image"
                                 style="background-image: url('${image.image}');"></div>
                        </div>`;
                        $(`#administration_images_${object.id}`).append(image_item);
                    });

                    // Dynamically append the social networks
                    object.boss.forEach((network) => {
                        let network_item = `
                        <a title="${network.social_networks.name}" href="${network.url}" target="_blank" style="color: ${network.social_networks.color};">
                            <i class="${network.social_networks.icon} me-1 fs-4"></i>
                        </a>`;
                        $(`#social_networks_${object.id}`).append(network_item);
                    });
                });
            }
        });
    }


    // Use event delegation by attaching the event to the parent
    $(".administration_positions").on("click", function () {
        var position = $(this).data("position");
        administrations_detail(position);
    });

})