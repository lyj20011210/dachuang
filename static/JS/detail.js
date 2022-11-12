$(function () {
    //评分
    var starRating = 0;
    var isCollect = 0;
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
        isCollect = 0;
        $('.photo span').find('.high').css('z-index', 0);
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
                data: {'name':starRating},
                success: function (result) {
                    console.log(result)
                    alert("helo")
                }
            })
            // alert('评分：' + (sdata['score'] + '分'))
            alert('评分：' + (starRating.toFixed(1) + '分'))
        }
    })
    //取消收藏
    $('.unGetSc').on('click', function () {
        alert("取消收藏")
        isCollect = 0;
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:5000/collects",
            dataType: "json",
            data: {'name':isCollect},
            success: function (result) {
                console.log(result)
                alert("helo")
            }
        })
    });
    // 收藏
    $('.getSc').on('click', function () {
        alert("收藏成功")
        isCollect = 1;
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:5000/collects",
            dataType: "json",
            data: {'name':isCollect},
            success: function (result) {
                console.log(result)
                alert("helo")
            }
        })
    });
})
