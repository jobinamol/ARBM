(function ($) {
    'use strict';

    // Preloader
    $(window).on('load', function () {
        $('.preloader').fadeOut(1000);
    });

    // Navbar Scroll
    $(window).on('scroll', function () {
        if ($(window).scrollTop() > 50) {
            $('.header-area').addClass('navbar-fixed');
        } else {
            $('.header-area').removeClass('navbar-fixed');
        }
    });

    // Hero Slider
    $('.hero-slides').owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        dots: false,
        autoplay: true,
        autoplayTimeout: 5000,
        smartSpeed: 1000,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>']
    });

    // Smooth Scroll
    $('a[href*="#"]').on('click', function (e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: $($(this).attr('href')).offset().top - 70
        }, 500, 'linear');
    });

    // Animation on Scroll
    new WOW().init();

    // Room Image Popup
    $('.room-img').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        }
    });

    // Date Picker
    $('input[type="date"]').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true
    });

    function toggleMenu() {
        const menu = document.getElementById('popupMenu');
        menu.classList.toggle('active');
        document.body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
    }

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        const menu = document.getElementById('popupMenu');
        if (e.target === menu) {
            toggleMenu();
        }
    });

})(jQuery); 