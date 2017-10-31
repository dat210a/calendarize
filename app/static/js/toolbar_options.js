
$("#resetToToday" ).click(function() {
    resetView();
});

var slider = document.getElementById("zoomSlider");

slider.onchange = function (){
    d3.select('.scrollArea').call(zoom.scaleTo, this.value);
}

$("#addCalendarForm").click(function(){
    $('.side_tab').css('border-color', 'lightgrey');
    $("#eventForm").hide()
    $("#profileDisplay").hide()
    $("#eventDisplay").hide()
    $("#calendarForm").show(700)
})

$("#openProfile").click(function(){
    $('.side_tab').css('border-color', 'lightgrey');
    $("#eventForm").hide()
    $("#eventDisplay").hide()
    $("#calendarForm").hide()
    $("#profileDisplay").show(700)
})

$("#addEventForm").click(function(){
    selector = $('#calendarID');
    selector.empty()
    d3.selectAll('.group').each(function(d){
        selector.append("<option value=" + d.id + ">" + d.name + "</option>");
    })
    selector.material_select();

    $('.side_tab').css('border-color', 'lightgrey');
    $("#eventDisplay").hide()
    $("#profileDisplay").hide()
    $("#calendarForm").hide()
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

$("#addEvent").submit(function(e){
    e.preventDefault()
    var form = $(this);
    oData = new FormData(form[0]);
    oData.append("tz", Intl.DateTimeFormat().resolvedOptions().timeZone)
    $.ajax({
        url: '/add_event',
        data: oData, 
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(response) {
            r = JSON.parse(response)
            if (r.success == 'true') {
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
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

$('#addFiles').click(function(e){
    e.preventDefault()
    var form = $('#formFiles');
    oData = new FormData(form[0]);
    oData.append("event_id", event_id)
    $.ajax({
        url: '/add_files',
        type: 'POST',
        dataType: 'multipart/form-data',
        data: oData, 
        processData: false,
        contentType: false,
        success: function(response) {
            if (response == 'true') {
                console.log ('success')
            }
            else {
                console.log ('could not upload files')
            }
        },
        error: function(error) {
            console.log('error: ', error);
        }
    });
})