
//id,date,duration,group,recurring
var current_event_id = null


function display_event(data){
    hide_all_forms()
    current_event_id = data.event_id;
    if (+data.event_recurring == 1) var format = d3.timeFormat('%d %B, ' + data.event_year)
    else var format = d3.timeFormat('%d %B, %Y')

    $('.eventdetailsfixedheader').css('background-color', data.calendar_color);
    $('.eventdetailsheaderBtn').css('background-color', data.calendar_color);

    $('.eventName').text(data.event_name)
    $('.eventGroup').text(() => d3.selectAll('.group').filter(d => d.calendar_id == data.event_calendar_id).data()[0].calendar_name)
    $('.eventRecur').text(() => +data.event_recurring == 1 ? 'YES' : 'NO')

    $('#event_notes').empty()
    $('#eventFiles').empty()

    var child = data.children.filter(c => data.event_year == c.child_year)
    if (child.length > 0){
        $('#event_owner').text("Created by: "+child[0].child_owner)
        $('.eventDateStart').text(format(new Date(child[0].child_start)))
        $('.eventDateEnd').text(format(new Date(child[0].child_end)))
        if (child[0].child_details == null || child[0].child_details == '') {
            $('#event_notes').text("No notes added for this year")
        }
        else $('#event_notes').text(child[0].child_details)
        $('#event_notes').append('<br><br> \
                                  ---------- General notes ----------\
                                  <br>');
    }
    else{
        $('#event_owner').text("Created by: "+data.event_owner)
        $('.eventDateStart').text(format(new Date(data.event_start)))
        $('.eventDateEnd').text(format(new Date(data.event_end)))
    }
    
    if (data.event_details == '') $('#event_notes').append("No general notes added for this event")
    else $('#event_notes').append(data.event_details)

    if (data.files.length > 0){
        data.files.forEach (function(filename){
            $('#eventFiles').append("<a href='/uploads/"+ filename +"?id="+ data.event_id +"' download='"+ filename +"'>"+ filename +"</a><br>")
        })
    }
    else{
        $('#eventFiles').append("<span>No files added</span>")
    }

    $("#eventDisplay").show(700)
}

function fillIn_editEvent_form(){

}

function display_calendar(){

}

function fillIn_editCalendar_form(){
    
}

function display_profile(){

}

function fillIn_editCalendar_form(){
    
}