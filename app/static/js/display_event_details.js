
//id,date,duration,group,recurring
var current_event = {}


function display(data){
    $("#eventDisplay").hide(0)
    current_event = data;
    if (+data.recurring == 1) var format = d3.timeFormat('%d / %m')
    else var format = d3.timeFormat('%d/%m/%Y')

    $('.eventdetailsfixedheader').css('background-color', data.color);
    $('.eventdetailsheaderBtn').css('background-color', data.color);

    $('.eventName').text(data.name)
    $('.eventDateStart').text(format(new Date(data.start_date)))
    $('.eventDateEnd').text(format(new Date(data.end_date)))
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
    $('#eventFiles').empty()
    if (data.files.length > 0){
        data.files.forEach (function(filename){
            $('#eventFiles').append("<a href='/uploads/"+ filename +"?id="+ data.id +"' download='"+ filename +"'>"+ filename +"</a><br>")
        })
    }
    else{
        $('#eventFiles').append("<span>No files added</span>")
    }

    hide_all_forms()
    $("#eventDisplay").show(700)
}


