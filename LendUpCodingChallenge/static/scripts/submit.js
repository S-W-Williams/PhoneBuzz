$(document).ajaxStart(function () {
    $(document.body).css({ 'cursor': 'wait' });
}).ajaxStop(function () {
    $(document.body).css({ 'cursor': 'default' });
});

function refreshHistory() {
    $.ajax({
        url: '/history',
        type: 'POST',
        success: function (response) {
            $('#alert').show();
            var rows = [];
            for (i = 0; i < response.history.length; i++) {
                var date = moment(response.history[i][1]);
                rows.push("<tr>" +
                    "<td>" + response.history[i][3] + "</td>" +
                    "<td>" + date.format('MMMM Do YYYY, h:mm:ss a') + "</td>" +
                    "<td>" + response.history[i][2] + "</td>" +
                    "<td>" + response.history[i][4] + "</td>" +
                    "<td>" + "<button class='btn btn-sm btn-success' class='replayButton' onClick='replay(" + response.history[i][3] + "," + response.history[i][4] + ")'>Replay</button>" + "</td>" + "</tr>");
            }
            var html = rows.join('');
            $("#historyTable > tbody").html(html);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function submitCall() {
    var delay = $('input[name="delay"]').val();
    var url = ''
    if (delay === "0") 
        url = '/outbound';
    else 
        url = '/timed'
    
    $.ajax({
        url: url,
        data: { phoneNumber: $('input[name="phoneNumber"]').val(), delay: delay },
        type: 'POST',
        success: function (response) {
            if (response.status == 'OK') {
                $("#message").text('Sucess!');
            }
            else
                $("#message").text(response.message);
        },
        error: function (error) {
            $("#message").text("Unknown Error");
            console.log(error);
        }
    });
}

function replay(phoneNumber, n) {
    $.ajax({
        url: '/replay',
        data: { phoneNumber: phoneNumber, n: n },
        type: 'POST',
        success: function (response) {
            if (response.status == 'OK') {
                $("#message").text('Relayed!');
            }
            else
                $("#message").text(response.message);
        },
        error: function (error) {
            $("#message").text("Unknown Error");
            console.log(error);
        }
    });
}

$(document).ready(function () {
    $('#submitCall').bind('click', submitCall);
    $('#refreshHistory').bind('click', refreshHistory);
    refreshHistory();
});

