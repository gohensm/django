function addComment() {
    $('#add').click(function() {
        let btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'text': $('#id_body').val()
            },
            'success': function(data) {
                document.getElementById('comments').innerHTML += data;
            }
        });
    });
}

function addLike() {
    $('.like').click(function() {
        let btn = $(this);
        $.ajax(btn.data('user'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'like': 1
            },
            'success': function(data) {
                document.getElementById('likes').innerHTML = data['like_amount'];
            }
        });
    });
}

$(document).ready(function() {
    addComment();
    addLike();
});

function openDialogue1(){
    $('#open').click(function(){
        document.getElementById('dialogue_1').show();
    })
}


function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return cookieValue ? cookieValue[2] : null;
}