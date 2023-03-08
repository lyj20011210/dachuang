$(function () {
    //评分
    var starRating = 0;
    //鼠标移入
    $('.photo span').on('mouseenter', function () {
        var index = $(this).index() + 1;
        $(this).prevAll().find('.high').css('z-index', 1);
        $(this).find('.high').css('z-index', 1);
        $(this).nextAll().find('.high').css('z-index', 0);
        $('.starNum').html((index * 2).toFixed(1) + '分');
    });
    //鼠标离开
    $('.photo').on('mouseleave', function () {
        $(this).find('.high').css('z-index', 0);
        var count = starRating / 2;
        console.log(count);
        if (count == 5) {
            $('.photo span').find('.high').css('z-index', 1);
        } else {
            $('.photo span').eq(count).prevAll().find('.high').css('z-index', 1);
        }
        $('.starNum').html(starRating.toFixed(1) + '分')
    }),
        //点击
        $('.photo span').on('click', function () {
            var index = $(this).index() + 1;
            $(this).prevAll().find('.high').css('z-index', 1)
            $(this).find('.high').css('z-index', 1);
            starRating = index * 2;
            $('.starNum').html(starRating.toFixed(1) + '分');
            //alert('评分：' + (starRating.toFixed(1) + '分'))
        });
    //取消评分
    $('.cancleStar').on('click', function () {
        starRating = 0;
        $('.photo span').find('.high').css('z-index', 0);
        $('.starNum').html(starRating.toFixed(1) + '分');
    });
    //确定评分

    $('.sureStar').on('click', function () {
        if (starRating === 0) {
            alert('最低一颗星！');
        } else {
            $.ajax({
                type: "GET",
                url: "http://127.0.0.1:5000/score",
                dataType: "json",
                data: {'name': starRating},
                success: function (result) {
                    console.log(result)
                    alert("helo")
                }
            })
            // alert('评分：' + (sdata['score'] + '分'))
            alert('评分：' + (starRating.toFixed(1) + '分'))
        }
    })

    // 评论提交
    $(".comment_input").submit(function (e) {
        e.preventDefault();
        var content = $("#comment_input").val();
        var params = {
            "content": content
        };
        $.ajax({
            url: "/news_comment",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(params),
            success: function (resp) {
                if (resp.errno == 1) {
                    alert(resp.errmsg);
                } else if (resp.errno == 2) {
                    alert(resp.errmsg);
                } else {
                    alert("评论成功！");
                    location.reload();
                }
            }

        })

    })

    // 评论回复
    $('.comment-content').delegate('a,input', 'click', function (e) {
        //获取到点击标签的class属性, reply_sub
        var sHandler = $(this).prop('class');

        if (sHandler.indexOf('reply') >= 0) {
            $(this).next().next().toggle();
        }

        if (sHandler.indexOf('reply_cancel') >= 0) {
            $(this).parent().parent().parent().toggle();
            return false
        }
        if (sHandler.indexOf('reply_sub') >= 0) {
            var $this = $(this)
            var parent_id = $this.parent().attr('data-comment_id')
            var content_child = $this.prev().val()
            var params_child = {
                "parent_id": parent_id,
                "content_child": content_child
            }
            $.ajax({
                url: "/news_comment",
                type: "post",
                contentType: "application/json",
                data: JSON.stringify(params_child),
                success: function (resp) {
                    if (resp.errno === 2) {
                        alert(resp.errmsg);
                    } else if (resp.errno === 3) {
                        alert(resp.errmsg);
                    } else {
                        alert("回复成功！");
                        location.reload();
                    }
                }
            })
            return false
        }
    })
    //收藏
    $("#btn_collect").click(function () {
        var classname = $("#btn_collect_icon").attr("class");

        if (classname == "glyphicon glyphicon-star-empty") {
            var isCollected = 1;
            $.ajax({
                type: "GET",
                url: "http://127.0.0.1:5000/collects",
                dataType: "json",
                data: {'flag_c': isCollected},
                success: function (resp) {
                    if (resp.errno === 1) {
                        alert(resp.errmsg);
                    } else if (resp.errno === 2) {
                        alert(resp.errmsg);
                        $("#btn_collect_icon").removeClass("glyphicon-star-empty glyphicon-star");
                        $("#btn_collect_icon").addClass("glyphicon glyphicon-star");
                    } else {
                        $("#btn_collect_icon").removeClass("glyphicon-star-empty glyphicon-star");
                        $("#btn_collect_icon").addClass("glyphicon glyphicon-star");
                        // console.log(reps)
                        alert("收藏成功");
                    }
                }
            })
        } else {
            var isCollected = 0;
            $.ajax({
                type: "GET",
                url: "http://127.0.0.1:5000/collects",
                dataType: "json",
                data: {'flag_c': isCollected},
                success: function (resp) {
                    if (resp.errno === 1) {
                        alert(resp.errmsg);
                    } else {
                        $("#btn_collect_icon").removeClass("glyphicon-star-empty glyphicon-star");
                        $("#btn_collect_icon").addClass("glyphicon glyphicon-star-empty");
                        // console.log(resp)
                        alert("取消收藏");
                    }
                }
            })
        }
    });
})
