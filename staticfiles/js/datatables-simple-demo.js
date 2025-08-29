// Simple DataTables initialization
window.addEventListener('DOMContentLoaded', event => {
    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple, {
            searchable: true,
            fixedHeight: true,
            perPage: 10,
            labels: {
                placeholder: "Search...",
                perPage: "{select} entries per page",
                noRows: "No entries found",
                info: "Showing {start} to {end} of {rows} entries"
            }
        });
    }
});
