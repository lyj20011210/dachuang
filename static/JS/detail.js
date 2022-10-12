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
})
