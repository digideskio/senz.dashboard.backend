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
        var chkObjs = document.getElementsByName('test');
        var select_app = document.getElementById('select_app').value;
        var select_tracker = document.getElementById('select_tracker').value;

        for(var i=0; i<chkObjs.length; ++i){
            if(chkObjs[i].checked){
                var event = chkObjs[i].parentNode.parentNode.getAttribute("id");
                var val = chkObjs[i].value;
                break;
            }
        }
        $.post("/panel",
        {
            tracker: select_tracker,
            app_id: select_app,
            event: event,
            val: val
        });
    });
});
