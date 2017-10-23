var timer = 0;

var xOffset = d3.scaleLinear().domain([0, midScreen-60]).range([20, 70]);
var color = d3.scaleOrdinal(d3.schemeCategory10);

var detailHeight = 100,
    detailWidth = 200;

//load data async
//TODO get data from SQL
d3.queue()
    .defer(d3.json, '/get_data')
    // .defer(d3.csv, "/static/assets/random_chart.csv")
    .await(ready);

function ready(error, datapoints){
    if (error){
        console.log("Can't load the data")
        return;
    }
    console.log(datapoints)

    //populate groups on the bottom menu
    var setOfGroups = [... new Set(datapoints.map(function(d){return d.group;}))];
    var groups = new Array(setOfGroups.length)
    setOfGroups.forEach(function(d, i){groups[i] = {name: setOfGroups[i], color: color(i)}})
    AddGroupButtons(groups)

    //sort data so its displayed from right to left
    //due to overlap
    var myData = datapoints.sort(function(x, y){
        return d3.descending(+x.start_date, +y.start_date);
    })

    //objects whith coordinates for detail boxes
    var detailsPoints = new Array(myData.length);
    for (i = 0; i < detailsPoints.length; i++){
        detailsPoints[i] = {'id': myData[i].id, 'date': myData[i].start_date};
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
                                    .attr("class", function(d){return 'datapoints ' + d.id;})
                                    .style('display', 'inline')
                            
    var points = dataGroup.append("rect")
                            .attr('class', 'points')
                            .style('pointer-events', 'visible')
                            .style("fill", function (d) {
                                d.color = groups.filter(function(gr){return gr.name == d.group})[0].color
                                return d.color
                            })
                            .attr("height", radius*2)
                            .attr("rx", radius)
                            .attr("x", function(d){
                                return d.x = time(parse(d.start_date))
                            })
                            .attr("y", function(d){
                                d.y = 0;
                                return d.y - radius;
                            })
                            .attr("width", function(d){
                                d.length = time(parse(d.end_date)) - d.x
                                return radius*2 + d.length;
                            })
                            .on('click', function (d, i) {
                                display(d);
                            });

    //initialize lines connecting point on timeline and detail boxes
    var connections = dataGroup
                        .append('path')
                            .attr('class', 'connector')
                            .attr("stroke", 'darkgrey')
                            .style("fill", 'none')
                            .style('display', 'none');

    //initialize detail boxes
    var detailContainer = dataGroup
                            .append('g')
                                .attr('class', 'detailContainer')
                                .style('display', 'none')

    detailContainer      
        .append("rect")
            .attr('class', 'detailBox')
            .attr("width", detailWidth)
            .attr("height", detailHeight)


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
            .style("font-size", 20)
            .text(function(){
                return this.parentNode.__data__.id;
            });

    detailContainer
        .append('line')
            .attr('x1', 5)
            .attr('x2', detailWidth - 10)
            .attr('y1', detailHeight/2 - 10)
            .attr('y2', detailHeight/2 - 10)
            .attr('stroke-width', 2)
            .attr('stroke', 'black');
                
    detailContainer
        .append('text')
            .attr('class', 'miniDate')
            .attr('x', 15)
            .attr('y', detailHeight/2 + 30)
            .style("font-size", 30)
            .text(function(){
                return d3.timeFormat('%d / %m')(parse(this.parentNode.__data__.date));
            });

    dataGroup
        .each(function(data){
            d3.select(this).selectAll('.detailBox')
                .style('fill', function(){return data.color;});
        });
};

//update data position after forces have taken effect
function ticked() {
    // if (timer == 1) {            //for debuging purposes - only allows one tick 
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
                            return 'translate(' + d.x + ',' + (d.y-50) + ')scale(1)';
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
