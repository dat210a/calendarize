
//id,date,duration,group,recurring
var current_event_id = null


function display(data){
    $("#eventDisplay").hide(0)
    current_event_id = data.event_id;
    if (+data.event_recurring == 1) var format = d3.timeFormat('%d %B, ' + data.event_year)
    else var format = d3.timeFormat('%d %B, %Y')

    $('.eventdetailsfixedheader').css('background-color', data.color);
    $('.eventdetailsheaderBtn').css('background-color', data.color);

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

    hide_all_forms()
    $("#eventDisplay").show(700)
}

function populate_edit_form(){

}
