
var form_div_ids = ["#eventDisplay", "#calendarDisplay", "#calendarForm", "#editCalendarForm", "#eventForm", "#editEventForm", "#profileDisplay"];
var colors = ['#f57c00', '#d32f2f', '#c2185b', '#7b1fa2', '#512da8', '#1976d2', '#0097a7', '#689f38'];

var slider = document.getElementById("zoomSlider");

function hide_all_forms(){
    form_div_ids.forEach (function(form_parent){
        $(form_parent).hide()
        form = $(form_parent).children('form')[0]
        if (typeof form != 'undefined') form.reset()
    });
};

$("#resetToToday" ).click(function() {
    resetView(new Date);
});

slider.onchange = function (){
    svg.call(zoom.scaleTo, this.value);
};

// load forms
$("#addCalendarForm").click(function(){
    hide_all_forms()
    selector = $('#setCalendarColor');
    selector.empty()
    colors.forEach(function(color){
        selector.append("<option value=" + color + "></option>");
    })
    selector.material_select(); 
    $.each(colors, function(i, color){
        if (d3.selectAll(".group").filter(d => d.calendar_color == color).empty()){
            $(".setColorContainer").find(".select-dropdown").css("border-bottom", () => "5px solid " + color)    
            return false;
        } 
        if (i == colors.length-1){
            $(".setColorContainer").find(".select-dropdown").css("border-bottom", () => "5px solid " + colors[0])} 
    });
    $(".setColorContainer").find("li").each(function(i){
        $(this).empty().addClass("valign-wrapper")
               .append("<div></div>").children("div").addClass("coloredLine").css("background-color", colors[i])
    })
    selector.on("change", function(){
        $(".setColorContainer").find(".select-dropdown").css("border-bottom", () => "5px solid " + $(this).val())
    })
    Materialize.updateTextFields();
    $("#calendarForm").show(700)
});

$("#addEventForm").click(function(){
    hide_all_forms()
    selector = $('#calendarID');
    selector.empty()
    d3.selectAll('.group').each(function(d){
        selector.append("<option value=" + d.calendar_id + ">" + d.calendar_name + "</option>");
    })
    selector.material_select();

    $("#eventForm").show(700)
});

// $("#editCalendarForm").click(function(){
//     hide_all_forms()
//     $("#calendarForm").show(700)
// });

$("#editEvent").click(function(){
    hide_all_forms()
    $("#editEventForm").show(700)
});

$("#openProfile").click(function(){
    hide_all_forms()
    $("#profileDisplay").show(700)
});

//
$("#startDate").change(function(){
    var $input = $('#uniqueendDate').pickadate()
    var picker = $input.pickadate('picker')
    picker.set('min', $(this).val())
});

////////////////////////////////////////////////////////////////////////
//                           Add new data

$("#addCalendar").submit(function(e){
    e.preventDefault()
    $.ajax({
        url: '/add_calendar',
        data: $(this).serialize(), 
        type: 'POST',
        success: function(response) {
            if (response == 'true') {
                $("#calendarForm").hide();
                current_event_id = null;
                load_data();
            }
            else {
                console.log ('could not create new calendar')
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

$("#addEvent").submit(function(e){
    e.preventDefault()
    var form = $(this)[0];
    oData = new FormData(form);
    oData.set('startDate', new Date(oData.get('startDate')).getTime())
    if (oData.get('endDate') != '') oData.set('endDate', new Date(oData.get('endDate')).getTime())
    $.ajax({
        url: '/add_event',
        type: 'POST',
        data: oData, 
        encType: "multipart/form-data",
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            r = JSON.parse(response)
            if (r.success == 'true') {
                $("#eventForm").hide()
                current_event_id = r.id;
                load_data()
            }
            else {
                if (r.message == 'date'){
                    $('#startDate').addClass("validate invalid")
                                    .blur(function(){
                                        $(this).removeClass('validate invalid');
                                    });
                }
                else{
                    console.log ('Cannot create new event at this time')
                }
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// $('#addFiles').click(function(e){
//     e.preventDefault()
//     var form = $('#formFiles');
//     oData = new FormData(form[0]);
//     oData.append("event_id", current_event_id)
//     $.ajax({
//         url: '/add_files',
//         type: 'POST',
//         dataType: 'multipart/form-data',
//         data: oData, 
//         processData: false,
//         contentType: false,
//         success: function(response) {
//             if (response == 'true') {
//                 console.log ('success')
//             }
//             else {
//                 console.log ('could not upload files')
//             }
//         },
//         error: function(error) {
//             console.log('error: ', error);
//         }
//     });
// });

////////////////////////////////////////////////////////////////////////
//                           Edit data



////////////////////////////////////////////////////////////////////////
//                           Delete data

$('#delete_event').click(function(e){
    e.preventDefault()
    $.ajax({
        url: '/delete_event',
        type: 'POST',
        data: {'event_id': current_event_id},
        success: function(response) {
            if (response == 'true') {
                $("#eventDisplay").hide()
                current_event_id = null;
                load_data();
            }
            else {
                console.log (response, 'could not delete this event')
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

$('#delete_calendar').click(function(e){
    e.preventDefault()
    $.ajax({
        url: '/delete_calendar',
        type: 'POST',
        data: {'calendar_id': calendar_id}, // TODO
        success: function(response) {
            if (response == 'true') {
                $("#eventDisplay").hide()
                current_event_id = null;
                load_data();
            }
            else {
                console.log (response, 'could not delete this calendar')
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});