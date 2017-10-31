
var form_ids = ["#eventDisplay", "#calendarDisplay", "#calendarForm", "#editCalendarForm", "#eventForm", "#editEventForm", "#profileDisplay"]

function hide_all_forms(){
    form_ids.forEach (function(form){
        $($(form)).hide()
    });
}

$("#resetToToday" ).click(function() {
    resetView();
});

var slider = document.getElementById("zoomSlider");

slider.onchange = function (){
    d3.select('.scrollArea').call(zoom.scaleTo, this.value);
}

$("#addCalendarForm").click(function(){
    $('.side_tab').css('border-color', 'lightgrey');
    hide_all_forms()
    $("#calendarForm").show(700)
});

$("#openProfile").click(function(){
    $('.side_tab').css('border-color', 'lightgrey');
    hide_all_forms()
    $("#profileDisplay").show(700)
})

$("#addEventForm").click(function(){
    selector = $('#calendarID');
    selector.empty()
    // selector.append('<option value="" disabled selected>Choose your option</option>')
    d3.selectAll('.group').each(function(d){
        selector.append("<option value=" + d.id + ">" + d.name + "</option>");
    })
    selector.material_select();

    $('.side_tab').css('border-color', 'lightgrey');
    hide_all_forms()
    $("#eventForm").show(700)
})

$("#addCalendar").submit(function(e){
    e.preventDefault()
    $.ajax({
        url: '/add_calendar',
        data: $(this).serialize(), 
        type: 'POST',
        success: function(response) {
            if (response == 'true') {
                $("#calendarForm").hide()
                load_data()
            }
            else {
                console.log ('could not create new calendar')
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

$("#btnNewEvent").click(function(e){
    e.preventDefault()
    $('#addEvent').each(function(){
        console.log($(this).find(':input')) //<-- Should return all input elements in that specific form.
    });
    var form = $('#addEvent')[0];
    oData = new FormData(form);
    oData.append("tz", Intl.DateTimeFormat().resolvedOptions().timeZone)
    $.ajax({
        url: '/add_event',
        type: 'POST',
        data: oData, 
        dataType: "multipart/form-data",
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response)
            r = JSON.parse(response)
            if (r.success == 'true') {
                console.log('here')
                $("#eventForm").hide()
                load_data()
                // var newEvent = d3.selectAll('.datapoints').filter(function(d){return d.id == r.id}).data()
                // display(newEvent)
            }
            else {
                if (r.message == 'date'){
                    $('#startDate').addClass("validate invalid")
                                    .blur(function(){
                                        $(this).removeClass('validate invalid');
                                    });
                }
                else{
                    console.log ('Cannot create new event at this time')
                }
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// $('#addFiles').click(function(e){
//     e.preventDefault()
//     var form = $('#formFiles');
//     oData = new FormData(form[0]);
//     oData.append("event_id", event_id)
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

$('#delete_event').click(function(e){
    e.preventDefault()
    $.ajax({
        url: '/delete_event',
        type: 'POST',
        data: {'event_id': event_id},
        success: function(response) {
            if (response == 'true') {
                $("#eventDisplay").hide()
                load_data()
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
                load_data()
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