$(document).ready(function() {
    $("#comment-form").submit(function(event) {
        event.preventDefault();
        var form = $(this);
        var postId = form.data("post_id");
    
      
        $.ajax({
          'url': "/add_comment/" + postId + "/",
          'type': "POST",
          'async': true,
          'dataType': 'json',
          'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'comment': $('#id_text').val()
          },
          success: function(response) {
            var commentsContainer = form.find(".comments");
            commentsContainer.append(response.comment_html);
            form.trigger("reset");
          },
          error: function(xhr) {
            console.log(xhr.responseText);
          }
        });
        form.attr('id', 'comment-form-' + postId);
    });


    $("#like-btn").click(function(event) {
    event.preventDefault();
    var btn = $(this);
    var form = btn.closest(".like-form");
    var postId = form.data("post-id");


    $.ajax({
        'url': "/post/" + postId + "/like/",
        'type': "POST",
        'data': {
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),

        },

        success: function(response) {
        // Оновлення відображення кількості лайків
        var likesCountContainer = $("#likes-count-" + postId);
        likesCountContainer.text(response.likes_count);

        // Зміна вигляду кнопки лайку
        btn.toggleClass("liked");
        },
        error: function(xhr) {
        console.log(xhr.responseText);
        }
        });
    });
});


$(document).ready(function() {
    addComment();
    addLike();
});

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return cookieValue ? cookieValue[2] : null;
}