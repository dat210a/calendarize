

//force pull towards the middle line
var dataGravity = d3.forceY(0).strength(0.1);
var detailsGravity = d3.forceY(function(d){
                                return d.y > 10 ? 100 : -140
                            }).strength(0.5);

//instantiate simulation
var simulation = d3.forceSimulation()
                        .force('gravity', dataGravity)
                        .force('detailsGravity', detailsGravity)
                        .force('pointsCollider', pointCollider)
                        .force('detailsBoxCollider', detailBoxCollider);

//update simulation based on user changes
function simUpdate(){
    timer = 0;
    simulation
        .alpha(1)
        .restart();
};

//collision force for points on the line
function pointCollider(alpha){
    var nodes = d3.selectAll('.data')
                    .selectAll('g')
                        .filter(function(d){
                            return d3.select(this).style('display') == 'inline';
                        })
                        .selectAll('.points')
                            .data().reverse();
    for (i = 0, n = nodes.length; i < n; i++){
        capsule = nodes[i];
        for (j = i + 1; j < n; ++j){
            point = nodes[j];
            var dist = capsuleCollider(capsule, point, capsule.length*k);
            if (dist < radius*2+2) {
                if (point.length*0.9 <= capsule.length) point.vy -= (radius*2+1 - dist);
                else capsule.vy -= (radius*2+1 - dist);
            }
        }
    }
}

//collision force for detail boxes
function detailBoxCollider(alpha){
    d3.selectAll('.data').selectAll('.detailContainer')
        .filter(function(){
            return d3.select(this.parentNode).style('display') == 'inline';
        })
        .each(function(point, i){
            var pParent = this.parentNode.__data__;
            d3.selectAll('.data').selectAll('.detailContainer')
                .filter(function(){
                    return d3.select(this.parentNode).style('display') == 'inline';
                })
                .filter(function(d, j){return j > i;})
                .each(function(capsule, j){
                    var cParent = this.parentNode.__data__;
                    var dist = detailsCollider(capsule, point, detailWidth, cParent, pParent);
                    if (dist < detailHeight+5) {
                        if (capsule.y > 0) capsule.vy += (detailHeight+5 - dist);
                        else capsule.vy -= (detailHeight+5 - dist);
                    }
                })
        })
}

// CAPSULE COLLIDER
// capsule colliders distance functions
function capsuleCollider(capsule, point, duration){
    return distToCapsule(capsule.x + capsule.vx, 
                         capsule.y + capsule.vy, 
                         point.x + point.vx, 
                         point.y + point.vy, 
                         duration);
};

function detailsCollider(capsule, point, duration, cParent, pParent){
    cx = cParent.x + cParent.length*k/2 + xOffset(Math.abs(capsule.y + capsule.vy));
    px = pParent.x + pParent.length*k/2 + xOffset(Math.abs(point.y + point.vy));
    if (px > cx + detailWidth + 25) return width;
    return distToCapsule(cx, capsule.y + capsule.vy, px, point.y + point.vy, duration);
};

// Capsule Collider helper functions
function sqr(x){
    return x*x;
};

function dist2(x1, y1, x2, y2){
    return sqr(x1 - x2) + sqr(y1 - y2);
};

function distToCapsule(cx, cy, px, py, duration) {
    if (duration == 0) return Math.sqrt(dist2(px, py, cx, cy));
    var t = (px - cx) / duration;
    t = Math.max(0, Math.min(1, t));
    return Math.sqrt(dist2(px, py, cx + t * duration, cy));
};