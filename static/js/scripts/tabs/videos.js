$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: "api/videos",
        data: {
            end: 6,
            get_type: "latest"
        },
        success: function(data){
            data.map((item) => {
                let obj = `
                    <div class="col-12 col-lg-4 col-xxl-4 mb-3">
                        <div class="video">
                            <video class="video_tab_item" controls id="video_${item.id}" width="100%" poster="${item.poster}">
                                <source src="${item.video_file}" type="video/mp4">
                            </video>
                        </div>
                        <p>${item.title.slice(0, 100)}</p>
                        <span>${item.added_at}</span>
                    </div>
                `
                $("#the_videos").append(obj)
            })
        }
    });
})