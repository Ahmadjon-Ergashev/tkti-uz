$(document).ready(() => {
    let $base_url = window.location.origin
    $.ajax({
        type: "GET",
        url: `${$base_url}/api/videos/`,
        data: {
            "get_type": "latest",
            "start": 0,
            "end": 6
        },
        success: function (data){
            data.map((obj) => {
                console.log(obj)
                let item_card = `
                    <div class="col-12 col-lg-4 col-xxl-3 mb-3">
                        <div class="item">
                            <div class="item_img" style="background-image: url('${ obj.poster }');">
                                <!-- <img src="{{ obj.image.url }}" alt="{{ obj.title }} | tkti.uz"> -->
                            </div>
                            <div class="item_body">
                                <h4>
                                    <a href="/videos/detail/${ obj.slug }">
                                        ${ obj.title.slice(0, 120) }
                                    </a>
                                </h4>
                            </div>
                            <div class="item_footer">
                                <span><a href="">${ obj.added_at }</a></span>
                                <span><i class="far fa-eye me-1"></i>${ obj.post_viewed_count }</span>
                            </div>
                        </div>
                    </div> 
                `
                $("#the_videos").append(item_card)
            })
        }
    })
})