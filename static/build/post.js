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

var jPostExample =  {
        "title":"HTML教程",
        "author":"yuanmin",
        "rep_num":200,
        "url_link": "www.baidu.com",
        "last_time":"17:34",
        "body":"this is a short corse for teaching"
    }

var jSerachExample = {
            'tieba_name': "游戏",
            'deepth': 1,
            'rep_num': 100,
        }

function postIn(post, animation){
    appendPost(post);
    post.css(animation.before)
    .animate(animation.after, animation.delay);
}

function createPost(jpost) {
    var psot = "";
    post = '<div class=\"post\"><a class=\"post-title\">'+jpost.title+'</a><p class=\"post-body\">' + jpost.body +'</p><div class=\"post-label\"><span class=\"post-rep-num\">'+jpost.rep_num+'</span><span class=\"post-author\">'+jpost.author+'</span><span class=\"post-last-time\">'+jpost.last_time+'</span></div></div></div>'
    return $(post);
}

function appendPost(post) {
    post.appendTo('.posts')
}

function getData() {
    console.log(1);
    $.post('/search', jSerachExample, function(data, status){
        for(var i in data) {
            postIn(createPost(data[i]), jPostAnimation);
        }
    })
}

var main = function(){
    //postIn(createPost(jPostExample), jPostAnimation);
    getData();
};

$(document).ready(main);