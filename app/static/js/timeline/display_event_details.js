
//id,date,duration,group,recurring
var event_id = 0


function display(data){
    event_id = data.id;
    if (+data.recurring == 1) var format = d3.timeFormat('%d / %m')
    else var format = d3.timeFormat('%d/%m/%Y')

    $('.side_tab').css('border-color', data.color);

    $('.eventID').text(data.name)
    $('.eventDateStart').text(format(parse(data.start_date)))
    $('.eventDateEnd').text(format(parse(data.end_date)))
    $('.eventGroup').text(data.group)
    $('.eventRecur').text(function () {return +data.recurring == 1 ? 'YES' : 'NO'})
    //$('eventFiles').text(data.files)

    $("#calendarForm").hide()
    $("#eventForm").hide()
    $("#eventDisplay").show()
}

