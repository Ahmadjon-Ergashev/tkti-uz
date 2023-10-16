$(document).ready(function(){
    const base_url = "http://127.0.0.1:8000/uz/"
    $.ajax({
        type: "GET",
        url: "api/widgets/years",
        data: {},
        success: function(data) {
            if (data.length !== 0) {
                data.map((item)=>{
                    console.log(item)
                    select_year = `<option value="${item.year}">${item.year}</option>`
                    $("#id_year").append(select_year)
                })
            }
        }
    });
    $("#id_type").on("change", () => {
        $.ajax({
            type: "GET",
            url: "api/posts/faculty_list",
            data: {},
            success: function(data) {
                if (data.length !== 0) {
                    data.map((item)=>{
                        // console.log(item)
                        select_faculty = `<option value="${item.id}">${item.title}</option>`
                        $("#id_faculty").append(select_faculty)
                    })
                }
            }
        });
    })
    $("#id_faculty").on("change", ()=> {
        // console.log($("#id_faculty").val())
        $.ajax({
            type: "GET",
            url: "api/posts/departments_list",
            data: {
                faculty: $("#id_faculty").val()
            },
            success: function(data) {
                if (data.length !== 0) {
                    data.map((item)=>{
                        // console.log(item)
                        select_dept = `<option value="${item.id}">${item.name}</option>`
                        $("#id_dept").append(select_dept)
                    })
                }
            }
        });
    })
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