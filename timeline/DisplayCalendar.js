//TODO change width/height dynamically
var width = 1600,
    height = 900;

var radius = 8;

var xPadding = 50;
var bottomOffset = 200;

var currentYear = 2017;

var midScreen = height / 2;

var k = 1;

//TODO maybe add more ticks when zoomed in
var weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

var xScale = d3.scaleLinear().domain([0, 365]).range([0, width]);

var zoom = d3.zoom()
                .scaleExtent([1, 12])
                .on("zoom", zoomInOut);

//create canvas and all basic timeline objects
var svg = d3.select('body')
                .append("svg")
                .attr("height", height)
                .attr("width", width + xPadding*2)
                .attr("transform", "translate(0, 0)");

svg.append('g')
        .attr("class", "background_items")
        .attr("transform", "translate(" + xPadding + ", 0)")
        .append('rect')
            .attr('class', 'scrollArea')
            .attr("height", height - bottomOffset)
            .attr("width", width)
            .style('fill', "transparent")
            .call(zoom);

//middle line
svg.select(".background_items")
        .append("line")
            .attr("stroke", "#ddd")
            .attr("stroke-width", radius)
            .attr("x1", 0)
            .attr("x2", width)
            .attr("y1", midScreen)
            .attr("y2", midScreen);

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

var yearTag = svg.select(".background_items").select("g")
                .append("text")
                    .attr("font-size", 50)
                    .style('fill', 'white')
                    .text(currentYear);

//instantiate movable objects
svg.append('g')
    .attr("class", "timeLine")
    .attr("transform", 'translate(' +xPadding+ ','+midScreen+')')
        .append('g')
            .attr("class", "months")

//left side padding
var leftSideBar = svg.append('g').attr("class", "leftSideBar")

leftSideBar.append("rect")
            .attr('width', xPadding)
            .attr('height', height)

leftSideBar.append('line')
            .attr("stroke", "black")
            .attr("stroke-width", 3)
            .attr("x1", xPadding-3)
            .attr("x2", xPadding-3)
            .attr("y1", midScreen-60)
            .attr("y2", midScreen+60);

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

//load month specs
d3.json("months.json", function(error, data){
    if (error) throw error;
    
    var monthsContainer = d3.selectAll(".months").selectAll('g')
                                .data(data)
                                .enter()
                                    .append("g")
                                    .attr("class", function(d){return d.Name;})
                                    .attr('transform', function(d, i){
                                       return 'translate('+xScale(d.TotalDays)+','+0+')'
                                    })

    var monthText = monthsContainer
                    .append("text")
                        .attr("y", 35)
                        .text(function (d) {return d.Abbrev;});

    var monthTics = monthsContainer
                    .append("line")
                        .attr("stroke", "black")
                        .attr("stroke-width", 2)
                        .attr("y1", -15)
                        .attr("y2", 15);

    var firstMonth = leftSideBar.append("text")
                        .attr('transform', 'translate(' + (xPadding-12) + ','  + midScreen + '), rotate(270)')
                        .attr("font-size", 24)
                        .text(data[0].Name);
})

//zoom and scroll update function
function zoomInOut() {
    var transform = d3.event.transform;
    var xNewScale = transform.rescaleX(xScale);

    //show/hide bottom bar when zooming in/out
    if (!d3.selectAll('.bottomMenu').empty())
    {
        if (k > 3.3 && transform.k < 3.3){
            if (d3.select('.bottomMenu').attr('up') === 'false') ToggleAgendaMenu();
        }
        else if (k < 3.3 && transform.k > 3.3){
            if (d3.select('.bottomMenu').attr('up') === 'true') ToggleAgendaMenu();
        }
    }
    k = d3.event.transform.k;
    var adjustedYearLength = Math.round(width*k);
    
    //update year display
    yearTag
        .text(function(){
            return currentYear - Math.floor((d3.event.transform.x - width/2)/adjustedYearLength) - 1;
        });
        
    //reposition month tags
    var highestX = 0;
    d3.selectAll('.months').selectAll('g')
                .attr('transform', function(d, i){
                    var x = xNewScale(d.TotalDays) % adjustedYearLength;
                    if (x<0) x += adjustedYearLength;
                    if (highestX < x) {
                        highestX = x;
                        d3.select('.leftSideBar').select('text')
                            .text(d.Name)
                    }
                    return 'translate('+x+','+0+')';
                });
    
    //Update data events position if there are any
    if (!d3.selectAll('.data').empty()){   
        if (k < 3.3){
            d3.selectAll('.data').selectAll('.detail').style('display', 'none');
        }
        else{
            d3.selectAll('.data').selectAll('.detail').style('display', 'inline');
        }
        d3.selectAll(".data").selectAll('line')
            .attr("x1", function(d, i){
                d.x = xNewScale(d.date);
                if (d.recurring == 1){
                    d.x = d.x % adjustedYearLength;
                    return d.x + d.duration*k >= 0 ? d.x : d.x = d.x + width*k;
                }
            })
            .attr("x2", function(d){
                return d.x + d.duration*k;
            });
        d3.selectAll('.data').selectAll('g').sort(function(x, y){
            return d3.descending(+x.x, +y.x)
        })
        simUpdate();
    }
}