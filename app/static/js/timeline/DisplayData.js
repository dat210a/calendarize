
var timer = 0;
var firstAvailColor = 0;

var xOffset = d3.scaleLinear().domain([0, midScreen-60]).range([20, 70]);

var detailHeight = 80,
    detailWidth = 200;

//load data async
function load_data(){
    d3.queue()
        .defer(d3.json, '/get_data') //  /tz?tz=' + Intl.DateTimeFormat().resolvedOptions().timeZone)
        .await(ready);
}

function ready(error, allData){
    if (error || allData == null){
        console.log("Can't load the data")
        return;
    }

    datapoints = allData[1]
    groups = allData[0]
    
    // fix color tag
    groups.forEach(function(d){d.calendar_color = '#' + d.calendar_color;})

    // add groups / calendars
    AddGroupButtons(groups)

    // clear data before assigning new one
    // TODO figure out whether it's possible to do with update() enter() exit()
    d3.selectAll('.data').remove()
    if (datapoints.length == 0) return

    //sort data so its displayed from right to left
    //due to overlap
    var myData = datapoints.sort(function(x, y){
        return d3.descending(+x.event_start, +y.event_start);
    })

    //objects whith coordinates for detail boxes
    var detailsPoints = new Array(myData.length);
    for (i = 0; i < detailsPoints.length; i++){
        detailsPoints[i] = {'name': myData[i].event_name, 'start': myData[i].event_start, 'end': myData[i].event_end, 'fixed': myData[i].event_fixed_date};
    }

    //setup simulation based on data
    nodes = myData.concat(detailsPoints);
    simulation.nodes(nodes)
                .on('tick', ticked);

    //display data
    var dataGroup = d3.select(".timeline")
                        .insert('g', '.g-today')
                        .attr("class", "data")
                        .selectAll('.datapoints')
                            .data(myData)
                            .enter()
                                .append("g")
                                    .attr("class", function(d, i){return 'datapoints e' + d.event_id;})
                                    .style('display', 'inline')

    //initialize lines connecting point on timeline and detail boxes
    var connections = dataGroup
                        .append('path')
                            .attr('class', 'connector shadow')
                            .attr('opacity', '0.99')
                            .style("stroke-width", '2')
                            .style("stroke", '#3D4148')
                            .style("fill", 'none')
                            .style('display', 'none');
                            
    //initialize points on the timeline
    var points = dataGroup.append("rect")
                            .attr('class', 'points shadow')
                            .style('pointer-events', 'visible')
                            .style("fill", function (d) {
                                d.calendar_color = groups.filter(function(gr){
                                    return gr.calendar_id == d.event_calendar_id
                                })[0].calendar_color
                                return d.calendar_color
                            })
                            .attr("height", radius*2)
                            .attr("rx", radius)
                            .attr("x", function(d){
                                d.event_start = new Date(d.event_start)
                                return d.x = time(d.event_start)
                            })
                            .attr("y", function(d){
                                d.y = 0;
                                return d.y - radius;
                            })
                            .attr("width", function(d){
                                d.event_end = new Date(d.event_end)
                                d.length = time(d.event_end) - d.x
                                return radius*2 + d.length;
                            })
                            .on('click', function (d, i) {
                                current_event = d
                                display_event();
                            });


    //initialize detail boxes
    var detailContainer = dataGroup
                            .append('g')
                                .attr('class', 'detailContainer')
                                .style('display', 'none')
                                

    detailContainer      
        .append("rect")
            .attr('class', 'detailBox shadow')
            .attr("width", detailWidth)
            .attr("height", detailHeight)
            .attr("rx", 2)
            .attr("ry", 2)


    //bind data (locations) to lines
    connections
        .data(detailsPoints)
        .attr('d', function(d, i){
            return link(d, this.parentNode.__data__);
        });

    //bind data (locations) to detail boxes
    detailContainer 
        .data(detailsPoints)
        .each(function(d){d.y = 0})
        .on('click', function (d, i) {
            current_event = this.parentNode.__data__
            display_event();
        });

    
    detailContainer
        .append('text')
            .attr('class', 'miniID')
            .attr('x', 15)
            .attr('y', 30)
            .style("font-size", 30)
            .style('fill', '#F1F0F0')
            .text(function(d){
                return d.name;
            })
            .each(function(){
                short_text(d3.select(this), detailWidth, 25)
            });

    detailContainer
        .append('line')
            .attr('x1', 10)
            .attr('x2', detailWidth - 10)
            .attr('y1', detailHeight/2)
            .attr('y2', detailHeight/2)
            .attr('stroke-width', 1)
            .style('stroke', '#F1F0F0');
                
    detailContainer
        .append('text')
            .attr('class', 'miniDate')
            .attr('x', 15)
            .attr('y', detailHeight/2 + 30)
            .style("font-size", 25)
            .style('fill', '#F1F0F0')
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

    dataGroup
        .each(function(data){
            d3.select(this).selectAll('.detailBox')
                .style('fill', function(){return data.calendar_color;});
        });
    
    // load, center to and display new created event
    if (current_event == null) svg.call(zoom.translateBy, 0)
    else{
        current_event = d3.selectAll(".datapoints").filter(d => d.event_id == current_event.event_id).data()[0]
        display_event()
        resetView(new Date(current_event.event_start))
    }
};

//update data position after forces have taken effect
function ticked() {
    // if (timer == 0) {            //for debuging purposes - only allows one tick 
    //     simulation.stop()
    // }
    timer++;

    var selection = d3.selectAll('.datapoints')
                        .filter(function(){
                            return d3.select(this).style('display') == 'inline';
                        })

    selection.selectAll('.points')
        .attr("x", function (d) {
            return d.x - radius;
        })
        .attr("y", function (d) {
            d.y = d.y > 0 ? 0 : d.y;
            return d.y - radius;
        })
    
    selection.selectAll('.detailContainer')
        .attr('transform', function(d){
            var parent = this.parentNode.__data__;
            d.x = parent.x + parent.length/2 + xOffset(Math.abs(d.y));
            return 'translate(' + d.x + ',' + (d.y-detailHeight/2) + ')';
        });

    selection.selectAll('.connector')
        .attr('d', function(d, i){
            return link(d, this.parentNode.__data__);
        });
};

function showDetails(){
    //how many points are displayed
    if (!d3.selectAll('.data').empty()){
        var pointsOnScreen = d3.selectAll('.data').selectAll('.datapoints')
            .filter(function(d){
                return ((d.x > 0) && (d.x < width) && d3.select(this).style("display") == 'inline');
            }).data().length

        var selection = d3.selectAll('.data').selectAll('.detailContainer');
        if (k < 3.3 && tresholdNumPoints < pointsOnScreen){
            if (selection.style('display') == 'inline'){
                selection
                    .transition()
                    .duration(500)
                    .attr('transform', function(d){
                        return 'translate(' + d.x + ',' + 0 + ')scale(0)';
                    })
                    .on("start", function(){
                        d3.selectAll('.data').selectAll('path').style('display', 'none');
                    })
                    .on("end", function(){d3.select(this).style('display', 'none')});
            };
        }
        else {
            if (selection.style('display') == 'none'){
                selection
                    .transition()
                    .duration(500)
                    .attr('transform', function(d){
                        var parent = this.parentNode.__data__;
                        d.x = parent.x + parent.length/2 + xOffset(Math.abs(d.y));
                        return 'translate(' + d.x + ',' + (d.y-detailHeight/2) + ')scale(1)';
                    })
                    .on("start", function(){
                        d3.select(this).style('display', 'inline')
                            .attr('transform', function(d){
                                return 'translate(' + d.x + ',' + 0 + ')scale(0)';
                            })
                    })
                    .on("end", function(){ 
                        d3.selectAll('.miniID')
                            .attr('x', 15)
                            .attr('y', 30)
                        d3.selectAll('.miniDate')
                            .attr('x', 15)
                            .attr('y', detailHeight/2 + 30)                              
                        d3.selectAll('.data').selectAll('path').style('display', 'inline');
                    })
            } 
        }
        simUpdate();
    }
}

//toggle on/off
function ToggleAgenda(cid) {
    d3.selectAll(".data").selectAll('.points')
        .filter(function(d){return d.event_calendar_id == cid})
        .each(function(){
            d3.select(this.parentNode).style("display", function(){
                    return d3.select(this).style("display") == 'inline' ? 'none' : 'inline';
                })
            })
    showDetails();
};

// text cutoff
function short_text(self, textWidth, endTextBuffer) {
    var textLength = self.node().getComputedTextLength(),
        text = self.text();
    while (textLength > (textWidth - endTextBuffer)) {
        text = text.slice(0, -1);
        self.text(text + '...');
        textLength = self.node().getComputedTextLength();
    }
}

//draw lines data-details
function link(target, source) {
    var x1 = Math.round(source.x + source.length/2);
    var y1 = Math.round(source.y);
    var x2 = Math.round(target.x);
    var y2 = Math.round(target.y);
    return "M" + x1 + "," + y1
    + "L" + (x2 - 20) + ',' + y2
    + "L" + x2 + ',' + y2;
};
