$(function () {

    "use strict";

    //===== Prealoder

    $(window).on('load', function (event) {
        $('.preloader').delay(500).fadeOut(500);
    });


    //===== Sticky

    $(window).on('scroll', function (event) {
        var scroll = $(window).scrollTop();
        if (scroll < 20) {
            $(".navbar-area").removeClass("sticky");
            $(".navbar-area img").attr("src", "assets/images/logo.svg");
        } else {
            $(".navbar-area").addClass("sticky");
            $(".navbar-area img").attr("src", "assets/images/logo-2.svg");
        }
    });


    //===== Section Menu Active

    var scrollLink = $('.page-scroll');
    // Active link switching
    $(window).scroll(function () {
        var scrollbarLocation = $(this).scrollTop();

        scrollLink.each(function () {

            var sectionOffset = $(this.hash).offset().top - 73;

            if (sectionOffset <= scrollbarLocation) {
                $(this).parent().addClass('active');
                $(this).parent().siblings().removeClass('active');
            }
        });
    });


    //===== close navbar-collapse when a  clicked

    $(".navbar-nav a").on('click', function () {
        $(".navbar-collapse").removeClass("show");
    });

    $(".navbar-toggler").on('click', function () {
        $(this).toggleClass("active");
    });

    $(".navbar-nav a").on('click', function () {
        $(".navbar-toggler").removeClass('active');
    });


    //===== Sidebar

    $('[href="#side-menu-left"], .overlay-left').on('click', function (event) {
        $('.sidebar-left, .overlay-left').addClass('open');
    });

    $('[href="#close"], .overlay-left').on('click', function (event) {
        $('.sidebar-left, .overlay-left').removeClass('open');
    });


    //===== Back to top

    // Show or hide the sticky footer button
    $(window).on('scroll', function (event) {
        if ($(this).scrollTop() > 600) {
            $('.back-to-top').fadeIn(200)
        } else {
            $('.back-to-top').fadeOut(200)
        }
    });


    //Animate the scroll to yop
    $('.back-to-top').on('click', function (event) {
        event.preventDefault();

        $('html, body').animate({
            scrollTop: 0,
        }, 1500);
    });

    $('.js-cek-jadwal').click(function () {
        var nik = $(this).closest('form').find('input[name="nik"]').val();
        var isValid = NusantaraValid.isValidNIK(nik)

        if (!isValid) {
            $.alert({
                columnClass: 'col-md-4 col-md-offset-4',
                title: 'Hasil Pengecekan',
                content: "NIK yang anda masukkan tidak valid",
                type: 'red',
                typeAnimated: true,
                buttons: {
                    close: function () {
                    }
                }
            });
            return false;
        }
        $.post('/api-cek-jadwal', {
            nik: nik
        }).done(function (response) {
            if (response.success) {
                var template = $('#check-result-template').html()
                var rendered = Mustache.render(template, response.peserta);
                $('.js-result-card').html(rendered);
            } else {
                $.alert({
                    columnClass: 'col-md-4 col-md-offset-4',
                    title: 'Hasil Pengecekan',
                    content: "Data NIK yang anda masukkan tidak ditemukan",
                    type: 'red',
                    typeAnimated: true,
                    buttons: {
                        close: function () {
                        }
                    }
                });
            }
        }).fail(function (response) {
            console.log(response)
        });
    })

    $('form .js-cek-jadwal-input').keydown(function (e) {
        if (e.keyCode == 13) {
            e.preventDefault()
            $('.js-result-close').click()
            $('.js-cek-jadwal').click()
        }
    });


    $(document).on('click', '.js-result-close', function () {
        $(this).closest('.js-result-card').empty();
    })

});