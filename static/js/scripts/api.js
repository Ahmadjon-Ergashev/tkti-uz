$(document).ready(function(){
    $NF404 = $("#not_found_404").data("not-found");
    $("#id_link").addClass("a_disabled");   
    function checkFields() {
        var field1 = $("#id_type").val() !== "--------------------" ? $("#id_type").val() : false;
        var field2 = $("#id_faculty").val() !== "--------------------" ? $("#id_faculty").val() : false;
        var field3 = $("#id_way").val() !== "--------------------" ? $("#id_way").val() : false;
        if (field1 && field2 && field3) {
            $("#id_link").removeClass("a_disabled");
            $("#id_link").addClass("a_able");
            $("#id_link").attr("href", `/posts/learing_way/detail/${field3}/`);         
        } else {
            $("#id_link").addClass("a_disabled");
        }
        if (!field1 | !field2 | !field3) {
            $("#id_link").addClass("a_disabled");
        }
    }
    $("#id_type, #id_faculty, #id_way").change(function () {
        checkFields();
    });

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
            },
            complete: function() {
                $("#id_type").prop("disabled", false);
            }
        });

    // $("#id_type").on("click", ()=>{
    //     $("#id_type").prop("disabled", true);
    //     $("#id_type").empty();
    //     $("#id_type").append(`<option value="">--------------------</option>`)
    //
    // })
    $("#id_type").on("change", () => {
        $("#id_faculty").empty()
        $("#id_faculty").append(`<option value="">--------------------</option>`)
        $.ajax({
            type: "GET",
            url: `api/posts/study_degree/${$("#id_type").val()}`,
            data: {},
            success: function(data) {
                if (data.length !== 0) {
                    data.field_edu.map((i)=>{
                        select_faculty = `<option value="${i.id}">${i.name}</option>`
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
                study_degree: $("#id_type").val(),
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
})