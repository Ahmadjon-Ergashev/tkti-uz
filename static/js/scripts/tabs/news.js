$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: "api/news",
        data: {
            end: 4,
            get_type: "latest"
        },
        success: function(data){
            data.map((item) => {
                let obj = `
                    <div class="col-12 col-md-4 col-xl-3 mb-2">
                        <div class="item">
                            <div class="item_img">
                                <img src="${item.image}" alt="${item.title} | tkti.uz">
                            </div>
                            <div class="item_body">
                                <h4>
                                    <a href="news/detail/${item.slug}">
                                        ${item.title.slice(0, 120)}
                                    </a>
                                </h4>
                            </div>
                            <div class="item_footer">
                                <span><a href="">${item.added_at}</a></span>
                                <span><i class="far fa-eye me-1"></i>${item.post_viewed_count}</span>
                            </div>
                        </div>
                    </div>
                `
                $("#the_last_news_4").append(obj)
            })
        }
    });
    $.ajax({
        type: "GET",
        url: "api/news",
        data: {
            start: 4,
            end: 12,
            get_type: "latest"
        },
        success: function(data){
            data.map((item) => {
                let obj = `
                    <div class="d-none col-12 d-md-block col-md-4 col-xl-3 mb-2">
                        <div class="news_box">
                            <div class="news_box_body">
                                <p>
                                    <a href="news/detail/${item.slug}">
                                        ${item.title.slice(0, 80)}
                                    </a>
                                </p>
                            </div>
                            <div class="news_box_footer">
                                <span><a href="">${item.added_at}</a></span>
                                <span><i class="far fa-eye me-1"></i>${item.post_viewed_count}</span>
                            </div>
                        </div>
                    </div>
                `
                $("#the_last_news_8").append(obj)
            })
        }
    });
    $.ajax({
        type: "GET",
        url: "api/news",
        data: {
            end: 4,
            get_type: "most_read"
        },
        success: function(data){
            data.map((item) => {
                let obj = `
                    <div class="col-12 col-md-4 col-xl-3 mb-2">
                        <div class="item">
                            <div class="item_img">
                                <img src="${item.image}" alt="${item.title} | tkti.uz">
                            </div>
                            <div class="item_body">
                                <h4>
                                    <a href="news/detail/${item.slug}">
                                        ${item.title.slice(0, 120)}
                                    </a>
                                </h4>
                            </div>
                            <div class="item_footer">
                                <span><a href="">${item.added_at}</a></span>
                                <span><i class="far fa-eye me-1"></i>${item.post_viewed_count}</span>
                            </div>
                        </div>
                    </div>
                `
                $("#the_most_read_4").append(obj)
            })
        }
    });
    $.ajax({
        type: "GET",
        url: "api/news",
        data: {
            start: 4,
            end: 12,
            get_type: "most_read"
        },
        success: function(data){
            data.map((item) => {
                let obj = `
                    <div class="d-none col-12 d-md-block col-md-4 col-xl-3 mb-2">
                        <div class="news_box">
                            <div class="news_box_body">
                                <p>
                                    <a href="news/detail/${item.slug}">
                                        ${item.title.slice(0, 80)}
                                    </a>
                                </p>
                            </div>
                            <div class="news_box_footer">
                                <span><a href="">${item.added_at}</a></span>
                                <span><i class="far fa-eye me-1"></i>${item.post_viewed_count}</span>
                            </div>
                        </div>
                    </div>
                `
                $("#the_most_read_8").append(obj)
            })
        }
    });
});