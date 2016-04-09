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

// var jPostExample =  {
//         "title":"HTML教程",
//         "author":"yuanmin",
//         "rep_num":200,
//         "url_link": "www.baidu.com",
//         "last_time":"17:34",
//         "body":"this is a short corse for teaching"
//     }

var jSerachExample = {
            'tieba_name': "游戏",
            'deepth': 1,
            'rep_num': 100,
        }

var hint = $(".hint");
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

function getSearchInfo(){
    var serchInfo = {};
    serchInfo["tieba_name"] = $("input[name='tieba_name']").val();
    serchInfo["deepth"] = $("input[name='deepth']").val();
    serchInfo["rep_num"] = $("input[name='rep_num']").val();
    serchInfo["author"] = $("input[name='author']").val();
    console.log(serchInfo);
    return serchInfo;
}

function getData() {
    console.log("getData");
    hint.text("正在搜索...");
    $.post('/search', getSearchInfo(),
        function(data, status){
        hint.hide();
        for(var i in data) {
            postIn(createPost(data[i]), jPostAnimation);
        }
    }
    ) 
}

function initPost() {
  $(".btn-go").click(getData);
}


var main = function(){
    //postIn(createPost(jPostExample), jPostAnimation);
    // getData();
    initPost();
};

main();
