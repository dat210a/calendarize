function resize(){
    oldWidth = width;
    totalWidth = $('.timelineScreen').width()
    totalHeight = $('.timelineRow').height();
    width = totalWidth - 2*xPadding,
    height = totalHeight;
    xScale = d3.scaleLinear().domain([0, 365]).range([0, width]);
    //main display elements
    svg
        .attr('width', totalWidth)
        .attr('height', totalHeight-10)
    d3.select('.scrollArea').attr("width", width)
                            .attr('height', (height-bottomBarHeight))
    d3.select('.midLine').attr("x2", width)
    d3.select('.Year').attr('transform', 'translate('+ width/2 +',' + 75 +')')
    rightSideBar.attr('transform', 'translate(' 
        + (xPadding + width) + ',' 
        + midScreen + ')')
    d3.select('.bottomBase').attr('width', totalWidth)
    d3.select('.bottomMenuButton')
        .attr('transform', function(){
            return 'translate('+(xPadding + width/2)+','+15+')'
    })
    //bottom bar
    d3.select('.bottomMenu')
            .attr("transform", "translate("+0+","+(height-bottomBarHeight)+")")

    //side panel
    d3.select('.sidePanel').style('height', totalHeight)

    //realign movables
    var oldX = d3.zoomTransform(d3.select('.scrollArea').node()).x
    d3.select('.scrollArea').call(zoom.translateBy, oldX/oldWidth*(width - oldWidth)/k, 0);
    simUpdate();
 }

$( window ).resize(function(){return resize()});
$( document ).ready(function(){return resize()});