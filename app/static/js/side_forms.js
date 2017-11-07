
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

function calendars_list(){
    $('#sidebar').load("/side/calendars_list")
};

function display_calendar(calendar_data){
    $('#sidebar').load("/side/display_calendar", function(){
        populate(calendar_data)
    })
}

function edit_calendar(){
    
}

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

function load_notifications(){
    $('#sidebar').load("/side/notifications")
}

$("#showFriends").click(function(){
    $('#sidebar').load("/side/friends")
});