
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
    $.ajax({
        url: '/add_calendar',
        data: $(this).serialize(), 
        type: 'POST',
        success: function(response) {
            if (response == 'true') {
                load_data()
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
        },
        error: function(error) {
            console.log(error);
        }
    });
});