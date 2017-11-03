
//zoom listener
var zoom = d3.zoom()
                .scaleExtent([1, 12])
                .on("zoom", rescale)

//attach zoom listener to svg
svg.call(zoom)
   .on("dblclick.zoom", null);

function resetView(date) {
    //adjust view to today
    var month = d3.timeMonth.floor(date)
    var numDays = d3.timeDay.count(month, d3.timeMonth.ceil(date))
    if (d3.timeDay.count(month, date) > numDays*3/4) month = d3.timeMonth.ceil(date);
    var focusOn = time(d3.timeDay.offset(month, Math.floor(numDays/2.0)));
    svg.call(zoom.scaleTo, 3.8);
    svg.call(zoom.translateTo, focusOn+xPadding/3.8);

    // //display next event
    // d3.selectAll('.datapoints')
    //     .filter(function(d){
    //         return d.x > +d3.select('.todayMark').attr('x');
    //     })
    //     .filter(function(d, i, j){
    //         return i == j.length-1;
    //     })
    //     .each(function(d){
    //         display_event(d)
    //     })
}

//zoom and scroll update function
function rescale() {
    var transform = d3.event.transform;
    var timeRescaled = transform.rescaleX(time);

    //recalculate axis
    axis.scale(timeRescaled)
    d3.select('.axis').call(axis)

    //show/hide bottom bar when zooming in/out
    if (!d3.selectAll('.bottomMenu').empty())
    {
        if (k > 3.3 && transform.k < 3.3){
            if (d3.select('.bottomMenu').attr('up') === 'false') ToggleAgendaMenu();
        }
        else if (k < 3.3 && transform.k > 3.3){
            if (d3.select('.bottomMenu').attr('up') === 'true') ToggleAgendaMenu();
        }
    }
    k = d3.event.transform.k;
    
    //adjust slider
    slider.value = k;

    //update axis
    displayAxis
        .selectAll('line')
            .style('stroke', '#3D4148')
            .style('stroke-width', (3/4*radius))
            .attr('y1', function(){
                return -d3.select(this).attr('y2')
            })
    
    //update year count
    yearTag
        .text(function(){
            return d3.timeFormat('%Y')(timeRescaled.invert(width/2));
        });

    firstMonth
        .text(function(){
            return d3.timeFormat('%B')(timeRescaled.invert(0));
        })
    
    //reposition today
    d3.select('.todayMark').attr('x', () => timeRescaled(new Date()) - radius)

    //reposition datapoints
    if (!d3.selectAll('.data').empty()){  
        //Update data points positions if there are any
        d3.selectAll(".data").selectAll('.points')
            .each(function(d, i){
                var startDate = new Date(d.event_start)
                d.x = timeRescaled(startDate)
                if (d.event_recurring == 1){
                    d.event_year = d3.timeFormat('%Y')(startDate)
                    d.event_year -= Math.floor(d.x / Math.round(width*k))
                    var child = d.children.filter(c => d.event_year == c.child_year)
                    if (child.length > 0){
                        startDate = new Date(child[0].child_start)
                        startDate.setFullYear(d.event_year) // TODO delete this after testing
                        d.x = timeRescaled(startDate)
                        d.length = timeRescaled(new Date(startDate)) - d.x // TODO change to child[0].child_end
                    }
                    else{
                        startDate.setFullYear(d.event_year)
                        d.x = timeRescaled(startDate)
                    }
                    // TODO make duplicate if need to display more on same screen
                }
            })
            .attr('width', function(d){
                return radius*2 + d.length*k;
            })

        d3.selectAll('.data').selectAll('.datapoints').sort(function(x, y){
            return d3.descending(+x.x, +y.x);
        });
        showDetails();
    };
};
                

