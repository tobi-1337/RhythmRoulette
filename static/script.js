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


    $('#save_value').click(function(event) {
        event.preventDefault();
        
        var selectedGenres = [];
        $('.genre-checkbox:checked').each(function() {
            selectedGenres.push($(this).val());
        });
    
        
        $.ajax({
            url: '/recommendations',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ genres: selectedGenres, recco_limit: $('#recco_limit').val() }),
            success: function(response) {
                
                alert(response.message); 
                window.location.href = '/'; 
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});