$(document).ready(function(){
    $base_url = window.location.origin
    $.ajax({
        type:"GET",
        url: `${$base_url}/api/posts/adminstrations/`,
        data: {},
        success: function (data) {
            data.map((item) => {
                let card_item = `
                    <div class="col-12 col-md-4 col-lg-4">
                        <div class="card" style="height: 560px">
                            <img src="${item.image}" class="card-img-top" alt="${item.f_name} | tkti.uz">
                            <div class="card-header">
                                <b>${item.position}</b>
                            </div>
                            <div class="card-body p-0">
                                <ul class="list-group list-group-flush">
                                    <li class="list-group-item"><b>${item.f_name}</b></li>
                                    <li class="list-group-item"><i class="fas fa-envelope me-1"></i> ${item.email}</li>
                                    <li class="list-group-item"><i class="fas fa-phone me-1"></i> ${item.phone}</li>
                                    <li class="list-group-item"><i class="fas fa-calendar me-1"></i> ${item.admission_days}</li>
                                    <li class="list-group-item">
                                        <a href="${item.facebook}" style="color: #3b5998;"><i class="fab fa-facebook-square me-1 fs-3"></i></a>
                                        <a href="${item.instagram}" style="color: #AC2BAC;"><i class="fab fa-instagram-square me-1 fs-3"></i></a>
                                        <a href="${item.linkedin}" style="color: #0E76A8;"><i class="fab fa-linkedin fs-3"></i></a>
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
            })
        }
    })
})