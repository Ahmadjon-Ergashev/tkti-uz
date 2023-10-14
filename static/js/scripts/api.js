$(document).ready(function(){
    const base_url = "http://127.0.0.1:8000/uz/"
    $('#filter_study_way').submit(function(event) {
        event.preventDefault();  
        var formData = $(this).serialize();
        $.ajax({
            type: 'GET',
            url: "api/posts/study_programs", 
            data: formData,
            success: function(data) {
                $('#result_data').empty();
                if (data.length !== 0) {                    
                    for (var i = 0; i < data.length; i++) {
                        var stf = data[i];
                        var listItem = `
                            <ul class="list-group list-group-flush border-bottom-1">
                                <li class="list-group-item"> ${stf.title} <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#StudyWay${stf.id}" aria-controls="offcanvasScrolling">show</button></li>
                                <div class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="StudyWay${stf.id}" aria-labelledby="offcanvasScrollingLabel">
                                    <div class="offcanvas-header">
                                        <h5 class="offcanvas-title" id="offcanvasScrollingLabel">Offcanvas with body scrolling</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                                    </div>
                                    <div class="offcanvas-body">
                                        <p>${stf.title}</p>
                                    </div>
                                </div>
                            </ul>`
                        $('#result_data').append(listItem);
                    }
                } else {
                    $('#result_data').append(`<p class="text-center">Afsuski ma'lumotlar to'pilmadi</p>`); 
                }
            }
        });
    });
})