$(document).ready(function (){
    let $base_url = window.location.origin;

    // Function to fetch shop list based on category
    function fetchShopList(categoryId) {
        let url = $base_url + "/api/shop/list";
        if (categoryId) {
            url += "?category=" + categoryId;
        }
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $("#tkti_shop_cards").empty(); // Clear previous cards
                data.map((item) => {
                    let card = `
                        <div class="col-10 m-auto col-sm-12 col-md-6 col-lg-3">
                            <div class="card">
                                <img src="${item.image}" class="card-img-top" alt="...">
                                <div class="card-body">
                                    <h5 class="card-title text-capitalize">${item.name}</h5>
                                    <p class="card-text">UZS ${item.price}</p>
                                    <a href="" class="btn-sm btn btn-primary rounded-5 px-2" 
                                        data-bs-toggle="modal" data-bs-target="#staticBackdrop${item.id}">
                                        Buyurtma berish
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="modal fade" id="staticBackdrop${item.id}" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel${item.id}" aria-hidden="true">
                            <div class="modal-lg modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" id="staticBackdropLabel${item.id}">Buyurtma berish</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="row">
                                            <div class="col-12 col-md-5">
                                                <img src="${item.image}" width="300" alt="">
                                            </div>
                                            <div class="col-12 col-md-7">
                                                <ul class="list-group list-group-flush">
                                                    <li class="list-group-item text-capitalize">
                                                        ${item.name}
                                                    </li>
                                                    <li class="list-group-item">
                                                        ${item.contact}
                                                    </li>
                                                    <li class="list-group-item">
                                                        ${item.phone_number}
                                                    </li>
                                                    <li class="list-group-item">
                                                        <a href="${item.telegram}">
                                                            <i style="color: #3288B0" class="fab fa-telegram fs-2"></i>
                                                        </a>
                                                        <a class="ms-2" href="${item.instagram}">
                                                            <i style="color: #AC2BAC" class="fab fa-instagram-square fs-2"></i>
                                                        </a>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    $("#tkti_shop_cards").append(card);
                });
            }
        });
    }

    // Initial fetch without category filter
    fetchShopList(null);

    // Event listener for category selection change
    $("#shop_category").change(function() {
        let categoryId = $(this).val();
        fetchShopList(categoryId);
    });

    // Fetch categories
    $.ajax({
        type: "GET",
        url: $base_url + "/api/shop/category/list",
        success: function (data) {
            data.map((item) => {
                let option = `<option value="${item.id}">${item.name}</option>`;
                $("#shop_category").append(option);
            });
        }
    });
});
