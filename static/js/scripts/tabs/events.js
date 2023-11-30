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
                            <div class="event_modal">
                                <div class="modal_window">
                                    <div class="row">
                                        <div class="col-7">
                                            <h5>${item.title}</h5>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item ps-0"><span class="font-monospace">${item.event_type.name}</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-calendar-alt pe-2"></i><span>${item.added_at}</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-map-marker-alt pe-2"></i></i><span>${item.location}</span></li>
                                                <li class="list-group-item ps-0"><a href="" class="search_btn">${item.read_more}</a></li>
                                            </ul>
                                        </div>
                                        <div class="col-5">
                                            <iframe 
                                                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d5992.611411878445!2d69.2526138524833!3d41.323965330062755!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38ae8b737f1f4161%3A0xab6842dfd7a53fdf!2sToshkent%20kimyo-texnologiya%20instituti%20(TKTI)!5e0!3m2!1suz!2s!4v1695310071406!5m2!1suz!2s" 
                                                width="100%" height="360px" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade">
                                            </iframe>
                                        </div>
                                    </div>
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
                            <div class="event_modal">
                                <div class="modal_window">
                                    <div class="row">
                                        <div class="col-7">
                                            <h5>${item.title}</h5>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item ps-0"><span class="font-monospace">${item.event_type.name}</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-calendar-alt pe-2"></i><span>${item.added_at}</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-map-marker-alt pe-2"></i></i><span>${item.location}</span></li>
                                                <li class="list-group-item ps-0"><a href="" class="search_btn">${item.read_more}</a></li>
                                            </ul>
                                        </div>
                                        <div class="col-5">
                                            <iframe 
                                                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d5992.611411878445!2d69.2526138524833!3d41.323965330062755!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38ae8b737f1f4161%3A0xab6842dfd7a53fdf!2sToshkent%20kimyo-texnologiya%20instituti%20(TKTI)!5e0!3m2!1suz!2s!4v1695310071406!5m2!1suz!2s" 
                                                width="100%" height="360px" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade">
                                            </iframe>
                                        </div>
                                    </div>
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
                            <div class="event_modal">
                                <div class="modal_window">
                                    <div class="row">
                                        <div class="col-7">
                                            <h5>${item.title}</h5>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item ps-0"><span class="font-monospace">${item.event_type.name}</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-calendar-alt pe-2"></i><span>${item.added_at}</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-map-marker-alt pe-2"></i></i><span>${item.location}</span></li>
                                                <li class="list-group-item ps-0"><a href="" class="search_btn">${item.read_more}</a></li>
                                            </ul>
                                        </div>
                                        <div class="col-5">
                                            <iframe 
                                                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d5992.611411878445!2d69.2526138524833!3d41.323965330062755!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38ae8b737f1f4161%3A0xab6842dfd7a53fdf!2sToshkent%20kimyo-texnologiya%20instituti%20(TKTI)!5e0!3m2!1suz!2s!4v1695310071406!5m2!1suz!2s" 
                                                width="100%" height="360px" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade">
                                            </iframe>
                                        </div>
                                    </div>
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