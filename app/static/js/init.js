
(function($) {
    $(function() {

        $('select').material_select();

        $('.dropdown-button').dropdown({
            inDuration: 300,
            outDuration: 225,
            hover: true, // Activate on hover
            belowOrigin: true, // Displays dropdown below the button
            alignment: 'right' // Displays dropdown with edge aligned to the left of button
          }
        );

        $('.datepicker').pickadate({
            selectMonths: true, // Creates a dropdown to control month
            selectYears: 15, // Creates a dropdown of 15 years to control year,
            today: 'Today',
            clear: 'Clear',
            close: 'Ok',
            closeOnSelect: false, // Close upon selecting a date,
            format: 'yyyy-mm-dd'
        });

        load_data('id');
    });

    jQuery(window).on('load', function(){
        $('#preloader').fadeOut('slow',function(){$(this).remove();});
    });
})(jQuery);