
$(".resetToToday" ).click(function() {
    resetView();
});

var slider = document.getElementById("zoomSlider");

slider.onchange = function (){
    d3.select('.scrollArea').call(zoom.scaleTo, this.value);
}