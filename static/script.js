function searchFunction() {
    document.getElementById('genreSearch').classList.toggle("show");
}

function filterFunction() {
    var input, filter, div, genreItems, label, i, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    div = document.getElementById("genreSearch");
    genreItems = div.getElementsByClassName("genre-item");
    for (i = 0; i < genreItems.length; i++) {
        label = genreItems[i].getElementsByTagName("label")[0];
        txtValue = label.textContent || label.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            genreItems[i].style.display = "";
        } else {
            genreItems[i].style.display = "none";
        }
    }
}

function updateSelectedGenres() {
    var selectedGenresList = document.getElementById('selectedGenresList');
    var checkboxes = document.querySelectorAll('.genre-checkbox:checked');
    selectedGenresList.innerHTML = ''; // Rensa listan

    checkboxes.forEach(function(checkbox) {
        var listItem = document.createElement('li');
        listItem.textContent = checkbox.value;
        selectedGenresList.appendChild(listItem);
    });
}

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
            alert("Du kan max välja 5 genres.");
            $(this).prop('checked', false);
            return;
        }
        updateSelectedGenres();
    });
    
    $('.search-checkbox').change(function () {
        var checkedGenres = $('.search-checkbox:checked');
        searchedGenres = [];
        checkedGenres.each(function () {
            searchedGenres.push($(this).val());
        });
        if (checkedGenres.length > 3) {
            alert("Du kan max välja 3 årtal.");
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
                    window.location.href = '/redirect-playlist';
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
                    window.location.href = '/redirect-playlist';
                },
                error: function (xhr, status, error) {
                    // Handle error
                }
            });
        } else {
            alert("Du måste välja minst en genre/årtal!");
        }
    });
});


const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})

function updateRangeValue(value) {
    document.getElementById("rangeValue").innerText = value;
}


//Följande är en funktion för dropdown-meny vi inte använder.
/*
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
    */