document.getElementById('searchForm').addEventListener('submit', function(event) {
    const input = document.getElementById('searchInput');
    if (input.value.trim() === '') {
        event.preventDefault();
        input.value = '';
        input.focus();
    }
});
