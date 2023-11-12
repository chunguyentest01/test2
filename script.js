$(document).ready(function() {
    $('#show-chart-btn').click(function() {
        $.ajax({
            url: '/plot',
            method: 'GET',
            success: function(response) {
                var img = new Image();
                img.src = 'data:image/png;base64,' + response.image;
                $('#chart-container').html(img);
            }
        });
    });
});