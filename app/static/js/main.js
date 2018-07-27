$(function () {
    // 设置登录界面全屏背景布
    $('.bg_login').css('height', $("body").height());

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
});