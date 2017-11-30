$("#zoomSlider").on("input", function (){
    svg.call(zoom.scaleTo, this.value);
});

function AddGroupButtons(groups){
    // add calendar buttons
    var container = $(".calendarsContainerInner")
    container.empty();
    groups.forEach(function(gr){
        container.append(`<a class="groupInstance z-depth-3 hoverable" href="#!" data-id="${gr.calendar_id}" data-color="${gr.calendar_color}" style="background-color: ${gr.calendar_color}"> \
                            <div class="groupInstanceName">${gr.calendar_name}</div> \
                            <div class="groupInstanceSettings right anim" href="#!" data-id="${gr.calendar_id}"><i class="material-icons">settings</i></div> \
                          </a>`)
    })

    //toggle display of events that belong to certain calendar on click
    $(".groupInstance").on('click', function(e){
        var id = $(this).data('id');
        ToggleAgenda(id)
        if ($(this).css("opacity") == 1) {
            $(this).css("opacity", 0.3)
        }
        else $(this).css("opacity", 1)
    })

    //check wether click was on settings or toggle display
    $(".groupInstanceSettings").on('click', function(e){
        if ($(this).hasClass("hover")){
            e.stopPropagation()
            request_calendar($(this).data('id'))
        } 
    })

    //change color on hover of corner triangle
    $(".groupInstanceSettings").on('mousemove', function(e){
        var offset = $(this).offset();
        if (e.pageX - offset.left - e.pageY + offset.top > 0){
            if (!$(this).hasClass('hover')) $(this).addClass('hover')
        }
        else $(this).removeClass('hover')
    })

    $(".groupInstanceSettings").on('mouseleave', function(e){
        $(this).removeClass('hover')
    })

    //shorten name if too long
    $(".groupInstanceName").each(function(){short_text_div($(this), 150, 30)})
}

//scroll calendar container if there are many calendars
$(".calendarsContainerInner").on('mousewheel', function(e){
    var scrollConst = e.originalEvent.wheelDelta/120*32.75
    calendars_container_scroll(scrollConst)
})

function calendarsContainerInnerUp(){
    calendars_container_scroll(131)
}


function calendarsContainerInnerDown(){
    calendars_container_scroll(-131)
}

function calendars_container_scroll(scrollConst){
    var container = $(".calendarsContainerInner")
    var numRows = container.height()/131
    var scroll = parseFloat(container.css("top"))+scrollConst
    scroll = Math.max(-131*(numRows-1), Math.min(scroll, 0))
    container.css("top", () => scroll+"px")
}

//open/close calendar container on button click
function ToggleAgendaMenu(){
    var $toggle = $(".calendarsContainer, .calendarToolbox")
    if ($toggle.hasClass('open')){
        $toggle.addClass('closed')
        $toggle.removeClass('open')
        $('.toggleArrow').text('arrow_drop_up')
    }
    else{
        $toggle.addClass('open')
        $toggle.removeClass('closed')  
        $('.toggleArrow').text('arrow_drop_down')   
    }
}

// text cutoff
function short_text_div(self, textWidth, endTextBuffer) {
    var textLength = self.width(),
        text = self.text();
    while (textLength > (textWidth - endTextBuffer)) {
        text = text.slice(0, -1);
        self.text(text + '...');
        textLength = self.width();
    }
}

//open calendar on side bar when settings button pressed
function request_calendar(cal_id){
    $.ajax({
        url: '/request_calandar',
        method: 'POST',
        dataType: 'json',
        data: {"cal_id": cal_id},
        success: function(r){
            if (r.success == 'true'){
                display_calendar(JSON.parse(r.data));
            }
        },
        error: function(error) {
            console.log(error);
        },
    });
};


