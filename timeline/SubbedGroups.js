var dataPlaceHolder = ["Work", "School", "House", "Family", "Misc"]

var bottomBarHeight = 200;

var agendasContainer = d3.selectAll('svg')
                            .append('g')
                            .attr("class", "agendas")
                            .attr("transform", "translate("+0+","+(height-bottomBarHeight)+")")
                            .attr('up', true)
                        .selectAll(".agendas")
                            .data(dataPlaceHolder)
                            .enter()
                            .append('g').attr('class', function(d){return d})
                                .attr('transform', function(d, i){
                                    return "translate("+(170*i + 20)+","+30+")"
                                })

d3.selectAll('.agendas')
    .insert('g', 'g')
        .attr('class', 'bottomMenu')
        .append('rect')
            .attr('fill', 'transparent')
            .attr('width', width)
            .attr('height', bottomBarHeight);

d3.selectAll('.bottomMenu')
    .append('g')
        .attr("class", 'bottomMenuButton')
        .attr('transform', function(){
             return 'translate('+(xPadding + width/2)+','+15+')'
        })
        .append('rect')
            .attr('fill', 'white')
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

agendasContainer
    .append("rect")
        .attr("width", 150)
        .attr("height", 150)
        .attr("rx", 20)
        .attr("ry", 20)
        .attr("fill", function (d, i) {
        return color(i);
        })
        .on('click', function (d, i) {
            ToggleAgenda(i)
            var tempColor = d3.select(this).attr("fill")
            if (tempColor == "lightgrey") { 
                d3.select(this).attr("fill", function () {return color(i);}) 
            }
            else { d3.select(this).attr("fill", "lightgrey") }
        });

agendasContainer
    .append("text")
        .style('text-anchor', 'start')
        .attr("x", 20)
        .attr("y", 120)
        .style("font-size", 30)
        .text(function(d){return d}); 

function ToggleAgendaMenu(){
    d3.selectAll('.agendas')
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
};

function ToggleAgenda(data) {
    d3.selectAll(".data").selectAll('line')
        .filter(function(d){return +d.color == data})
        .each(function(){
            d3.select(this.parentNode).style("display", function(){
                return d3.select(this).style("display") == 'inline' ? 'none' : 'inline';
                })
            })      
    simUpdate()
};