
//zoom listener
var zoom = d3.zoom()
                .scaleExtent([1, 12])
                .on("zoom", rescale)

//attach zoom listener to svg
svg.call(zoom)
   .on("dblclick.zoom", null);

function resetView(date) {
    //adjust view to date
    var month = d3.timeMonth.floor(date)
    var numDays = d3.timeDay.count(month, d3.timeMonth.ceil(+month + 1))
    if (d3.timeDay.count(month, date) > numDays*3/4) month = d3.timeMonth.ceil(date);
    var focusOn = time(d3.timeDay.offset(month, Math.floor(numDays/2.0)));
    svg.call(zoom.scaleTo, 3.8);
    svg.call(zoom.translateTo, focusOn+xPadding/3.8);
}

//zoom and scroll update function
function rescale() {
    var transform = d3.event.transform;
    var timeRescaled = transform.rescaleX(time);

    //recalculate axis
    axis.scale(timeRescaled)
    d3.select('.axis').call(axis)
    k = d3.event.transform.k;
    
    //adjust slider
    colorStop = (k-0.5)/12*100;
    $("#zoomSlider").val( k );
    $("#zoomSlider").css("--gradient", () => 'linear-gradient(90deg, #3D4148 '+ colorStop +'%, #97989c '+ colorStop +'%)')

    //update axis
    displayAxis
        .selectAll('line')
            .style('stroke', '#3D4148')
            .style('stroke-width', (3/4*radius))
            .each(function(d){
                if (d.getMonth() == 0){
                    d3.select(this).attr('y2', () => +d3.select(this).attr('y2') + 20)
                                   .attr('y1', () => -d3.select(this).attr('y2'))
                }
                else d3.select(this).attr('y1', () => -d3.select(this).attr('y2'))
            })

    displayAxis
        .selectAll("text")
        .each(function(){
            d3.select(this).attr("x", 22)
            d3.select(this).attr("y", 20)
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
                d.x = timeRescaled(d.event_start)
                d.length = timeRescaled(d.event_end) - d.x
                if (d.event_recurring == 1){
                    var year = d.event_start.getFullYear()
                    year -= Math.floor((d.x + d.length) / Math.round(width*k))
                    if (d.event_end.getMonth() < d.event_start.getMonth()) d.event_end.setFullYear(year + 1)
                    else d.event_end.setFullYear(year)
                    d.event_start.setFullYear(year)
                    var child = d.children.filter(c => year == +c.child_year)
                    if (child.length > 0){
                        child = child[0]
                        d.x = timeRescaled( new Date(child.child_start))
                        d.length = timeRescaled(new Date( child.child_end)) - d.x;
                        d3.select(this.parentNode).selectAll(".miniDate")
                                            .text(function(){
                                                if (child.child_fixed_date == 1){
                                                    if (child.child_start == data.child_end){
                                                        return d3.timeFormat('%d / %m')(new Date(child.child_start));
                                                    }
                                                    else{
                                                        return d3.timeFormat('%d/%m')(new Date(child.child_start)) + '  -  ' 
                                                            + d3.timeFormat('%d/%m')(new Date(child.child_end));
                                                    }
                                                }
                                                else{
                                                    return 'In ' + d3.timeFormat('%B')(new Date(child.child_start));
                                                }
                                            });
                    }
                    else {
                        d.x = timeRescaled(d.event_start)
                        d.length = timeRescaled(d.event_end) - d.x
                        d3.select(this.parentNode).selectAll(".miniDate")
                                                    .text(function(data){
                                                        if (data.fixed == 1){
                                                            if (data.start == data.end){
                                                                return d3.timeFormat('%d / %m')(new Date(data.start));
                                                            }
                                                            else{
                                                                return d3.timeFormat('%d/%m')(new Date(data.start)) + '  -  ' 
                                                                    + d3.timeFormat('%d/%m')(new Date(data.end));
                                                            }
                                                        }
                                                        else{
                                                            return 'In ' + d3.timeFormat('%B')(new Date(data.start));
                                                        }
                                                    });
                    }
                }
            })
            .attr('width', function(d){
                return radius*2 + d.length;
            })

        d3.selectAll('.data').selectAll('.datapoints').sort(function(x, y){
            return d3.descending(+x.x, +y.x);
        });
        showDetails();
    };
};
                

