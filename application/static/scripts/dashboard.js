$(function(){
    var path = location.pathname;
    $navItem = $("#sidebar").find(".sub-nav li");

    if(path.indexOf("profile") > 0) {
        $navItem.eq(0).addClass("active");  
    } else if (path.indexOf("interest") > 0) {
        $navItem.eq(1).addClass("active"); 
    } else if (path.indexOf("marriage") > 0) {
        $navItem.eq(2).addClass("active");
    } else if (path.indexOf("consumption") > 0) {
        $navItem.eq(3).addClass("active");
    } else if (path.indexOf("location") > 0) {
        $navItem.eq(4).addClass("active");
    } else if (path.indexOf("motion") > 0) {
        $(".motion").addClass("active");
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