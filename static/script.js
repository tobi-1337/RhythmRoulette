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
        event.preventDefault();
        // Samla in de valda genrerna
        var selectedGenres = [];
        $('.genre-checkbox:checked').each(function() {
            selectedGenres.push($(this).val());
        });
    
        // Skicka valda värden till Python med AJAX
        $.ajax({
            url: '/recommendations',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ genres: selectedGenres, recco_limit: $('#recco_limit').val() }),
            success: function(response) {
                // Behandla svaret från Python
                alert(response.message); // Visa ett meddelande för användaren
                window.location.href = '/'; // Omdirigera användaren till startsidan
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});