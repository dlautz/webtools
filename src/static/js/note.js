$(document).ready(function() {

    $("#getTagForm").click(function(event){
        $("#noteForm").hide();
        $("#tagForm").fadeIn();
    });



    $("#tagAdd").click(function(event) {

        var noteID = $("#noteID").text();
        console.log(noteID)

        var addTagUrl = "/notes/add_tag/" + noteID

        var newTag = {"name": $("#tagName").val()}

        $.ajax({
            type: 'POST',
            dataType: 'json',
            headers: {"Content-Type": "application/json"},
            url: addTagUrl,
            data: JSON.stringify(newTag)

        })
//        .done(function(){
//            $("#tagName").val("");
//            $("#tagForm").hide();
//            $("#noteForm").fadeIn();
//            });
    });
});
