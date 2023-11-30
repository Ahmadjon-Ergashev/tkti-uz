function submitForm(){
    document.getElementById('lang').submit(); 
} 
$(document).ready(function(){
    $(".social_networks_links").each(function() {
        $color = $(this).data("social-color");
        $a = $(this).find("a");
        $a.find("i").css("color", $color)
    })
    $("#social_media_btn").hide()
    $("#show_social_media_btn").click(function(){
        $("#social_media_btn").fadeToggle()  
    })
    const df = new RegExp("default.jpg")
    let text = $("#object_base_img")[0]?.children[0]?.attributes[0]?.nodeValue
    $("#object_post").map((item) => {
        if ($("#object_post")[item].children[0]?.children[0]?.localName === "img" || df.test(text)) {
            $("#object_base_img").hide()
        }
    });
    $("#the_videos .video_tab_item").hover(
        function() {
            $(this).prop("controls", true);
        },
        function() {
            $(this).prop("controls", false);
        }
    );
    $(".ql-align-center").addClass("text-center");
})
