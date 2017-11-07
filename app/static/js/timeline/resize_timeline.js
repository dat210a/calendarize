

function resize(){
    oldWidth = width;
    oldHeight = height;
    totalWidth = $('.timelineScreen').width();
    totalHeight = $('.bodyMain').height();

    // set dimensions
    width = totalWidth - 2*xPadding;
    height = totalHeight;
    midScreen = height/2;
    
    // Scales
    time.range([0, width]);

    //frames
    // $('#sidebar').css("min-height", totalHeight + "px" )
    //               .css("max-height", totalHeight + "px" );

    //background elements
    svg
        .attr('width', totalWidth)
        .attr('height', height)
    // d3.select('.scrollArea').attr("width", width)
    //                         .attr('height', height)
    d3.select('.Year').attr('transform', 'translate('+ width/2 +',' + 75 +')')

    //sides
    rightSideBar
        .attr('transform', 'translate(' 
            + (xPadding + width) + ',' 
            + midScreen + ')')
        .selectAll('rect')
            .attr('height', height)
            .attr('y', -midScreen)

    leftSideBar
        .attr('transform', 'translate(' 
            + xPadding + ',' + midScreen + ')')
        .selectAll('rect')
            .attr('height', height)
            .attr('y', -midScreen)

    //bottom bar
    d3.select('.bottomMenu')
            .attr("transform", function(){
                var up = d3.select(this).attr('up') === 'true';
                var move = up ? height-bottomBarHeight : height;
                return "translate(0," + move + ")"
            })
            .select('.bottomBase')
                .attr('width', totalWidth)

    //readjust line position
    d3.select('.timeline')
        .attr("transform", 'translate(' +xPadding+ ','+midScreen+')')

    //realign movables
    var oldX = d3.zoomTransform(svg.node()).x
    svg.call(zoom.translateBy, oldX/oldWidth*(width - oldWidth)/k, 0);
 }

$( window ).resize(function(){resize()});
$( document ).ready(function(){
    resize();
    resetView(new Date);
});