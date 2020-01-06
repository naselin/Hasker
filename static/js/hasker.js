function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    var csrftoken = getCookie('csrftoken');
    $('a.vote').click(function (event) {
        var id = $(this).data('id');
        var vote = $(this).data('vote');
        var vtype = $(this).data('vtype');
        $.ajax({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                type: 'POST',
                data: {'vote': vote},
                url: '/vote/' + vtype + '/' + id + '/',
                success: function (data, status, xhr) {
                    var votes = data['rating'];
                    var votes_tag = $('p.votes-' + vtype + '-' + id);
                    votes_tag.text(votes);
                },
                error: function (xhr, status, exception) {
                    console.log(xhr, status, exception)
                }
            }
        );
    });
    $('a.mark').click(function (event) {
        var id = $(this).data('id');
        var qid = $(this).data('qid');
        var vote = $(this).data('vote');
        $.ajax({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                type: 'POST',
                url: '/mark/' + id + '/',
                success: function (data, status, xhr) {
                    window.location.reload(true)
                },
                error: function (xhr, status, exception) {
                    console.log(xhr, status, exception)
                }
            }
        );
    });
});