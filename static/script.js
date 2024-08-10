document.getElementById('toggle-button').addEventListener('click', function() {
    const searchContainer = document.querySelector('.search-container');
    if (searchContainer.classList.contains('hidden')) {
        searchContainer.classList.remove('hidden');
        this.classList.remove('rotated');
    } else {
        searchContainer.classList.add('hidden');
        this.classList.add('rotated');
    }
});
