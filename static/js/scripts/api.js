$(document).ready(function(){
    $NF404 = $("#not_found_404").data("not-found");
    $.ajax({
        type: "GET",
        url: "api/posts/study_degree",
        data: {},
        success: function(data) {
            if (data.length !== 0) {
                data.map((item)=>{
                    select_type = `<option value="${item.id}">${item.name}</option>`
                    $("#id_type").append(select_type)
                })
            }
        }
    });
    $("#id_type").on("change", () => {
        $("#id_faculty").empty()
        $("#id_faculty").append(`<option value="">--------------------</option>`)
        $.ajax({
            type: "GET",
            url: `api/posts/study_degree/${$("#id_type").val()}`,
            data: {},
            success: function(data) {
                console.log(data)
                if (data.length !== 0) {
                    data.faculty.map((i)=>{
                        select_faculty = `<option value="${i.id}">${i.title}</option>`
                        $("#id_faculty").append(select_faculty)
                    })
                }
            }
        });
    })
    $("#id_faculty").on("change", ()=> {
        $("#id_way").empty()
        $("#id_way").append(`<option value="">--------------------</option>`)
        $.ajax({
            type: "GET",
            url: "api/posts/learning_way",
            data: {
                faculty: $("#id_faculty").val()
            },
            success: function(data) {
                if (data.length !== 0) {
                    data.map((item)=>{
                        select_dept = `<option value="${item.id}">${item.name}</option>`
                        $("#id_way").append(select_dept)
                    })
                }
            }
        });
    })
    $('#filter_study_way').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'GET',
            url: "api/posts/study_programs/", 
            data: {
                year: $("#id_year").val() !== "--------------------" ? $("#id_year").val(): "",
                faculty: $("#id_faculty").val() !== "--------------------" ? $("#id_faculty").val(): "",
                department: $("#id_dept").val() !== "--------------------" ? $("#id_dept").val(): "",
                study_way: $("#id_type").val() !== "--------------------" ? $("#id_type").val(): ""
            },
            success: function(data) {
                $('#result_data').empty();
                if (data.length !== 0) { 
                    data.map((item) => {
                        console.log(item)
                        var listItem = `
                            <ul class="list-group list-group-flush border-bottom-1">
                                <li class="list-group-item"><span>${item.title}</span> 
                                <div class="btn-group" role="group" aria-label="Basic example">
                                    <a class="btn btn-primary" href="${item.pdf_file}" download="${item.pdf_file}">yuklab olish</a>
                                    <a class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#StudyWay${item.id}" aria-controls="offcanvasScrolling">Ko'rish</a></li>
                                </div>
                                <div class="offcanvas offcanvas-start w-100" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="StudyWay${item.id}" aria-labelledby="offcanvasScrollingLabel">
                                    <div class="offcanvas-header">
                                        <h5 class="offcanvas-title" id="offcanvasScrollingLabel">${item.title}</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                                    </div>
                                    <div class="offcanvas-body">
                                        <iframe src="${item.pdf_file}" width="100%" height="100%" frameborder="0"></iframe>
                                    </div>
                                </div>
                            </ul>
                        `
                        $('#result_data').append(listItem);
                    })                  
                } else {
                    $('#result_data').append(`<p class="text-center">Afsuski ma'lumotlar to'pilmadi</p>`); 
                }
            }
        });
    });

    // faculty and departments
    $.ajax({
        type: 'GET',
        url: "api/posts/faculty_list/",
        data: {},
        success: function(data){
            data.map((item) => {
                obj = `
                <div class="faculty" data-faculty-title="${item.title}" data-faculty-id="${item.id}">
                    <div class="card_img" style="background-image: url('${item.image}');">
                        <p>${item.title}</p>
                    </div>
                </div>
                `
                $("#faculties .card_box").append(obj)
            })
            $(".card_img p").hide();
            $(".faculty").on("mouseenter mouseleave", function() {
                $(this).find(".card_img p").fadeToggle();
            })
            $("#departments .wrapper").hide()
            $(".faculty").on("click", function() {
                let faculty_id = $(this).data("faculty-id")
                let title = $(this).data("faculty-title")
                $("#departments .box").fadeIn()
                showDepartments(faculty_id)
                $("#departments .wrapper #faculty_title").html(title)
                $("#departments .wrapper").fadeIn()
            })
        }
    });
    function showDepartments(faculty_id){
        $("#departments .row").empty();
        $.ajax({
            type: 'GET',
            url: "api/posts/departments_list/", 
            data: {
                faculty: faculty_id
            },
            success: function(data){
                if (data.length != 0) {
                    $("#departments #not_found_dept").hide()
                    data.map((item) => {
                        this_faculty = `
                            <div class="col-12 col-lg-4 col-xxl-3 mb-3">
                                <div class="dept-item">
                                    <p>
                                        <a href="/posts/navbar/post/${item.faculty.slug}">
                                            ${item.faculty.title}
                                        </a>    
                                    </p>
                                </div>
                            </div>
                        `
                        let obj = `     
                            <div class="col-12 col-lg-4 col-xxl-3 mb-3">
                                <div class="dept-item">
                                    <p>
                                        <a href="/posts/departments/${item.slug}">
                                            ${item.name}
                                        </a>
                                    </p>
                                </div>
                            </div>
                        `
                        $("#departments .row").append(obj);
                    }); 
                    $("#departments .row").prepend(this_faculty);
                } else {
                    $("#departments #not_found_dept").html($NF404).show()
                }
            } 
        })
    }
})