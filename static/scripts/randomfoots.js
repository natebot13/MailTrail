var foots = ['static/images/footsteps1.png', 'static/images/footsteps2.png', 'static/images/footsteps3.png', 'static/images/snailsmall.png']

randInt = function(x) {
  return Math.floor(Math.random() * x);
};

function putfoots() {
  var i;
  for (i in foots) {
    me = $(document.createElement('img'));
    me.addClass('foot');
    this.me.css({left: randInt(100)-50 + '%', top: randInt(100)-50 + '%',});
    me.attr('src', foots[i]);
    transform = {webkitTransform: 'rotate(' + randInt(360) + 'deg)',
                 msTransform: 'rotate(' + randInt(360) + 'deg)',
                 mozTransform: 'rotate(' + randInt(360) + 'deg)',
                 transform: 'rotate(' + randInt(360) + 'deg)'};
    me.css(transform);
    $('body').prepend(me);
  }
}

putfoots();
