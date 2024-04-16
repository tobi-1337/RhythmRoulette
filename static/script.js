$(document).ready(function () {
    var selectedGenres = [];
    var searchedGenres = [];

    $('.genre-checkbox').change(function () {
        var checkedGenres = $('.genre-checkbox:checked');
        selectedGenres = [];
        checkedGenres.each(function () {
            selectedGenres.push($(this).val());
        });
        if (checkedGenres.length > 5) {
            alert("You can only choose up to 5 genres.");
            $(this).prop('checked', false);
            return;
        }
    });
    function dropdownFunction() {
        document.getElementById("myDropdown").classList.toggle("show");
    }
    
    window.onclick = function(event) {
        if (!event.target.matches('.dropdown_btn')) {
            var dropdowns = document.getElementsByClassName("dropdown_content");
            var i;
            for (i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
        }
    }
    $('.search-checkbox').change(function () {
        var checkedGenres = $('.search-checkbox:checked');
        searchedGenres = [];
        checkedGenres.each(function () {
            searchedGenres.push($(this).val());
        });
        if (checkedGenres.length > 3) {
            alert("You can only choose up to 3 decades.");
            $(this).prop('checked', false);
            return;
        }
    });

    $('#search_value').click(function (event) {
        event.preventDefault();
        if (selectedGenres.length > 0) {
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
                    // Handle error
                }
            });
        } else if (searchedGenres.length > 0) {
            $.ajax({
                url: '/search',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ decades: searchedGenres, search_limit: $('#search_limit').val() }),
                success: function (searchResponse) {
                    alert(searchResponse.message);
                    window.location.href = '/';
                },
                error: function (xhr, status, error) {
                    // Handle error
                }
            });
        } else {
            alert("Please select at least one genre or decade.");
        }
    });
});


const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})