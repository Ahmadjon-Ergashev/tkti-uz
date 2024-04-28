$(document).ready(function(){
    $base_url = window.location.origin
    $.ajax({
        type:"GET",
        url: `${$base_url}/api/posts/talented_students/`,
        data: {},
        success: function (data) {
            data.map((item) => {
                let card_item = `
                    <div class="col-12 col-md-4 col-lg-4">  
                        <div class="card" style="min-height: 440px;">
                `;
                if (item.image) {
                    card_item += `
                        <img src="${item.image}" class="card-img-top" alt="${item.f_name} | tkti.uz">
                    `;
                } else {
                    card_item += `
                        <img src="https://www.viewhotels.jp/ryogoku/wp-content/uploads/sites/9/2020/03/test-img.jpg" class="card-img-top" alt="${item.f_name} | tkti.uz">
                    `;
                }
                card_item += `
                        <div class="card-header">
                            <b>${item.f_name}</b>
                        </div>
                        <div class="card-body">
                            <p class="card-text">
                                ${item.desc}
                            </p>
                        </div>
                    </div>
                </div>
                `;
                $("#talented_students").append(card_item);
            });
}

    })
})