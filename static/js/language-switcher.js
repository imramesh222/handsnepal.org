document.addEventListener('DOMContentLoaded', function() {
    const languageToggle = document.getElementById('languageToggle');
    const languageDropdown = document.getElementById('languageDropdown');
    const currentLanguage = document.querySelector('.current-language');
    const languageOptions = document.querySelectorAll('.language-option');
    const csrfToken = getCSRFToken();

    // Toggle dropdown
    if (languageToggle) {
        languageToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            if (languageDropdown) {
                languageDropdown.classList.toggle('show');
            }
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
        if (languageDropdown) {
            languageDropdown.classList.remove('show');
        }
    });

    // Handle language selection
    languageOptions.forEach(option => {
        option.addEventListener('click', function(e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            if (lang) {
                setLanguage(lang);
            }
        });
    });

    // Set language function
    function setLanguage(lang) {
        if (!lang) return;
        
        // Create form data
        const formData = new URLSearchParams();
        formData.append('language', lang);
        formData.append('next', window.location.pathname);
        formData.append('csrfmiddlewaretoken', csrfToken);

        // Send AJAX request to set language
        fetch('/i18n/setlang/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            },
            body: formData,
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                console.error('Language switch failed:', data.message || 'Unknown error');
                // Fallback to page reload with language parameter
                window.location.href = `/${lang}${window.location.pathname}`;
            }
        })
        .catch(error => {
            console.error('Error switching language:', error);
            // Fallback to page reload with language parameter
            window.location.href = `/${lang}${window.location.pathname}`;
        });
    }

    // Helper function to get CSRF token
    function getCSRFToken() {
        // Try to get from meta tag
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag) {
            return metaTag.getAttribute('content');
        }

        // Fallback to cookie
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
            
        if (cookieValue) {
            return decodeURIComponent(cookieValue);
        }

        console.warn('CSRF token not found');
        return '';
    }
});