$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: "api/news/events",
        data: {
            end: 8,
            start: 0,
            get_type: "upcoming"
        },
        success: function(data){
            data.map((item) => {
                let obj = `
                    <div class="col-12 col-md-6 col-lg-4 col-xl-3 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <div class="card_header">
                                    <h5 class="card-title_h5">${item.title.slice(0, 80)}</h5>
                                </div>
                                <div class="box_footer">
                                    <span class="time">${item.added_at}</span> <br>
                                    <span>${item.event_type.name}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `
                $("#upcoming_events").append(obj)
            })
        }
    });
    $.ajax({
        type: "GET",
        url: "api/news/events",
        data: {
            end: 8,
            start: 0,
            get_type: "all"
        },
        success: function(data){
            data.map((item) => {
                let obj = `
                    <div class="col-12 col-md-6 col-lg-4 col-xl-3 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <div class="card_header">
                                    <h5 class="card-title_h5">${item.title.slice(0, 80)}</h5>
                                </div>
                                <div class="box_footer">
                                    <span class="time">${item.added_at}</span> <br>
                                    <span>${item.event_type.name}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `
                $("#all_events").append(obj)
            })
        }
    });
    $.ajax({
        type: "GET",
        url: "api/news/events",
        data: {
            end: 8,
            start: 0,
            get_type: "past"
        },
        success: function(data){
            data.map((item) => {
                let obj = `
                    <div class="col-12 col-md-6 col-lg-4 col-xl-3 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <div class="card_header">
                                    <h5 class="card-title_h5">${item.title.slice(0, 80)}</h5>
                                </div>
                                <div class="box_footer">
                                    <span class="time">${item.added_at}</span> <br>
                                    <span>${item.event_type.name}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `
                $("#arxiv_events").append(obj)
            })
        }
    });
})