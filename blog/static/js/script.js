$(document).ready(function(){
    $('.like-btn').click(function(){
        $.ajax({
            method: 'POST',
            url: $(this).data('url'),
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.liked) {
                    console.log('liked')
                } else {
                    console.log('unlike')
                }
                $('.likes').text(response.total_likes)
            }
        })
    })
})