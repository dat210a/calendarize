
$("#resetToToday" ).click(function() {
    resetView();
});

var slider = document.getElementById("zoomSlider");



slider.onchange = function (){
    d3.select('.scrollArea').call(zoom.scaleTo, this.value);
}

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