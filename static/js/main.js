function submitForm(){
    document.getElementById('lang').submit(); 
}
$(document).ready(function() {
    $(".social_networks_links").each(function() {
        const color = $(this).data("social-color");
        const $a = $(this).find("a");
        $a.find("i").css("color", color);
    });
    $(".brm_card, .brm_color").each(function() {
        const color = $(this).data("brm-color");
        $(this).css("background", color);
    });
    const $socialMediaBtn = $("#social_media_btn").hide();
    $("#show_social_media_btn").click(function() {
        $socialMediaBtn.fadeToggle();
    });
    const df = "default.jpg";
    const text = $("#object_base_img")[0]?.children[0]?.attributes[0]?.nodeValue;
    $("#object_post").each(function() {
        const imgElement = $(this).children(":first-child").children(":first-child")[0];

        if (imgElement && imgElement.localName === "img" || text.indexOf(df) !== -1) {
            $("#object_base_img").hide();
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
    $(".ql-align-center").addClass("text-center")
});
