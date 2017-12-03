function init_forms(){
    Materialize.updateTextFields();
    $('select').material_select();
}

function init_date(){
    init_forms();
    
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15,
        today: 'Today',
        clear: 'Clear',
        close: 'Ok',
        closeOnSelect: true, // Close upon selecting a date,
    });
}

function init_dropdown(){
    $('.dropdown-button').dropdown({
        inDuration: 300,
        outDuration: 225,
        hover: false, // Activate on hover
        belowOrigin: true, // Displays dropdown below the button
        alignment: 'right' // Displays dropdown with edge aligned to the left of button
        }
    );
}
