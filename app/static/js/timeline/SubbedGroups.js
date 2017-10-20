var bottomBarHeight = 180;
var groupBoxDim = 150;

var padding = 20;

//create bottom bar 
d3.selectAll('svg')
        .append('g')
            .attr("class", "bottomMenu")
            .attr("transform", "translate("+0+","+(height-bottomBarHeight)+")")
            .attr('up', true)
            .append('rect')
                .attr('class', 'bottomBase')
                .style('fill', 'black')
                .style('opacity', 0.2)
                .attr('width', totalWidth)
                .attr('height', bottomBarHeight);

d3.selectAll('.bottomMenu').append('g').attr('class', 'agendas')

d3.select('.toggleGroupVisibility')
                .on('click', function(){
                    ToggleAgendaMenu();
                });

function AddGroupButtons(groups){
    //initialize toggle objects and bind color data
    var agendasContainer = d3.selectAll(".agendas").selectAll('g')
                                .data(groups)
                                .enter()
                                .append('g').attr('class', function(d){return d.name})
                                    .attr('transform', function(d, i){
                                        return "translate("+((groupBoxDim+padding)*i + padding)+","+((bottomBarHeight - groupBoxDim)/2)+")"
                                    })
                                    
    //add subscribed calendar boxes and click event handler
    agendasContainer
        .append("rect")
            .attr("width", groupBoxDim)
            .attr("height", groupBoxDim)
            .attr("rx", 20)
            .attr("ry", 20)
            .style("fill", function (d) {
                return d.color;
            })
            .on('click', function (d) {
                ToggleAgenda(d.color)
                if (d3.select(this).style("fill") == "darkgrey") { 
                    d3.select(this).style("fill", function () {return d.color;}) 
                }
                else { d3.select(this).style("fill", "darkgrey") }
            });

    agendasContainer
        .append("text")
            .attr("x", 20)
            .attr("y", 120)
            .style("font-size", 30)
            .text(function(d){return d.name}); 
};

//toggle up/down
function ToggleAgendaMenu(){
    var toggle;
    d3.selectAll('.bottomMenu')
        .transition()
        .duration(1000)
        .attr('transform', function(){
            toggle = d3.select(this).attr('up') === 'true'
            var move = toggle ? height : height-bottomBarHeight
            d3.selectAll('.scrollArea')
                .attr('height', function(){
                    return +d3.select(this).attr('height') + (toggle ? bottomBarHeight : -(bottomBarHeight))
                })
            d3.select(this).attr('up', !toggle)
            return "translate(0," + move + ")"
        })
    d3.select(".calendarToolbox")
        .transition()
        .duration(1000)
        .style("bottom", function(){
            return toggle ? '1px' : '181px'
        })
    if (toggle){
        d3.select('.toggleArrow')
            .text('arrow_drop_up')
    }
    else{
        d3.select('.toggleArrow')
                .text('arrow_drop_down')
    }
}

//toggle on/off
function ToggleAgenda(data) {
    d3.selectAll(".data").selectAll('.points')
        .filter(function(d){return d.color == data})
        .each(function(){
            d3.select(this.parentNode).style("display", function(){
                    return d3.select(this).style("display") == 'inline' ? 'none' : 'inline';
                })
            })      
    showDetails();
};