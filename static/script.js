$(document).ready(function () {
    var selectedGenres = [];
    var searchedGenres = [];

    $('.genre-checkbox').change(function () {
        var checkedGenres = $('.genre-checkbox:checked');

        if (checkedGenres.length > 5) {
            alert("Du kan endast välja upp till 5 genrer.");
            $(this).prop('checked', false);
            return;
        }

        selectedGenres = [];
        checkedGenres.each(function () {
            selectedGenres.push($(this).val());
        });
    });

    $('.search-checkbox').change(function () {
        var checkedGenres = $('.search-checkbox:checked');

        if (checkedGenres.length > 3) {
            alert("Du kan endast välja upp till 3 årtionden.");
            $(this).prop('checked', false);
            return;
        }

        searchedGenres = [];
        checkedGenres.each(function () {
            searchedGenres.push($(this).val());
        });
    });


    $('#save_value').click(function (event) {
        event.preventDefault();

        var selectedGenres = [];
        $('.genre-checkbox:checked').each(function () {
            selectedGenres.push($(this).val());
        });
    });
        $('#search_value').click(function (event) {
            event.preventDefault();

            var searchedGenres = [];
            $('.search-checkbox:checked').each(function () {
                searchedGenres.push($(this).val());
            });
        });
            if (selectedGenres > 0) {
                $.ajax({
                    url: '/recommendations',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ genres: selectedGenres, recco_limit: $('#recco_limit').val() }),
                    success: function (response) {
                        alert(response.message);
                        window.location.href = '/';
                    },
                    error: function (xhr, status, error) {
                    }
                });
            } else if (searchedGenres > 0) {
                        $.ajax({
                        url: '/search',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({ genres: searchedGenres, search_limit: $('#search_limit').val() }),
                        success: function (searchResponse) {
                            alert(response.message);
                            window.location.href = '/';
                        },
                        error: function (xhr, status, error) {
                    
                        }
                    
                    });
                }
            
        });