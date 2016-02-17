$(function(){
    var path = location.pathname;
    $navItem = $("#sidebar").find(".sub-nav li");

    if(path.indexOf("profile") > 0) {
        $navItem.eq(0).addClass("active");
        // $("#userGroupNav").css("color","rgba(51, 204, 204, 1)");
        $("#userGroupSubNav").css("display","block");
    } else if (path.indexOf("interest") > 0) {
        $navItem.eq(1).addClass("active"); 
        $("#userGroupSubNav").css("display","block");
    } else if (path.indexOf("marriage") > 0) {
        $navItem.eq(2).addClass("active");
        $("#userGroupSubNav").css("display","block");
    } else if (path.indexOf("consumption") > 0) {
        $navItem.eq(3).addClass("active");
        $("#userGroupSubNav").css("display","block");
    } else if (path.indexOf("location") > 0) {
        $navItem.eq(4).addClass("active");
        $("#userGroupSubNav").css("display","block");
    } else if (path.indexOf("motion") > 0) {
        $(".motion").addClass("active");
    } else if (path.indexOf("context") > 0) {
        $(".context").addClass("active");
    } else if (path.indexOf("single") > 0) {
        $(".single").addClass("active");
    } else if (path.indexOf("group") > 0) {
        $(".group").addClass("active");
    } else if (path.indexOf("push") > 0) {
        $(".push").addClass("active");
    } else if (path.indexOf("history") > 0) {
        $(".history").addClass("active");
    } else {
        $(".index").addClass("active");
    }

    if (path.indexOf("dashboard") > 0) {
        $(".nav-dashboard").addClass("active");
    } else if (path.indexOf("integration") > 0) {
        $(".nav-integration").addClass("active");
    } else if (path.indexOf("create") > 0) {
        $(".nav-settings").addClass("active");
    } else if (path.indexOf("manage") > 0) {
        $(".nav-settings").addClass("active");
    } else if (path.indexOf("panel") > 0) {
        $(".nav-panel").addClass("active"); 
    }

    $(".j-auto-jump").on("click", "li a", function(e){
        e.preventDefault();
        var $this = $(this);
        $("html,body").animate({scrollTop:$($this.attr("href")).offset().top - 50 },1000);
    })

});
