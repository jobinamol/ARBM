(function($) {
    'use strict';
    
    // Smooth scrolling
    $('a[href*="#"]').on('click', function(e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: $($(this).attr('href')).offset().top - 70
        }, 500);
    });
    
    // Navbar color change on scroll
    $(window).scroll(function() {
        if ($(window).scrollTop() > 50) {
            $('.navbar').addClass('scrolled');
        } else {
            $('.navbar').removeClass('scrolled');
        }
    });
    
    // Initialize date pickers
    if($('input[type="date"]').length) {
        $('input[type="date"]').datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true
        });
    }
    
    $(document).ready(function() {
        // Auto dismiss alerts after 5 seconds
        setTimeout(function() {
            $('.alert').alert('close');
        }, 5000);
    });
    
})(jQuery); 