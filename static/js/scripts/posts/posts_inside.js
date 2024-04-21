$(document).ready(function(){
    let $base_url = window.location.origin
    $.ajax({
        type:"GET",
        url: `${$base_url}/api/posts/adminstrations/`,
        data: {},
        success: function (data) {
            data.map((item) => {

                let card_item = `
                    <div class="col-12 col-md-4 col-lg-4">
                        <div class="card" style="height: 580px">
                            <img src="${item.image}" class="card-img-top" alt="${item.f_name} | tkti.uz">
                            <div class="card-header">
                                <span class="font-weight-bold">${item.position}</span>
                            </div>
                            <div class="card-body p-0">
                                <ul class="list-group list-group-flush">
                                    <li class="list-group-item"><span>${item.f_name}</span></li>
                                    <li class="list-group-item"><i class="fas fa-envelope me-1"></i> ${item.email}</li>
                                    <li class="list-group-item"><i class="fas fa-phone me-1"></i> ${item.phone}</li>
                                    <li class="list-group-item"><i class="fas fa-calendar me-1"></i> ${item.admission_days}</li>
                                    <li class="list-group-item social-networks">
                                        <div class=""></div>
                                    </li>
                                </ul>
                            </div>
                            <div class="card-footer text-center">
                                <a href="" data-bs-toggle="modal" data-bs-target="#staticBackdrop${item.id}">${item.read_more}</a>
                                
                                <!-- Modal -->
                                <div class="modal fade" id="staticBackdrop${item.id}" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                                    <div class="modal-dialog modal-xl">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="exampleModalLabel"><b>${item.f_name}</b></h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <div class="accordion accordion-flush" id="accordionExample">
                                                    <div class="accordion-item">
                                                        <h2 class="accordion-header">
                                                            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                                                <b>${ item.short_info_title }</b>
                                                            </button>
                                                        </h2>
                                                        <div id="collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body text-start">
                                                                ${ item.short_info }
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="accordion-item">
                                                        <h2 class="accordion-header">
                                                            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
                                                                <b>${ item.scientific_direction_title }</b>
                                                            </button>
                                                        </h2>
                                                        <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body text-start">
                                                                ${ item.scientific_direction }
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="accordion-item">
                                                        <h2 class="accordion-header">
                                                            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="true" aria-controls="collapseThree">
                                                                <b>${ item.main_tasks_in_position_title }</b>
                                                            </button>
                                                        </h2>
                                                        <div id="collapseThree" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body text-start">
                                                                ${ item.main_tasks_in_position }
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="accordion-item">
                                                        <h2 class="accordion-header">
                                                            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapsefour" aria-expanded="true" aria-controls="collapsefour">
                                                                <b>${ item.scientific_activity_title }</b>
                                                            </button>
                                                        </h2>
                                                        <div id="collapsefour" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body text-start">
                                                                ${ item.scientific_activity }
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `
                $("#adminstations").append(card_item)

                if (item.boss) {
                    item.boss.forEach((instance) => {
                        let network = `
                            <a href="${instance.url}" target="_blank" style="color: ${instance.social_networks.color};"><i class="${instance.social_networks.icon} me-1 fs-3"></i></a>
                        `;
                        $(".social-networks").last().append(network);
                    });
                }
            })
        }
    })
})