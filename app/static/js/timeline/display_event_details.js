
//id,date,duration,group,recurring
var event_id = 0


function display(data){
    event_id = data.id;
    if (+data.recurring == 1) var format = d3.timeFormat('%d / %m')
    else var format = d3.timeFormat('%d/%m/%Y')

    $('.eventdetailsfixedheader').css('background-color', data.color);
    $('.eventdetailsheaderBtn').css('background-color', data.color);

    $('.eventName').text(data.name)
    $('.eventDateStart').text(format(parse(data.start_date)))
    $('.eventDateEnd').text(format(parse(data.end_date)))
    $('.eventGroup').text(function(){
        groupName = d3.selectAll('.group')
                            .filter(function(d){
                                return d.id == data.group
                            })
                            .data()[0]
                                .name
        return groupName;
    })
    $('.eventRecur').text(function () {return +data.recurring == 1 ? 'YES' : 'NO'})
    //$('eventFiles').text(data.files)

    $("#calendarForm").hide()
    $("#eventForm").hide()
    $("#eventDisplay").show()
}


