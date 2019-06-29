$(document).ready(function(){
    refreshTable();
    $("#youtube_container").hide();
});

function refreshTable(){
    $('#tableHolder').load('existing_jobs.php', function(){
        setTimeout(refreshTable, 2000);
    });
}

$(function() {

    $("#add_url").change(function(){
        var url = this.value;

        var domain = url.replace('http://','').replace('https://','').split(/[/?#]/)[0];

        if(domain === "www.youtube.com" || domain === "youtube.com" || domain === "www.youtu.be" || domain === "youtu.be") {
            $("#youtube_container").show();
            $("#download_type_disabled").val(0);
            $("#download_type").val(0);
        } else {
            $("#youtube_container").hide();
            $("#download_type_disabled").val(1);
            $("#download_type").val(1);
        }
    });
});