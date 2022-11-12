$(function () {

    // nav部分
    $(".main_left div").mouseover(function () {
        $(this).addClass("current").siblings().removeClass("current");
        var index = $(this).index(); //得到当前li的索引号
        $(".main_right .content").eq(index).stop().slideDown(1200).siblings().stop().slideUp(1200);
    });

    // sec2 点击部分
    $(".sec2_main_head ul li").click(function () {
        $(this).addClass("current1").siblings().removeClass("current1");
        var index = $(this).index(); //得到当前li的索引号
        $(".sec2_main_body>.sec2_main_body_content")
            .eq(index)
            .stop()
            .fadeIn(1200)
            .siblings()
            .stop()
            .fadeOut(1200);
    });
});

function isHidden(oDiv){
    for(let i = 1; i<=6; i++){
        let vDiv = document.getElementById('div' + i);
        vDiv.style.display = 'none';
    }
    let cDiv = document.getElementById(oDiv);
    cDiv.style.display = 'block';

}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
