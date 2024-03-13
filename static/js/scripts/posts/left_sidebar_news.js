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
            data.map((ads) => {
                let cards = `
                    <li>
                        <div class="header_tabs_section">
                            <span><a href="/ads/detail/${ ads.slug }">${ ads.added_at }</a></span>
                            <span><i class="fas fa-eye"></i> ${ ads.post_viewed_count }</span>
                        </div>
                        <div class="body_tabs_section">
                            <a href="/ads/detail/${ ads.slug }">
                                ${ ads.title.slice(0, 55) }
                            </a>
                        </div>
                    </li>
                `
                $("#most_read_ads_4").append(cards)
            })
        }
    })

    $.ajax({
        type: "GET",
        url: `${$base_url}/api/news/`,
        data: {
            "get_type": "latest",
            "start": 0,
            "end": 4
        },
        success: function (data) {
            data.map((news) => {
                let cards = `
                    <li>
                        <div class="header_tabs_section">
                            <span><a href="/news/detail/${ news.slug }">${ news.added_at }</a></span>
                            <span><i class="fas fa-eye"></i> ${ news.post_viewed_count }</span>
                        </div>
                        <div class="body_tabs_section">
                            <a href="/news/detail/${ news.slug }">
                                ${ news.title.slice(0, 55) }
                            </a>
                        </div>
                    </li>
                `
                $("#most_read_news_4").append(cards)
            })
        }
    })
})