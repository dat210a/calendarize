var colors = ['#f57c00', '#d32f2f', '#c2185b', '#7b1fa2', '#512da8', '#1976d2', '#0097a7', '#689f38'];
var current_event = null;

var slider = document.getElementById("zoomSlider");

slider.onchange = function (){
    svg.call(zoom.scaleTo, this.value);
};

$("#resetToToday" ).click(function() {
    resetView(new Date);
});

// load forms
// function calendars_list(){
//     $('#sidebar').load("/side/calendars_list");
// };

function add_calendar(){
    $('#sidebar').load("/side/add_calendar");
};

function display_calendar(calendar_data){
    $('#sidebar').load("/side/display_calendar", function(){

        populate(calendar_data);
    });
};

function edit_calendar(calendar_data){
    $('#sidebar').load("/side/edit_calendar", function(){
        populate(calendar_data);
    });
};

function add_event(){
    $('#sidebar').load("/side/add_event");
};

function display_event(){
    $('#sidebar').load("/side/display_event");
};

function edit_event(){
    $('#sidebar').load("/side/edit_event");
};

function edit_instance(){
    $('#sidebar').load("/side/edit_instance");
};

function display_profile(){
    $('#sidebar').load("/side/display_profile");
};

function edit_profile(user_data){
    $('#sidebar').load("/side/edit_profile", function(){
        populate(user_data)
    });
};

function notifications(){
    $('#sidebar').load("/side/notifications");
};

function display_friends(){
    $('#sidebar').load("/side/friends");
};

function add_friends(){
    $('#sidebar').load("/side/add_friends");
};