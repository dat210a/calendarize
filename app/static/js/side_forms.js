
var form_div_ids = ["#eventDisplay", "#calendarDisplay", "#calendarForm", "#editCalendarForm", "#eventForm", "#editEventForm", "#profileDisplay"];
var current_event_id = null

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

$("#editEvent").click(function(){
    hide_all_forms()
    $("#editEventForm").show(700)
});


//id,date,duration,group,recurring
var current_event_id = null


function display(data){
    $("#eventDisplay").hide(0)
    current_event_id = data.event_id;
    if (+data.event_recurring == 1) var format = d3.timeFormat('%d %B, ' + data.event_year)
    else var format = d3.timeFormat('%d %B, %Y')

    $('.eventdetailsfixedheader').css('background-color', data.color);
    $('.eventdetailsheaderBtn').css('background-color', data.color);

    $('.eventName').text(data.event_name)
    $('#event_owner').text("Created by: "+data.event_owner)
    $('.eventDateStart').text(format(new Date(data.event_start)))
    $('.eventDateEnd').text(format(new Date(data.event_end)))
    $('.eventGroup').text(() => d3.selectAll('.group').filter(d => d.calendar_id == data.event_calendar_id).data()[0].calendar_name)
    $('.eventRecur').text(() => +data.event_recurring == 1 ? 'YES' : 'NO')
    
    $('#event_notes').empty()
    if (data.event_details == '') $('#event_notes').text("No notes added")
    else $('#event_notes').text(data.event_details)

    $('#eventFiles').empty()
    if (data.files.length > 0){
        data.files.forEach (function(filename){
            $('#eventFiles').append("<a href='/uploads/"+ filename +"?id="+ data.event_id +"' download='"+ filename +"'>"+ filename +"</a><br>")
        })
    }
    else{
        $('#eventFiles').append("<span>No files added</span>")
    }

    hide_all_forms()
    $("#eventDisplay").show(700)
}

function populate_edit_form(){

}

$("#openProfile").click(function(){
    hide_all_forms()
    $("#profileDisplay").show(700)
});

//
$("#startDate").change(function(){
    var $input = $('#uniqueendDate').pickadate()
    var picker = $input.pickadate('picker')
    picker.set('min', $(this).val())
});

////////////////////////////////////////////////////////////////////////
//                           Add new data



// $('#addFiles').click(function(e){
//     e.preventDefault()
//     var form = $('#formFiles');
//     oData = new FormData(form[0]);
//     oData.append("event_id", current_event_id)
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
        data: {'event_id': current_event_id},
        success: function(response) {
            if (response == 'true') {
                $("#eventDisplay").hide()
                current_event_id = null;
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
                current_event_id = null;
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