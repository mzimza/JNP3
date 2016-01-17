var host = document.location.host;
$(document).ready(function() {
    showTweets(host, true);
});

$('table').on({
    click: function(){
        var tweet_id = $(this).parent().parent().find('.id').text();
        $.ajax({
            url: 'http://' + host + '/tweet/' + tweet_id + '/',
            type: 'DELETE',
            success: function(data){
                showTweets(host);
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr, errmsg, err);
            }
        });
    }
}, '.delete-tweet'
);

$('table').on({
    click: function() {
        var tweet_id = $(this).parent().find('.id').text();
        $.ajax({
            url: 'http://' + host + '/like/' + tweet_id + '/',
            type: 'POST',
            success: function(){
                var new_value = parseInt($('#'+tweet_id).find('.likes').text())  + 1;
                $('#'+tweet_id).find('.likes').text(new_value);
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr, errmsg, err);
            }
        });
    }
}, '.likes'
);

$('table').on({
    click: function() {
        var tweet_id = $(this).parent().parent().find('.id').text();
        $.ajax({
            url: 'http://' + host + '/retweet/' + tweet_id + '/',
            type: 'POST',
            success: function(){
                var new_value = parseInt($('#'+tweet_id).find('.shares').text())  + 1;
                $('#'+tweet_id).find('.shares').text(new_value);
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr, errmsg, err);
            }
        });
    }
}, '.retweet-tweet'
);

var addButtonInfoCell = function (cellID, type, show, origin) {
    if (show) {
        var btn = document.createElement("input");
        btn.type = "button";
        btn.name = type;
        btn.value = type.charAt(0).toUpperCase() + type.slice(1);
        var my_class = type + '-tweet';
        $('th.'+my_class).text('');
        if (type.charAt(0) == 'd') {
            my_class += ' btn-danger';
        }
        else {
            my_class += ' btn-primary';
        }
        btn.className="btn btn-xs " + my_class;
        cellID.appendChild(btn);
    }
    else {
        var col_name = 'th#' + type + 'Header';
        if (type.charAt(0) == 'r') {
            if ($(col_name).text() === '') {
                $(col_name).text('Retweeted from');
            }
            if (origin) {
                getTweet(origin, function(data){
                    cellID.appendChild(document.createTextNode(data.author.first_name + ' ' + data.author.last_name));
                });
            }
        }
        else {
            if ($(col_name).text() === '') {
                $(col_name).text('Author');
            }
            if (origin) {
                cellID.appendChild(document.createTextNode(origin.first_name + ' ' + origin.last_name));
            }
        }
    }
};


function addRow(tableID, data, show_delete, show_retweet) {
    var tableRef = document.getElementById(tableID);
    var newRow   = tableRef.insertRow();
    newRow.id = data.id;
    var idCell = newRow.insertCell(0);
    idCell.className = 'id';
    idCell.style.display = 'none';
    idCell.appendChild(document.createTextNode(data.id));
    var textCell = newRow.insertCell(1);
    textCell.className = 'tweet';
    textCell.appendChild(document.createTextNode(data.text));
    var likesCell = newRow.insertCell(2);
    likesCell.appendChild(document.createTextNode(data.likes));
    likesCell.className = 'likes';
    var sharesCell = newRow.insertCell(3);
    sharesCell.className = 'shares';
    sharesCell.appendChild(document.createTextNode(data.shares));
    var retweetCell = newRow.insertCell(4);
    addButtonInfoCell(retweetCell, 'retweet', show_retweet, data.origin);
    var deleteCell = newRow.insertCell(5);
    addButtonInfoCell(deleteCell, 'delete', show_delete, data.author);
};

var getTweet = function(tweet_id, handler) {
    $.ajax({
        url: 'http://' + host + '/tweet/' + tweet_id + '/',
        type: 'GET',
        headers: {
            'Content-Type' : 'application/json',
        },
        success: function(data) {
            handler(data);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr, errmsg, err);
        }
    });
};

var showTweets = function(host) {
    $.ajax({
        url: 'http://' + host + '/wall/',
        type: 'GET',
        headers: {
            'Content-Type' : 'application/json',
        },
        success: function(data) {
            $('#tweetBody').empty();
            data.forEach(function(element, index){
                addRow('tweetBody', element, true, false);
            });
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr, errmsg, err);
        }
    });
};


$('#publishTweet').on({
     click: function() {
         var tweet = $("#newTweetText").val();
         var data = {'text' : tweet};
         $.ajax({
            url: 'http://' + host + '/tweet/',
            type: 'POST',
            headers: {
                    'Content-Type': 'application/json',
            },
            data: JSON.stringify(data),
            success: function() {
                $("#newTweetText").val('');
                showTweets(host, true);
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr, errmsg, err);
            },
         });
    }
});

$('#home').on({
    click: function() {
        $('#home').parent().find('li').each(function(){
            $(this).removeClass('active');
        });
        $('#home').addClass('active');
        //var host = document.location.host;
        location.href='http://' + host + '/home/';
    }
});

$('#popularTweets').on({
    click: function() {
        $('#popularTweets').parent().find('li').each(function(){
              $(this).removeClass('active');
        });
        $('#popularTweets').addClass('active');
        $.ajax({
            url: 'http://' + host + '/popular/',
            type: 'GET',
            success: function(data) {
                $('#tweetBody').empty();
                data.forEach(function(element, index){
                    addRow('tweetBody', element, false, true);
                });
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr, errmsg, err);
            },
        });
    }
});

$('#newestTweets').on({
    click: function() {
        $('#newestTweets').parent().find('li').each(function(){
              $(this).removeClass('active');
        });
        $('#newestTweets').addClass('active');
        $.ajax({
            url: 'http://' + host + '/newest/',
            type: 'GET',
            success: function(data) {
                $('#tweetBody').empty();
                data.forEach(function(element, index){
                    addRow('tweetBody', element, false, true);
                });
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr, errmsg, err);
            },
        });
    }
});