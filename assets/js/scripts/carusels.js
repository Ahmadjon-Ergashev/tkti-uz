$(document).ready(function(){
    $("#statistika").slick({
        dots: true,
        arrows: false,
        infinite: true,
        autoplay: true,
        slidesToShow: 4,
        centerMode: true,
        slidesToScroll: 1,
        autoplaySpeed: 3000,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
    
    $("#headerIMG").slick({
        infinite: true,
        arrows: false,
        autoplay: true,
        speed: 700,
        fade: true,
        autoplaySpeed: 3000,
        cssEase: 'linear'
    });

    $("#news_gallary").slick({
        infinite: true,
        arrows: false,
        autoplay: true,
        autoplaySpeed: 3000,
    });

    $('#photo_carusel').slick({
        // arrows: false,
        infinite: true,
        slidesToShow: 4,
        // centerMode: true,
        slidesToScroll: 1,
        autoplaySpeed: 3000,
        responsive: [
          {
            breakpoint: 768,
            settings: {
              arrows: false,
              centerMode: true,
              slidesToShow: 3
            }
          },
          {
            breakpoint: 480,
            settings: {
              arrows: false,
              centerMode: true,
              slidesToShow: 1
            }
          }
        ]
      });

    $("#usefull_links").slick({
        dots: true,
        arrows: false,
        infinite: true,
        autoplay: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        autoplaySpeed: 3000,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
    $("#students_list").slick({
        dots: true,
        arrows: false,
        infinite: true,
        autoplay: true,
        slidesToShow: 4,
        centerMode: true,
        slidesToScroll: 1,
        autoplaySpeed: 3000,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
})