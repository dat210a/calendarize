var left_timeline_button = leftSideBar.append('g')
                                        .attr('class', 'left_timeline_button')
                                        .attr('opacity', 0)

left_timeline_button.append('text')
        .style('font-family', 'Material Icons')
        .attr('font-size', '50px')
        .attr('fill', 'lightgrey')
        .text('chevron_left')
        .attr('x', -70)
        .attr('y', 25)

left_timeline_button.append("rect")
        .attr('width', xPadding)
        .attr('height', height)
        .attr('x', -xPadding)
        .attr('y', -midScreen)
        .style("fill", "url(#left_linear_gradient)")

var right_timeline_button = rightSideBar.append('g')
                                        .attr('class', 'right_timeline_button')
                                        .attr('opacity', 0)

right_timeline_button.append('text')
    .style('font-family', 'Material Icons')
    .attr('font-size', '50px')
    .attr('fill', 'lightgrey')
    .text('chevron_right')
    .attr('x', 20)
    .attr('y', 25)

right_timeline_button.append("rect")
    .attr('width', xPadding)
    .attr('height', height)
    .attr('y', -midScreen)
    .style("fill", "url(#right_linear_gradient)")


var defsLeft = left_timeline_button.append("defs");
var defsRight = right_timeline_button.append("defs");

var leftLinearGradient = defsLeft.append("linearGradient")
                            .attr("id", "left_linear_gradient");
var rightLinearGradient = defsRight.append("linearGradient")
                            .attr("id", "right_linear_gradient");

leftLinearGradient
    .attr("x1", "0%")
    .attr("y1", "0%")
    .attr("x2", "100%")
    .attr("y2", "0%");

leftLinearGradient.append("stop") 
    .attr("offset", "0%")   
    .attr("stop-color", "rgba(0,0,0,0.5)");

leftLinearGradient.append("stop") 
    .attr("offset", "100%")   
    .attr("stop-color", "rgba(0,0,0,0)"); 

rightLinearGradient
    .attr("x1", "0%")
    .attr("y1", "0%")
    .attr("x2", "100%")
    .attr("y2", "0%");

rightLinearGradient.append("stop") 
    .attr("offset", "0%")   
    .attr("stop-color", "rgba(0,0,0,0)");

rightLinearGradient.append("stop") 
    .attr("offset", "100%")   
    .attr("stop-color", "rgba(0,0,0,0.5)"); 

    leftSideBar
    .on('mouseover', function(d){
        left_timeline_button.transition()
                            .duration(200)
                            .attr('opacity', 1)
    })
    .on('mouseout', function(d){
        left_timeline_button.transition()
                            .duration(200)
                            .attr('opacity', 0)
    })
    .on('click', function(){
        svg.call(zoom.translateBy, width/k)
    })

right_timeline_button
    .on('mouseover', function(d){
        right_timeline_button.transition()
                             .duration(200)
                             .attr('opacity', 1)
    })
    .on('mouseout', function(d){
        right_timeline_button.transition()
                             .duration(200)
                             .attr('opacity', 0)
    })
    .on('click', function(){
        svg.call(zoom.translateBy, -width/k)
    })