//var location2;
//$(function(){
//    $("select").click(function(){
//        $(this).find("option:selected").parent().prev().attr("checked", true);
//        location2 = $(this).find("option:selected").text();
//    });
//    $("select").change(function(){
//        location2 = $(this).find("option:selected").text();
//    });
//});
//
//$(function(){
//    $("#location_type_one input").click(function(){
//        location2 = $(this).next().find("option:selected").text();
//    });
//});

$(document).ready(function(){
    $('#btn').click(function(e){
        //var _xsrf = $("[name='_xsrf']").attr('value');
        //var app_id = $(".switch-app .dropdown button").attr("app_id");
        var chkObjs = document.getElementsByName('test');
        //var type, val;
        var select_app = document.getElementById('select_app').value;

        for(var i=0; i<chkObjs.length; ++i){
            if(chkObjs[i].checked){
                var type = chkObjs[i].parentNode.parentNode.getAttribute("id");
                var val = chkObjs[i].value;
                break;
            }
        }
        $.post("/panel",
        {
            //_xsrf: _xsrf,
            app_id: select_app,
            type: type,
            val: val
        });
    });
});
