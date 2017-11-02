
//id,date,duration,group,recurring
var current_event = {}


function display(data){
    $("#eventDisplay").hide(0)
    current_event = data;
    if (+data.event_recurring == 1) var format = d3.timeFormat('%d / %m')
    else var format = d3.timeFormat('%d/%m/%Y')

    $('.eventdetailsfixedheader').css('background-color', data.color);
    $('.eventdetailsheaderBtn').css('background-color', data.color);

    $('.eventName').text(data.event_name)
    $('#event_owner').text("Created by: "+data.event_owner)
    $('.eventDateStart').text(format(new Date(data.event_start)))
    $('.eventDateEnd').text(format(new Date(data.event_end)))
    $('.eventGroup').text(function(){
        groupName = d3.selectAll('.group')
                            .filter(function(d){
                                return d.calendar_id == data.event_calendar_id
                            })
                            .data()[0]
                                .calendar_name
        return groupName;
    })
    $('.eventRecur').text(function () {return +data.event_calendar_id == 1 ? 'YES' : 'NO'})
    
    $('#event_notes').empty()
    if (data.event_details == '') $('#event_notes').text("No notes added")
    else $('#event_notes').text(data.event_details)

    $('#eventFiles').empty()
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


