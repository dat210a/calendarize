
var timer = 0;

var xOffset = d3.scaleLinear().domain([0, midScreen-60]).range([20, 70]);
var color = d3.scaleOrdinal(['#f57c00', '#d32f2f', '#c2185b', '#7b1fa2', '#512da8', '#1976d2', '#0097a7', '#689f38']);

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
    
    groups.forEach(function(d, i){d.color = color(i)})
    AddGroupButtons(groups)

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
        detailsPoints[i] = {'name': myData[i].event_name, 'start': myData[i].event_start, 'end': myData[i].event_end};
    }

    //setup simulation based on data
    nodes = myData.concat(detailsPoints);
    simulation.nodes(nodes)
                .on('tick', ticked);

    //divide what forces affect which objects
    dataGravity.initialize(myData);
    detailsGravity.initialize(detailsPoints);

    //display data
    var dataGroup = d3.select(".timeline")
                        .insert('g', '.g-today')
                        .attr("class", "data")
                        .selectAll('.datapoints')
                            .data(myData)
                            .enter()
                                .append("g")
                                    .attr("class", function(d, i){return 'datapoints ' + i;})
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
                            
    var points = dataGroup.append("rect")
                            .attr('class', 'points shadow')
                            .style('pointer-events', 'visible')
                            .style("fill", function (d) {
                                d.color = groups.filter(function(gr){
                                    return gr.calendar_id == d.event_calendar_id
                                })[0].color
                                return d.color
                            })
                            .attr("height", radius*2)
                            .attr("rx", radius)
                            .attr("x", function(d){
                                var startDate = new Date(d.event_start)
                                d.event_year = d3.timeFormat('%Y')(startDate)
                                return d.x = time(startDate)
                            })
                            .attr("y", function(d){
                                d.y = 0;
                                return d.y - radius;
                            })
                            .attr("width", function(d){
                                d.length = time(new Date(d.event_end)) - d.x
                                return radius*2 + d.length;
                            })
                            .on('click', function (d, i) {
                                display(d);
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
        .on('click', function (d, i) {
            display(this.parentNode.__data__);
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
                if (data.start == data.end){
                    return d3.timeFormat('%d / %m')(new Date(this.parentNode.__data__.start));
                }
                else{
                    return d3.timeFormat('%d/%m')(new Date(this.parentNode.__data__.start)) + '  -  ' 
                         + d3.timeFormat('%d/%m')(new Date(this.parentNode.__data__.end));
                }
            });

    dataGroup
        .each(function(data){
            d3.select(this).selectAll('.detailBox')
                .style('fill', function(){return data.color;});
        });
    
    if (current_event_id == null) d3.select('svg').call(zoom.translateBy, 0)
    else{
        d3.select('svg').call(zoom.translateBy, 0) // TODO center to event
        event_data = d3.selectAll(".datapoints").filter(d => d.event_id == current_event_id).data()[0]
        display(event_data)
    }
};

//update data position after forces have taken effect
function ticked() {
    // if (timer == 0) {            //for debuging purposes - only allows one tick 
    //     simulation.stop()
    // }
    // timer++;

    var selection = d3.selectAll('.datapoints')
                        .filter(function(){
                            return d3.select(this).style('display') == 'inline';
                        })

    selection.selectAll('.points')
        .attr("x", function (d) {
            return d.x;
        })
        .attr("y", function (d) {
            d.y = d.y > 0 ? 0 : d.y;
            return d.y -radius;
        })
    
    selection.selectAll('.detailContainer')
        .attr('transform', function(d){
            var parent = this.parentNode.__data__;
            d.x = parent.x + parent.length*k/2 + xOffset(Math.abs(d.y));
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

        if (k < 3.3 && tresholdNumPoints < pointsOnScreen){
            if (d3.selectAll('.data').selectAll('.detailContainer').style('display') == 'inline'){
                d3.selectAll('.data').selectAll('.detailContainer')
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
            if (d3.selectAll('.data').selectAll('.detailContainer').style('display') == 'none'){
                d3.selectAll('.data').selectAll('.detailContainer')
                            .transition()
                            .duration(500)
                            .attr('transform', function(d){
                                var parent = this.parentNode.__data__;
                                d.x = parent.x + parent.length*k/2 + xOffset(Math.abs(d.y));
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

//draw lines data-details
function link(target, source) {
    var x1 = Math.round(source.x + source.length*k/2 + radius);
    var y1 = Math.round(source.y);
    var x2 = Math.round(target.x);
    var y2 = Math.round(target.y);
    return "M" + x1 + "," + y1
    + "L" + (x2 - 20) + ',' + y2
    + "L" + x2 + ',' + y2;
};
