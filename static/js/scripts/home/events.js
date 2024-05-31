$(document).ready(() => {
    let $base_url = window.location.origin
    $.ajax({
        type: "GET",
        url: `${$base_url}/api/news/events/`,
        data: {
            "get_type": "upcoming",
            "start": 0,
            "end": 8
        },
        success: function (data)  {
            data.map((upc) => {
                let cards = `
                    <div class="col-12 col-md-6 col-lg-4 col-xl-3 mb-3">
                        <div class="card"  style="min-height: 190px;">
                            <div class="card-body">
                                <div class="card_header">
                                    <h5 class="card-title_h5">
                                        ${ upc.title.slice(0, 80) }
                                    </h5>
                                </div>
                                <div class="box_footer">
                                    <span class="time">${ upc.added_at }</span> <br>
                                    <span>${ upc.event_type.name }</span>
                                </div>
                            </div>
                            <div class="event_modal">
                                <div class="modal_window">
                                    <div class="row">
                                        <div class="col-12 p-4">
                                            <h5>${ upc.title }</h5>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item ps-0"><span class="font-monospace">${ upc.event_type.name }</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-calendar-alt pe-2"></i><span>${ upc.added_at }</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-map-marker-alt pe-2"></i></i><span>${ upc.location }</span></li>
                                                <li class="list-group-item ps-0"><a href="/events/detail/${ upc.slug }" class="search_btn">${ upc.read_more }</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `
                 $("#upcoming_events").append(cards)
            })
        }
    })
    $.ajax({
        type: "GET",
        url: `${$base_url}/api/news/events/`,
        data: {
            "get_type": "all",
            "start": 0,
            "end": 8
        },
        success: function (data) {
            data.map((upc) => {
                let cards = `
                    <div class="col-12 col-md-6 col-lg-4 col-xl-3 mb-3">
                        <div class="card" style="min-height: 190px;">
                            <div class="card-body">
                                <div class="card_header">
                                    <h5 class="card-title_h5">
                                        ${ upc.title.slice(0, 80) }
                                    </h5>
                                </div>
                                <div class="box_footer">
                                    <span class="time">${ upc.added_at }</span> <br>
                                    <span>${ upc.event_type_name }</span>
                                </div>
                            </div>
                            <div class="event_modal">
                                <div class="modal_window">
                                    <div class="row">
                                        <div class="col-12 p-4">
                                            <h5>${ upc.title }</h5>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item ps-0"><span class="font-monospace">${ upc.event_type_name }</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-calendar-alt pe-2"></i><span>${ upc.added_at }</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-map-marker-alt pe-2"></i></i><span>${ upc.location }</span></li>
                                                <li class="list-group-item ps-0"><a href="/events/detail/${ upc.slug }" class="search_btn">${ upc.read_more }</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `
                 $("#all_events").append(cards)
            })
        }
    })
    $.ajax({
        type: "GET",
        url: `${$base_url}/api/news/events/`,
        data: {
            "get_type": "past",
            "start": 0,
            "end": 8
        },
        success: function (data) {
            data.map((upc) => {
                let cards = `
                    <div class="col-12 col-md-6 col-lg-4 col-xl-3 mb-3">
                        <div class="card" style="min-height: 190px;">
                            <div class="card-body">
                                <div class="card_header">
                                    <h5 class="card-title_h5">
                                        ${ upc.title.slice(0, 80) }
                                    </h5>
                                </div>
                                <div class="box_footer">
                                    <span class="time">${ upc.added_at }</span> <br>
                                    <span>${ upc.event_type_name }</span>
                                </div>
                            </div>
                            <div class="event_modal">
                                <div class="modal_window">
                                    <div class="row">
                                        <div class="col-12 p-4">
                                            <h5>${ upc.title }</h5>
                                            <ul class="list-group list-group-flush">
                                                <li class="list-group-item ps-0"><span class="font-monospace">${ upc.event_type_name }</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-calendar-alt pe-2"></i><span>${ upc.added_at }</span></li>
                                                <li class="list-group-item ps-0"><i class="fas fa-map-marker-alt pe-2"></i></i><span>${ upc.location }</span></li>
                                                <li class="list-group-item ps-0"><a href="/events/detail/${ upc.slug }" class="search_btn">${ upc.read_more }</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `
                 $("#arxiv_events").append(cards)
            })
        }
    })
})