
var timer = 0;

var xOffset = d3.scaleLinear().domain([0, midScreen-60]).range([20, 70]);
var color = d3.scaleOrdinal(d3.schemeCategory10);

var detailHeight = 100,
    detailWidth = 200;

//force pull towards the middle line
var dataGravity = d3.forceY(0).strength(0.1);
var detailsGravity = d3.forceY(function(d){
                                return d.y > 0 ? 100 : -170
                            }).strength(0.5);

//instantiate simulation
var simulation = d3.forceSimulation()
                        .force('gravity', dataGravity)
                        .force('detailsGravity', detailsGravity)
                        .force('pointsCollider', pointCollider)
                        .force('detailsBoxCollider', detailBoxCollider);

//collision force for points on the line
function pointCollider(alpha){
    var nodes = d3.selectAll('.data')
                    .selectAll('g')
                        .filter(function(d){
                            return d3.select(this).style('display') == 'inline';
                        })
                        .selectAll('line')
                            .data().reverse();
    for (i = 0, n = nodes.length; i < n; i++){
        capsule = nodes[i];
        for (j = i + 1; j < n; ++j){
            point = nodes[j];
            var dist = capsuleCollider(capsule, point, capsule.duration*k);
            if (dist < radius*2+1) {
                if (point.duration <= capsule.duration) point.vy -= (radius*2+1 - dist);
                else capsule.vy -= (radius*2+1 - dist);
            }
        }
    }
}

//collision force for detail boxes
function detailBoxCollider(alpha){
    var nodes = d3.selectAll('.data').selectAll('rect').data();
    d3.selectAll('.data').selectAll('rect')
        .each(function(point, i){
            var pParent = this.parentNode.__data__;
            d3.selectAll('.data').selectAll('rect')
                .filter(function(d, j){return j > i;})
                .each(function(capsule, j){
                    var cParent = this.parentNode.__data__;
                    var dist = detailsCollider(capsule, point, detailWidth, cParent, pParent);
                    if (dist < 50*2+5) {
                        if (capsule.y > 0) capsule.vy += (50*2+5 - dist);
                        else capsule.vy -= (50*2+5 - dist);
                    }
                })
        })
}

//load data async
//TODO get data from SQL
d3.queue()
    .defer(d3.csv, "/static/assets/random_chart.csv")
    .await(ready);

function ready(error, datapoints){
    if (error){
        console.log("Can't load the data")
        return;
    }

    //populate groups on the bottom menu
    var setOfGroups = [... new Set(datapoints.map(function(d){return d.group;}))];
    var groups = new Array(setOfGroups.length)
    setOfGroups.forEach(function(d, i){groups[i] = {name: setOfGroups[i], color: color(i)}})
    AddGroupButtons(groups)

    //sort data so its displayed from right to left
    //due to overlap
    var myData = datapoints.sort(function(x, y){
        return d3.descending(+x.date, +y.date);
    })

    //objects whith coordinates for detail boxes
    var detailsPoints = new Array(myData.length);
    for (i = 0; i < detailsPoints.length; i++){
        detailsPoints[i] = {'id': myData[i].id};
    }

    //setup simulation based on data
    nodes = myData.concat(detailsPoints);
    simulation.nodes(nodes)
                .on('tick', ticked);

    //divide what forces affect which objects
    dataGravity.initialize(myData);
    detailsGravity.initialize(detailsPoints);

    //display data
    var dataGroup = d3.select(".timeLine").append('g').attr("class", "data").selectAll('g')
                    .data(myData)
                    .enter()
                        .append("g")
                        .attr("class", function(d){return d.id;});
                            
    var points = dataGroup.append("line")
                            .attr("stroke", function (d) {
                                d.color = groups.filter(function(gr){return gr.name == d.group})[0].color
                                return d.color
                            })
                            .attr("stroke-width", radius*2)
                            .attr("stroke-linecap", "round")
                            .attr("x1", function(d){
                                return d.x = xScale(d.date);
                            })
                            .attr("x2", function(d){
                                d.duration = xScale(d.duration);
                                return d.x + d.duration*k;
                            })
                            .attr("y1", function(d){
                                return d.y = 1;
                            })
                            .attr("y2", 1)
                            .on('click', function (d, i) {
                                console.log (d);
                            });

    //initialize lines connecting point on timeline and detail boxes
    var connections = dataGroup
                        .append('path')
                            .attr('class', 'detail')
                            .attr("stroke", 'darkgrey')
                            .style("fill", 'none')
                            .style('display', 'none');

    //initialize detail boxes'
    //TODO has to use transform, so its easier to display data
    var details = dataGroup
                    .append("rect")
                        .attr('class', 'detail')
                        .attr("width", detailWidth)
                        .attr("height", detailHeight)
                        .style('display', 'none');

    //bind data (locations) to lines
    connections
            .data(detailsPoints)
            .attr('d', function(d, i){
                return link(d, this.parentNode.__data__);
            });

    //bind data (locations) to detail boxes
    details 
            .data(detailsPoints)
            .attr("y", function(d,i){
                d.y = -midScreen/2;
                return d.y - 50;
            })

    points.each(function(data){
            d3.select(this.parentNode).selectAll('rect')
                .attr("x", function(d){
                        return d.x = data.x + data.duration/2;
                    })
                .style('fill', function(){return data.color;});
        });

    //update data position after forces have taken effect
    function ticked() {
        // if (timer == 1) {            //for debuging purposes - only allows one tick 
        //     simulation.stop()
        // }
        // timer++;

        points
            .attr("x1", function (d) {
                return d.x;
            })
            .attr("x2", function (d) {
                return d.x + d.duration*k;
            })
            .attr("y1", function (d) {
                return d.y = d.y > 0 ? 0 : d.y;
            })
            .attr("y2", function (d) {
                return d.y;
            });
        
        details
            .attr("x", function(d){
                var parent = this.parentNode.__data__;
                d.x = parent.x + parent.duration*k/2 + xOffset(Math.abs(d.y));
                return d.x;
            })
            .attr("y", function(d){
                return d.y - 50;
            });
        connections
            .attr('d', function(d, i){
                return link(d, this.parentNode.__data__);
            });
    };
};

//update simulation based on user changes
function simUpdate(){
    timer = 0;
    simulation
        .alpha(1)
        .restart();
};

//draw lines data-details
function link(target, source) {
    var x1 = source.x + source.duration*k/2;
    var y1 = source.y;
    var x2 = target.x;
    var y2 = target.y;
    return "M" + x1 + "," + y1
    + "L" + (x2 - 20) + ',' + y2
    + "L" + x2 + ',' + y2;
};

// capsule colliders distance functions
function capsuleCollider(capsule, point, duration){
    return distToCapsule(capsule.x + capsule.vx, 
                         capsule.y + capsule.vy, 
                         point.x + point.vx, 
                         point.y + point.vy, 
                         duration);
};

function detailsCollider(capsule, point, duration, cParent, pParent){
    cx = cParent.x + cParent.duration*k/2 + xOffset(Math.abs(capsule.y + capsule.vy));
    px = pParent.x + pParent.duration*k/2 + xOffset(Math.abs(point.y + point.vy));
    if (px > cx + detailWidth + 25) return detailWidth;
    return distToCapsule(cx, capsule.y + capsule.vy, px, point.y + point.vy, duration);
};

// Capsule Collider helper functions
function sqr(x){
    return x*x;
};

function dist2(x1, y1, x2, y2){
    return sqr(x1 - x2) + sqr(y1 - y2);
};

function distToCapsule(cx, cy, px, py, duration) {
    if (duration == 0) return Math.sqrt(dist2(px, py, cx, cy));
    var t = (px - cx) / duration;
    t = Math.max(0, Math.min(1, t));
    return Math.sqrt(dist2(px, py, cx + t * duration, cy));
};
