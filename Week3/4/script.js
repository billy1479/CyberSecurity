// this script gets loaded once the page is ready
$(document).ready(function () {

    // some jQuery to handle clicking the menu links
    $('ul.sidenav li').click(function () {
        var index = $(this).attr('data-index');
        $('.content').addClass('hidden');
        $('#' + index).removeClass('hidden');
        $('ul.sidenav li a').removeClass('active').addClass('inactive');
        $('a', this).removeClass('inactive').addClass('active');
    });

    // message submit clicked
    $("#submit").click(function (e) {
        e.preventDefault();
        // send messages to server and update result with server data
        $.post("message", { Name: $('#nameInput')[0].value, Message: $('#messageInput')[0].value }, function (data) {
            $("#result").html(data);
            $("#result").scrollTop(1E10);
        });
    });

    // refresh clicked
    $("#refresh").click(function (e) {
        e.preventDefault();
        $.post("message", function (data) {
            $("#result").html(data);
            $("#result").scrollTop(1E10);
        });
    });

    // login button clicked 
    $("#login").click(function (e) {
        e.preventDefault();
        // get messages from server
        $.post("login", 'Password='+$('#password')[0].value, function (data) {
            $("#private").html(data);
            // document.cookie = "key=" + data;
            $("#private").removeClass("hidden");
            $("#refresh").click();
        });
    });

    $("#refresh").click();
});