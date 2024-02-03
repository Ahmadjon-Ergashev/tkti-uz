$(document).ready(() => {
    let $base_url = window.location.origin

    $.ajax({
        type: "GET",
        url: `${$base_url}/api/ads/`,
        data: {
            "get_type": "latest",
            "start": 0,
            "end": 4
        },
        success: function (data) {
            data.map((obj) => {
                let item_card = `
                     <div class="col-12 col-md-4 col-xl-3 mb-2">
                        <div class="item">
                            <div class="item_img" style="background-image: url('${obj.image}');">
                                <!-- <img src="{{ obj.image.url }}" alt="{{ obj.title }} | tkti.uz"> -->
                            </div>
                            <div class="item_body">
                                <h4>
                                    <a href="ads/detail/${ obj.slug }">
                                        ${obj.title.slice(0, 150)}...
                                    </a>
                                </h4>
                            </div>
                            <div class="item_footer">
                                <span><a href="">${obj.added_at}</a></span>
                                <span><i class="far fa-eye me-1"></i>${obj.post_viewed_count}</span>
                            </div>
                        </div>
                    </div>
                 `
                $("#the_last_ads_4").append(item_card)
            })
        }
    })
    $.ajax({
        type: "GET",
        url: `${$base_url}/api/ads/`,
        data: {
            "get_type": "latest",
            "start": 4,
            "end": 12
        },
        success: function (data) {
            data.map((obj) => {
                let cards = `
                    <div class="d-none col-12 d-md-block col-md-4 col-xl-3 mb-2">
                        <div class="news_box">
                            <div class="news_box_body">
                                <p>
                                    <a href="ads/detail/${ obj.slug }">
                                        ${ obj.title.slice(0, 80) }
                                    </a>
                                </p>
                            </div>
                            <div class="news_box_footer">
                                <span><a href="">${ obj.added_at }</a></span>
                                <span><i class="far fa-eye me-1"></i>${ obj.post_viewed_count }</span>
                            </div>
                        </div>
                    </div>
                `
                $("#the_last_ads_8").append(cards)
            })
        }
    })
})