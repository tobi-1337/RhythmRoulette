$(document).ready(function() {
    var selectedGenres = [];

    $('.genre-checkbox').change(function() {
        var checkedGenres = $('.genre-checkbox:checked');
        
        if (checkedGenres.length > 5) {
            alert("Du kan endast välja upp till 5 genrer.");
            $(this).prop('checked', false);
            return;
        }

        selectedGenres = [];
        checkedGenres.each(function() {
            selectedGenres.push($(this).val());
        });
    });


    $('#save_value').click(function() {
        // Skicka valda värden till Python med AJAX
        $.ajax({
            url: '/recommendations',
            type: 'POST',
            data: { genres: selectedGenres, recco_limit: $('#recco_limit').val() },
            success: function(response) {
                // Behandla svaret från Python
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});