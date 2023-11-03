$(document).ready(function(){
    let base_url = window.location.origin
    $.ajax({
        type: 'GET',
        url: `${base_url}/api/widgets/faq_category/`,
        success: function (data) {
            data.map((item) => {
                let opt = `
                    <option value="${item.id}">${item.name}</option>
                `
                $('#faq_category').append(opt);
            })
        }
    })
    $("#faq_category").change(function(){
        var id = $(this).val();
        console.log(id)
        $.ajax({
            type: 'GET',
            url: `${base_url}/api/widgets/faq`,
            data: {
                faq_category: id
            },
            success: function (data) {
                $('#faq_answers').empty();
                data.map((item) => {
                    let obj = `
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse-${item.id}" aria-expanded="false" aria-controls="flush-collapse-${item.id}">
                                    ${item.title}
                                </button>
                            </h2>
                            <div id="flush-collapse-${item.id}" class="accordion-collapse collapse" data-bs-parent="#faq_answers">
                                <div class="accordion-body">
                                    ${item.answer}
                                </div>
                            </div>
                        </div>
                    `
                    $('#faq_answers').append(obj);
                })
            }
        })
    })
})