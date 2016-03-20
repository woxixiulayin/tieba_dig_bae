var main = function(){
    $(".post").css({"left":"800px","opacity":"0"})
    .animate({left: "0", opacity: "1"}, 1200);

};

$(document).ready(main);