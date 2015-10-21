var location2;
$(function(){
    $("select").click(function(){
        $(this).find("option:selected").parent().prev().attr("checked", true);
        location2 = $(this).find("option:selected").text();
    });
    $("select").change(function(){
        location2 = $(this).find("option:selected").text();
    });
});

$(function(){
    $("#location_type_one input").click(function(){
        location2 = $(this).next().find("option:selected").text();
    });
});

$(document).ready(function(){
    $('#btn').click(function(e){
        var _xsrf = $("[name='_xsrf']").attr('value');
        var app_id = $(".switch-app .dropdown button").attr("app_id");
        var chkObjs = document.getElementsByName('test');
        var type, val;

        for(var i=0; i<chkObjs.length; ++i){
            if(chkObjs[i].checked){
                type = chkObjs[i].parentNode.parentNode.getAttribute("id");
                val = chkObjs[i].value;
                break;
            }
        }

        $.post("/panel",
        {
            _xsrf: _xsrf,
            app_id: app_id,
            type: type,
            val: val
        });

        if(type === "location_type_one"){
            $.post("/panel",
            {
                _xsrf: _xsrf,
                app_id: app_id,
                type: "location_type_two",
                val: location2
            });
        }
    });
});
