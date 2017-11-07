var bottomBarHeight = 180;
var groupBoxDim = 150;

var padding = 20;

//create bottom bar 
var bottomMenu = svg.append('g')
                        .attr("class", "bottomMenu")
                        .attr("transform", "translate("+0+","+(height-bottomBarHeight)+")")
                        .attr('up', true)

bottomMenu.append('rect')
    .attr('class', 'bottomBase')
    .attr('width', totalWidth)
    .attr('height', bottomBarHeight);

bottomMenu.append('g')
            .attr('class', 'agendas')

d3.select('.toggleGroupVisibility')
                .on('click', function(){
                    ToggleAgendaMenu();
                });

function AddGroupButtons(groups){
    //initialize toggle objects and bind color data
    var agendasContainer = d3.selectAll(".agendas").selectAll('g')
                                .data(groups)
                                .enter()
                                .append('g').attr('class', function(d){return 'group ' + d.calendar_name})
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
                return d.calendar_color;
            })
            .on('click', function (d) {
                ToggleAgenda(d.calendar_color)
                if (d3.select(this).style("fill") == "darkgrey") { 
                    d3.select(this).style("fill", function (d) {return d.calendar_color;}) 
                }
                else { d3.select(this).style("fill", "darkgrey") }
            });

    agendasContainer
        .append("text")
            .attr("x", 20)
            .attr("y", 120)
            .style("font-size", 30)
            .text(function(d){return d.calendar_name})
            .each(function(){
                short_text(d3.select(this), groupBoxDim, 30)
            });
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

//toggle up/down
function ToggleAgendaMenu(){
    var toggle;
    d3.selectAll('.bottomMenu')
        .transition()
        .duration(1000)
        .attr('transform', function(){
            toggle = d3.select(this).attr('up') === 'true'
            var move = toggle ? height : height-bottomBarHeight
            // d3.selectAll('.scrollArea')
            //     .attr('height', function(){
            //         return +d3.select(this).attr('height') + (toggle ? bottomBarHeight : -(bottomBarHeight))
            //     })
            d3.select(this).attr('up', !toggle)
            return "translate(0," + move + ")"
        })
    d3.select(".calendarToolbox")
        .transition()
        .duration(1000)
        .style("bottom", function(){
            return toggle ? '5px' : '180px'
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
        .filter(function(d){return d.calendar_color == data})
        .each(function(){
            d3.select(this.parentNode).style("display", function(){
                    return d3.select(this).style("display") == 'inline' ? 'none' : 'inline';
                })
            })      
    showDetails();
};