function toggleFollow() {
    $.ajax({
        url: window.USER_FOLLOW_URL,
        success: function(data) {
            $("#followCount").html(data.follower_count + 'Followers');
            $('#followElement').html(data.button);
        }
    });
    location.reload("#namewrapper");

};


$(function() {
    $("#toggle").click(function() {
        if ($(this).is(":checked")) {
            $("#menu1").show();
            $("#menu2").hide();
        } else {
            $("#menu1").hide();
            $("#menu2").show();
        }
    });
});