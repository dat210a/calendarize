
var totalWidth = 800;
var totalHeight = 600;
var xPadding = 75;

var width = totalWidth - 2*xPadding,
    height = totalHeight;

var midScreen = height / 2;

var radius = 8;

var tresholdNumPoints = 8;
var k = 1;

var time = d3.scaleTime()
                .domain([new Date('1/1/1999'), d3.timeMillisecond.offset(new Date('1/1/2000'), 20930400)])
                .range([0, width]);

var axis = d3.axisBottom(time)
                .tickFormat(d3.timeFormat('%b'))
                .tickArguments([d3.timeMonth.every(1)])
                .tickPadding(15)
                .tickSize(25)

//create canvas and all basic timeline objects
var svg = d3.select('svg')
                    .attr('width', totalWidth)
                    .attr('height', height)
                    .attr("transform", "translate(" + 0 + "," + 0 + ")")

svg.append('path')
        .attr('d', 'M515,-14L597,-395L617,-395')

//year display
svg.append('g')
        .attr("class", "background_items")
        .attr("transform", "translate(" + xPadding + ", 0)")
        .append("g")
            .attr("class", "Year")
            .attr('transform', 'translate('+ width/2 +',' + 75 +')')
        .append('rect')
            .attr('class', "yearBox shadow")
            .attr("width", 150)
            .attr("height", 75)
            .attr("x", -75)
            .attr("y", -55)
            .attr("rx", 2)
            .attr("ry", 2)

var yearTag = svg.select(".background_items").select(".Year")
                .append("text")
                    .attr('class', 'yearText')
                    .attr("font-size", 50)
                    .style('fill', '#F1F0F0')
                    .style('text-anchor', 'middle')
                    .text(function(){
                        return d3.timeFormat('%Y')(time.invert(width/2));
                    });

//instantiate movable objects
svg.append('g')
    .attr("class", "timeline")
    .attr("transform", 'translate(' +xPadding+ ','+midScreen+')')

//axis
var displayAxis = d3.select(".timeline")
                    .append('g')
                        .attr('class', 'axis')
                        .style('font-size', 16)
                        .call(axis)

displayAxis.selectAll('path')
                .style("stroke-width", radius)
                .style("stroke", "#97989C")

displayAxis
    .selectAll('line')
        .attr('stroke', '#3D4148')
        .attr('y1', function(){
            return -d3.select(this).attr('y2')
        })
        .attr('stroke-width', '2px')

//today
d3.select('.timeline')
    .append('g')
    .attr('class', 'g-today')
    .append('text')
        .attr('class', 'todayMark')
        .style('font-family', 'Material Icons')
        .attr('font-size', '20px')
        .text('account_circle')
        .attr('y', 10)

// svg.append('g')
//         .attr("class", "foreground_items")
//         .attr("transform", "translate(" + xPadding + ", 0)")
//         .append('rect')
//             .attr('class', 'scrollArea')
//             .attr("height", height)
//             .attr("width", width)
//             .style('fill', "transparent")
//             .on('click', function(){
//                 d3.select(this).attr('display', 'none');
//                 var element = document.elementFromPoint(event.clientX,event.clientY)
//                 d3.select($(element).parent()[0]).dispatch('click')
//                 d3.select(this).attr('display', 'inline');
//             })



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
            .style("stroke", "#3D4148")
            .style("stroke-width", (3/4*radius))
            .attr("x1", 1)
            .attr("x2", 1)
            .attr("y1", -50)
            .attr("y2", 50);

var firstMonth = leftSideBar.append("text")
                    .attr('transform', 'translate(' + (-12) + ','  + 0 + '), rotate(270)')
                    .style('text-anchor', 'middle')
                    .attr("font-size", 24)
                    .text(function(){
                        return d3.timeFormat('%B')(time.invert(0));
                    })

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
            .style("stroke", "#3D4148")
            .attr("stroke-width", (3/4*radius))
            .attr("y1", -50)
            .attr("y2", +50);


            