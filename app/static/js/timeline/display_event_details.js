
//id,date,duration,group,recurring

function display(data){
    if (+data.recurring == 1) var format = d3.timeFormat('%d / %m')
    else var format = d3.timeFormat('%d/%m/%Y')

    d3.select('.eventDetails').style('border-color', data.color)

    $('.eventID').text(data.id)
    $('.eventDateStart').text(format(parse(data.start_date)))
    $('.eventDateEnd').text(format(parse(data.end_date)))
    $('.eventGroup').text(data.group)
    $('.eventRecur').text(function () {return +data.recurring == 1 ? 'YES' : 'NO'})
    //$('eventFiles').text(data.files)
}

