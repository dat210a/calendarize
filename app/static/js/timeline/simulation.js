
//instantiate simulation
var simulation = d3.forceSimulation()
                        .force('gravity', gravity)
                        .force('pointsCollider', pointCollider)
                        .force('detailsBoxCollider', detailBoxCollider);

//update simulation based on user changes
function simUpdate(){
    timer = 0;
    simulation
        .alpha(0.2)
        .restart();
};

function pushDown(container){
    d3.selectAll('.data').selectAll('.e' + container.event_id)
        .selectAll('.detailContainer')
            .each(function(d){ if (d.y <= 0) d.y = 100;})
}

function pullUp(container){
    d3.selectAll('.data').selectAll('.e' + container.event_id)
        .selectAll('.detailContainer')
            .each(function(d){ if (d.y > 0) d.y = -140;})
}

//pull towards the mid line 
function gravity(alpha){
    var selection = d3.selectAll('.data')
                        .selectAll('g')
                            .filter(function(d){
                                return d3.select(this).style('display') == 'inline';
                            })
    selection.selectAll('.points')
                .each(function(d){
                    d.vy += (0 - d.y)*0.4*alpha
                })
    selection.selectAll('.detailContainer')
                .each(function(d){
                    var pullTo =  d.y > 10 ? 100 : -140
                    d.vy += (pullTo - d.y)*0.1*alpha
                    // if (this.parentNode.__data__.event_id == 39) console.log(d.y, d.vy)
                })        
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
        var numOverlap = 0;
        for (j = i + 1; j < n; j++){
            point = nodes[j];
            var dist = capsuleCollider(capsule, point, capsule.length);
            if (dist < radius*2+2) {
                numOverlap++;
                if (capsule.length < point.length*0.9
                    || (point.length > 0.9*capsule.length && point.y + point.vy > capsule.y + capsule.vy + radius/2))
                    {
                        capsule.vy -= (radius*2+2 - dist);
                    }
                else point.vy -= (radius*2+2 - dist);
                if (timer == 0 && point.y + point.vy == 0)
                    pushDown(point)
            }
        }
        if (timer == 0 && numOverlap > 0 && capsule.y + capsule.vy == 0){
            pushDown(capsule)
            // else 
            //     d3.selectAll('.data').selectAll('.e' + capsule.event_id)
            //         .selectAll('.detailContainer')
            //             .each(function(d){ if (d.y > 0) d.y = -140;})
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
            var pointRootX = pParent.x + pParent.length/2;
            d3.selectAll('.data').selectAll('.detailContainer')
                .filter(function(){
                    return d3.select(this.parentNode).style('display') == 'inline';
                })
                .filter((d, j) => j > i)
                .each(function(capsule){
                    var cParent = this.parentNode.__data__;
                    var capsuleRootX = cParent.x + cParent.length/2
                    if (capsuleRootX < pointRootX) {
                        var dist = detailsCollider(capsule, point, detailWidth, capsuleRootX, pointRootX);
                        if (dist < detailHeight+5) {
                            if (capsule.y > 0) capsule.vy += (detailHeight+5 - dist);
                            else capsule.vy -= (detailHeight+5 - dist);
                        }
                    }
                    else{
                        var dist = detailsCollider(point, capsule, detailWidth, pointRootX, capsuleRootX);
                        if (dist < detailHeight+5) {
                            if (point.y > 0) point.vy += (detailHeight+5 - dist);
                            else point.vy -= (detailHeight+5 - dist);
                        }
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

function detailsCollider(capsule, point, length, capsuleRootX, pointRootX){
    cx = capsuleRootX + xOffset(Math.abs(capsule.y + capsule.vy));
    px = pointRootX + xOffset(Math.abs(point.y + point.vy));
    if (px > cx + detailWidth + 25) return width;
    return distToCapsule(cx, capsule.y + capsule.vy, px, point.y + point.vy, length);
};

// Capsule Collider helper functions
function sqr(x){
    return x*x;
};

function dist2(x1, y1, x2, y2){
    return sqr(x1 - x2) + sqr(y1 - y2);
};

function distToCapsule(cx, cy, px, py, length) {
    if (length == 0) return Math.sqrt(dist2(px, py, cx, cy));
    var t = (px - cx) / length;
    t = Math.max(0, Math.min(1, t));
    return Math.sqrt(dist2(px, py, cx + t * length, cy));
};