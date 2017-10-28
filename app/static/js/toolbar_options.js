
$("#resetToToday" ).click(function() {
    resetView();
});

var slider = document.getElementById("zoomSlider");

slider.onchange = function (){
    d3.select('.scrollArea').call(zoom.scaleTo, this.value);
}

$("#addCalendarForm").click(function(){
    $('.side_tab').css('border-color', 'lightgrey');
    $("#calendarForm").show()
    $("#eventForm").hide()
    $("#eventDisplay").hide()
})

$("#addEventForm").click(function(){
    selector = $('#calendarID');
    selector.empty()
    d3.selectAll('.group').each(function(d){
        selector.append("<option value=" + d.id + ">" + d.name + "</option>");
    })
    selector.material_select();

    $('.side_tab').css('border-color', 'lightgrey');
    $("#calendarForm").hide()
    $("#eventForm").show()
    $("#eventDisplay").hide()
})

$("#addCalendar").submit(function(e){
    e.preventDefault()
    console.log($('#endDate'))
    $.ajax({
        url: '/add_calendar',
        data: $(this).serialize(), 
        type: 'POST',
        success: function(response) {
            if (response == 'true') {
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
    $.ajax({
        url: '/add_event',
        data: $(this).serialize(), 
        type: 'POST',
        success: function(response) {
            if (response == 'true') {
                load_data()
            }
            else {
                console.log ('could not create new event')
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