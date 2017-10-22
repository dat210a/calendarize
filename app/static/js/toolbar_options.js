
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
    $('.side_tab').css('border-color', 'lightgrey');
    $("#calendarForm").hide()
    $("#eventForm").show()
    $("#eventDisplay").hide()
})

$("#addCalendar").click(function(){
    $.ajax({
        url: '/add_calendar',
        data: $(this).serialize(), 
        type: 'POST',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
});

$("#addEvent").click(function(){
    $.ajax({
        url: '/add_event',
        data: $(this).serialize(), 
        type: 'POST',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
});