// $(document).ready(function () {
//     let $base_url = window.location.origin
//     console.log($("#search_query").val())
//     $('#search-form').on('submit', function (event) {
//         event.preventDefault();
//         let searchQuery = $("#search_query").val();
//
//         $.ajax({
//             url: $base_url + "/api/news/",
//             type: "GET",
//             data: {
//                 search: searchQuery,
//                 get_type: "latest",
//                 start: 0,
//                 end: 4
//             },
//             success: function (data) {
//                 $("#search_result_news").empty();
//                 data.map((item) => {
//                     let card_item = `
//                         <div class="col-12 col-md-4 col-lg-3 p-2">
//                             <div class="card" style="height: 300px">
//                                 <div class="card_bg" style="background-image: url('${item.image}')"></div>
//                                 <div class="card-body">
//                                     <p class="card-text">
//                                         ${item.title.slice(0, 100)}<br>
//                                         <a href="detail/${item.slug}">
//                                             ${item.read_more}
//                                         </a>
//                                     </p>
//                                 </div>
//                             </div>
//                         </div>
//                     `
//                     $("#search_result_news").append(card_item)
//                 })
//             }
//         })
//     })
// })