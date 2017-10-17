
//zoom listener
var zoom = d3.zoom()
                .scaleExtent([1, 12])
                .on("zoom", rescale)

//attach listener to an object
d3.select('.scrollArea')            
        .call(zoom)
        .on("dblclick.zoom", null);

function resetView() {
    //adjust view to today
    var today = time(new Date());
    d3.select('.scrollArea').call(zoom.scaleTo, 12);
    d3.select('.scrollArea').call(zoom.translateTo, today+xPadding/12);

    //set next event
    d3.selectAll('.datapoints')
        .filter(function(d){
            return d.x > +d3.select('.today').attr('x');
        })
        .filter(function(d, i, j){
            return i == j.length-1;
        })
        .each(function(d){
            display(d)
        })
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
            .attr('y1', function(){
                return -d3.select(this).attr('y2')
            })
            .attr('stroke-width', '2px')
    
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
    d3.select('.today').attr('x', function(){return timeRescaled(new Date())})

    //reposition datapoints
    if (!d3.selectAll('.data').empty()){  
        //Update data points positions if there are any
        d3.selectAll(".data").selectAll('.points')
            .attr('width', function(d){
                return radius*2 + d.length*k;
            })
            .attr("x", function(d, i){
                d.x = timeRescaled(parse(d.start_date))
                if (d.recurring == 1){
                    d.x = d.x % Math.round(width*k);
                    return d.x + d.length*k >= 0 ? d.x : d.x = d.x + width*k;
                }
            })

        d3.selectAll('.data').selectAll('.datapoints').sort(function(x, y){
            return d3.descending(+x.x, +y.x);
        });
        showDetails();
    };
};
                

