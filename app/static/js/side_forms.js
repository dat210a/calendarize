
var form_div_ids = ["#eventDisplay", "#calendarDisplay", "#calendarForm", "#editCalendarForm", "#eventForm", "#editEventForm", "#profileDisplay"];
var current_event = null

var slider = document.getElementById("zoomSlider");


$("#resetToToday" ).click(function() {
    resetView(new Date);
});

slider.onchange = function (){
    svg.call(zoom.scaleTo, this.value);
};

// load forms
$("#addCalendarForm").click(function(){
    $('#sidebar').load("/side/add_calendar")
});

$("#addEventForm").click(function(){
    $('#sidebar').load("/side/add_event")
});

$("#calendarsSettings").click(function(){
    $('#sidebar').load("/side/display_calendars")
});

function editEvent(){
    $('#sidebar').load("/side/edit_event")
}

function display(){
    $('#sidebar').load("/side/display_event")
}

$("#openProfile").click(function(){
    $('#sidebar').load("/side/display_profile")
});

//

////////////////////////////////////////////////////////////////////////
//                           Add new data



// $('#addFiles').click(function(e){
//     e.preventDefault()
//     var form = $('#formFiles');
//     oData = new FormData(form[0]);
//     oData.append("event_id", current_event.event_id)
//     $.ajax({
//         url: '/add_files',
//         type: 'POST',
//         dataType: 'multipart/form-data',
//         data: oData, 
//         processData: false,
//         contentType: false,
//         success: function(response) {
//             if (response == 'true') {
//                 console.log ('success')
//             }
//             else {
//                 console.log ('could not upload files')
//             }
//         },
//         error: function(error) {
//             console.log('error: ', error);
//         }
//     });
// });

////////////////////////////////////////////////////////////////////////
//                           Edit data



////////////////////////////////////////////////////////////////////////
//                           Delete data

$('#delete_event').click(function(e){
    e.preventDefault()
    $.ajax({
        url: '/delete_event',
        type: 'POST',
        data: {'event_id': current_event.event_id},
        success: function(response) {
            if (response == 'true') {
                $("#eventDisplay").hide()
                current_event = null;
                load_data();
            }
            else {
                console.log (response, 'could not delete this event')
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

$('#delete_calendar').click(function(e){
    e.preventDefault()
    $.ajax({
        url: '/delete_calendar',
        type: 'POST',
        data: {'calendar_id': calendar_id}, // TODO
        success: function(response) {
            if (response == 'true') {
                $("#eventDisplay").hide()
                current_event = null;
                load_data();
            }
            else {
                console.log (response, 'could not delete this calendar')
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});