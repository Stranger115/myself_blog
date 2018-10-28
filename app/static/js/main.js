$(function () {
    // 设置登录界面全屏背景布
    $('.bg_login').css('height', $("body").height());
    var height = $('.register_page').height();
    $('.register_page').css('height', height + 50);


    $(".nav li").click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    });

    // 显示登录模块
    $(".show_login").click(function () {
        $(".login_content").fadeIn(10);
        $('.bg_login').fadeIn(10);
    });
    // 隐藏登录模块
    $('.login_content .close_login').click(function () {
        $('.login_content ').fadeOut(10);
        $('.bg_login').fadeOut(10)
    });

    // 回复评论
    $(".comment-date .reply_func").click(function () {
        $('.comments').find('.reply').eq($(this).attr('value')).fadeIn(10);
    });

    // 隐藏评论显示
    $(".reply button").click(function () {
        $(this).parent().parent().fadeOut(10)
    })
});