

var totalWidth = 900;
var totalHeight = 670;
var xPadding = 75;

var width = totalWidth - 2*xPadding,
    height = totalHeight;

var midScreen = height / 2;
var bottomOffset = 200;

var radius = 8;

var tresholdNumPoints = 8;
var k = 1;

var parse = d3.timeParse('%_m/%_d/%Y');
var time = d3.scaleTime()
                .domain([new Date('1/1/2020'), new Date('12/31/2020')])
                .range([0, width]);

var axis = d3.axisBottom(time)
                .tickFormat(d3.timeFormat('%b'))
                .tickArguments([d3.timeMonth.every(1)])
                .tickPadding(15)
                .tickSize(15)

//create canvas and all basic timeline objects
var svg = d3.select('svg')
                    .attr('width', totalWidth)
                    .attr('height', height)
                    .attr("transform", "translate(" + 0 + "," + 5 + ")")

svg.append('g')
        .attr("class", "background_items")
        .attr("transform", "translate(" + xPadding + ", 0)")
        .append('rect')
            .attr('class', 'scrollArea')
            .attr("height", height - bottomOffset)
            .attr("width", width)
            .style('fill', "transparent")

//axis
var displayAxis = svg.select(".background_items")
                        .append('g')
                            .attr('class', 'axis')
                            .attr('transform', function(){
                                return 'translate('+0+','+midScreen+')'
                            })
                            .style('font-size', 16)
                            .call(axis)
    
displayAxis
        .selectAll('path')
            .attr("stroke-width", radius)
            .attr("stroke", "lightgrey")

displayAxis
        .selectAll('line')
            .attr('y1', function(){
                return -d3.select(this).attr('y2')
            })
            .attr('stroke-width', '2px')

//year display
svg.select(".background_items")
        .append("g")
            .attr("class", "Year")
            .attr('transform', 'translate('+ width/2 +',' + 75 +')')
        .append('rect')
            .attr("width", 150)
            .attr("height", 75)
            .attr("x", -75)
            .attr("y", -55)
            .attr("stroke", "darkgrey")
            .style("fill", "darkgrey");

var yearTag = svg.select(".background_items").select(".Year")
                .append("text")
                    .attr("font-size", 50)
                    .style('fill', 'white')
                    .style('text-anchor', 'middle')
                    .text(function(){
                        return d3.timeFormat('%Y')(time.invert(width/2));
                    });

//instantiate movable objects
svg.append('g')
    .attr("class", "timeline")
    .attr("transform", 'translate(' +xPadding+ ','+midScreen+')')

//left side padding
var leftSideBar = svg.append('g')
                        .attr("class", "leftSideBar")
                        .attr('transform', 'translate(' 
                            + xPadding + ',' + midScreen + ')')

leftSideBar.append("rect")
            .attr('width', xPadding)
            .attr('height', height)
            .attr('x', -xPadding)
            .attr('y', -midScreen)

leftSideBar.append('line')
            .attr("stroke", "black")
            .attr("stroke-width", 3)
            .attr("x1", -3)
            .attr("x2", -3)
            .attr("y1", -60)
            .attr("y2", 60);

//right side padding
var rightSideBar = svg.append('g')
                            .attr("class", "rightSideBar")
                            .attr('transform', 'translate(' 
                                    + (xPadding + width) + ',' 
                                    + midScreen + ')')


rightSideBar.append("rect")
            .attr('width', xPadding)
            .attr('height', height)
            .attr("y", -midScreen)

rightSideBar.append('line')
            .attr("stroke", "black")
            .attr("stroke-width", 3)
            .attr("y1", -40)
            .attr("y2", +40);

var firstMonth = leftSideBar.append("text")
                    .attr('transform', 'translate(' + (-12) + ','  + 0 + '), rotate(270)')
                    .style('text-anchor', 'middle')
                    .attr("font-size", 24)
                    .text(function(){
                        return d3.timeFormat('%B')(time.invert(-1));
                    })

//today
d3.select('.timeline')
    .append('g')
        .attr('class', 'g-today')
        .append('text')
            .attr('class', 'today')
            .attr('font-family', 'Material Icons')
            .attr('font-size', '20px')
            .text('account_circle')
            .attr('y', 10)
