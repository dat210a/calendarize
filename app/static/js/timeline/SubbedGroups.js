function AddGroupButtons(groups){
    var container = $(".calendarsContainerInner")
    container.empty();
    groups.forEach(function(gr){
        container.append(`<a class="groupInstance z-depth-3" href="#!" data-id="${gr.calendar_id}" style="background-color: ${gr.calendar_color}"> \
                            <div class="groupInstanceName">${gr.calendar_name}</div> \
                            <div class="groupInstanceSettings right anim" href="#!" data-id="${gr.calendar_id}"><i class="material-icons">settings</i></div> \
                          </a>`)
    })

    $(".groupInstance").on('click', function(e){
        var id = $(this).data('id');
        ToggleAgenda(id)
        if ($(this).css("opacity") == 1) {
            $(this).css("opacity", 0.3)
        }
        else $(this).css("opacity", 1)
    })

    $(".groupInstanceSettings").on('click', function(e){
        if ($(this).hasClass("hover")){
            e.stopPropagation()
            request_calendar($(this).data('id'))
        } 
    })

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

    $(".groupInstanceName").each(function(){short_text_div($(this), 150, 30)})
}

$(".calendarsContainerInner").on('mousewheel', function(e){
    var container = $(this)
    var numRows = container.height()/131
    var scrollConst = e.originalEvent.wheelDelta/120*32.5
    var scroll = parseFloat(container.css("top"))+scrollConst
    scroll = Math.max(-130*(numRows-1), Math.min(scroll, 0))
    container.css("top", () => scroll+"px")
})

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

function hide(){
    console.log("hide")
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


