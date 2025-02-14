$(function() {
    $("#draggable").draggable({
        revert: "invalid" 
    });

    $("#droppable").droppable({
        accept: "#draggable", 
        over: function(event, ui) { 
            $(this).addClass("ui-state-highlight"); 
        },
        out: function(event, ui) { 
            $(this).removeClass("ui-state-highlight"); 
        },
        drop: function(event, ui) {
            $(this).addClass("ui-state-highlight")
                   .find("p")
                   .html("Dropped!");
        }
    });
});
