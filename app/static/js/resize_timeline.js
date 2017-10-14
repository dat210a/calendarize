
var margin = 6;

function resize(){
    oldWidth = width;
    oldHeight = height;
    totalWidth = $('.timelineScreen').width();
    totalHeight = $('.timelineRow').height()-margin;

    //header: 70px footer: 64px svg min-height: 300px
    // var winH = $(window).height()-70-64-margin;
    // if (winH > 300 && winH < totalHeight) totalHeight = winH;

    // set dimensions
    width = totalWidth - 2*xPadding,
    height = totalHeight;
    
    // Scales
    time.range([0, width]);

    //frames
    $('.eventDetails').height(totalHeight-margin);

    //main display elements
    svg
        .attr('width', totalWidth)
        .attr('height', totalHeight)
    d3.select('.scrollArea').attr("width", width)
                            .attr('height', (height-bottomBarHeight))
    d3.select('.midLine').attr("x2", width)
    d3.select('.Year').attr('transform', 'translate('+ width/2 +',' + 75 +')')
    rightSideBar
        .attr('transform', 'translate(' 
            + (xPadding + width) + ',' 
            + midScreen + ')')
        .select('rect')
            .attr('height', totalHeight)
    leftSideBar
        .attr('transform', 'translate(' 
            + xPadding + ',' + midScreen + ')')
        .select('rect')
            .attr('height', totalHeight)
    d3.select('.bottomBase').attr('width', totalWidth)

    //bottom bar
    d3.select('.bottomMenu')
            .attr("transform", function(){
                var up = d3.select(this).attr('up') === 'true';
                var move = up ? height-bottomBarHeight : height;
                return "translate("+0+","+move+")";
            })

    //side panel
    d3.select('.sidePanel').style('height', totalHeight)

    //realign movables
    var oldX = d3.zoomTransform(d3.select('.scrollArea').node()).x
    d3.select('.scrollArea').call(zoom.translateBy, oldX/oldWidth*(width - oldWidth)/k, 0);
 }

$( window ).resize(function(){resize()});
$( document ).ready(function(){
    resize();
    resetView();
});