// Simple DataTables initialization with error handling
window.addEventListener('DOMContentLoaded', event => {
    try {
        // Check if Simple DataTables is loaded
        if (typeof simpleDatatables === 'undefined') {
            console.warn('Simple DataTables is not loaded. Make sure it is included before this script.');
            return;
        }

        // Initialize DataTable if the element exists
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
    } catch (error) {
        console.error('Error initializing DataTable:', error);
    }
});
