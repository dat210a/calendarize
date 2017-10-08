var bottomBarHeight = 200;

var groupBoxWidth = 150,
    groupBoxHeight = 150;

var padding = 20;

//create bottom bar 
d3.selectAll('svg')
        .append('g')
        .attr("class", "bottomMenu")
        .attr("transform", "translate("+0+","+(height-bottomBarHeight)+")")
        .attr('up', true)
        .append('rect')
            .style('fill', 'transparent')
            .attr('width', width)
            .attr('height', bottomBarHeight);
            
//add toggle button
d3.selectAll('.bottomMenu')
    .append('g')
        .attr("class", 'bottomMenuButton')
        .attr('transform', function(){
             return 'translate('+(xPadding + width/2)+','+15+')'
        })
        .append('rect')
            .attr('width', 100)
            .attr('height', 40)
            .attr('x', -50)
            .attr('y', -37)
            .attr("stroke", "black")
            .on('click', ToggleAgendaMenu);

d3.selectAll('.bottomMenuButton')
    .append('text')
        .text('===')
        .attr("font-size", 50)
        .on('click', ToggleAgendaMenu);

d3.selectAll('.bottomMenu').append('g').attr('class', 'agendas')

function AddGroupButtons(groups){
    //initialize toggle objects and bind color data
    var agendasContainer = d3.selectAll(".agendas").selectAll('g')
                                .data(groups)
                                .enter()
                                .append('g').attr('class', function(d){return d.name})
                                    .attr('transform', function(d, i){
                                        return "translate("+((groupBoxWidth+padding)*i + padding)+","+30+")"
                                    })
                                    
    //add subscribed calendar boxes and click event handler
    agendasContainer
        .append("rect")
            .attr("width", groupBoxWidth)
            .attr("height", groupBoxHeight)
            .attr("rx", 20)
            .attr("ry", 20)
            .style("fill", function (d) {
                return d.color;
            })
            .on('click', function (d) {
                ToggleAgenda(d.color)
                if (d3.select(this).style("fill") == "lightgrey") { 
                    d3.select(this).style("fill", function () {return d.color;}) 
                }
                else { d3.select(this).style("fill", "lightgrey") }
            });

    agendasContainer
        .append("text")
            .style('text-anchor', 'start')
            .attr("x", 20)
            .attr("y", 120)
            .style("font-size", 30)
            .text(function(d){return d.name}); 
};

//toggle up/down
function ToggleAgendaMenu(){
    d3.selectAll('.bottomMenu')
        .transition()
        .duration(1000)
        .attr('transform', function(){
            var toggle = d3.select(this).attr('up') === 'true'
            var move = toggle ? height-22 : height-bottomBarHeight
            d3.selectAll('.scrollArea')
                .attr('height', function(){
                    return +d3.select(this).attr('height') + (toggle ? bottomBarHeight-30 : -(bottomBarHeight-30))
                })
            d3.select(this).attr('up', !toggle)
            return "translate(0," + move + ")"
        })
}

//toggle on/off
function ToggleAgenda(data) {
    d3.selectAll(".data").selectAll('line')
        .filter(function(d){return d.color == data})
        .each(function(){
            d3.select(this.parentNode).style("display", function(){
                return d3.select(this).style("display") == 'inline' ? 'none' : 'inline';
                })
            })      
    simUpdate()
};