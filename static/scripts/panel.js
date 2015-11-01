$(document).ready(function(){
    $('#btn').click(function(e){
        var motionObjs = document.getElementsByName('motion');
        var contextObjs = document.getElementsByName('context');
        var select_app = document.getElementById('select_app').value;
        var select_tracker = document.getElementById('select_tracker').value;

        for(var i=0; i<motionObjs.length; ++i){
            if(motionObjs[i].checked){
                var motionType = motionObjs[i].parentNode.parentNode.getAttribute("id");
                var motionVal = motionObjs[i].value;
                break;
            }
        }
        for(i=0; i<contextObjs.length; ++i){
            if(motionObjs[i].checked){
                var contextType = contextObjs[i].parentNode.parentNode.getAttribute("id");
                var contextVal = contextObjs[i].value;
                break;
            }
        }
        $.post("/panel/debug",
        {
            tracker: select_tracker,
            app_id: select_app,
            motionType: motionType,
            contextType: contextType,
            motionVal: motionVal,
            contextVal: contextVal
        });
    });
});
