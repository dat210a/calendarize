
var form_div_ids = ["#eventDisplay", "#calendarDisplay", "#calendarForm", "#editCalendarForm", "#eventForm", "#editEventForm", "#profileDisplay"];
var colors = ['#f57c00', '#d32f2f', '#c2185b', '#7b1fa2', '#512da8', '#1976d2', '#0097a7', '#689f38'];
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

function editProfile(){
    $('#sidebar').load("/side/edit_profile")
}

$("#showNotifications").click(function(){
    $('#sidebar').load("/side/notifications")
})

$("#showFriends").click(function(){
    $('#sidebar').load("/side/friends")
})