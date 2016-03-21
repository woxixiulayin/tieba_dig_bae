var jPostAnimation = {
    before: {
        left: "800px",
        opacity: "0"
    },
    after: {
        left: "0",
        opacity: "1"
    },
    delay: 1200
}

function postIn(post, animation){
    post.css(animation.before)
    .animate(animation.after, animation.delay);
}

var main = function(){
    postIn($(".post"), jPostAnimation);
};

$(document).ready(main);