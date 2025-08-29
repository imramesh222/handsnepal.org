document.addEventListener('DOMContentLoaded', function() {
    const languageToggle = document.getElementById('languageToggle');
    const languageDropdown = document.getElementById('languageDropdown');
    
    if (!languageToggle || !languageDropdown) return;
    
    const languageOptions = Array.from(document.querySelectorAll('.language-option'));
    
    // Initialize ARIA attributes
    languageToggle.setAttribute('aria-haspopup', 'true');
    languageToggle.setAttribute('aria-expanded', 'false');
    
    // Function to close dropdown
    const closeDropdown = () => {
        languageDropdown.classList.remove('show');
        languageToggle.setAttribute('aria-expanded', 'false');
    };
    
    // Toggle dropdown
    languageToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        
        // Close all other open dropdowns first
        document.querySelectorAll('.language-dropdown.show').forEach(dropdown => {
            if (dropdown !== languageDropdown) {
                dropdown.classList.remove('show');
                const toggle = dropdown.previousElementSibling;
                if (toggle && toggle.getAttribute('aria-expanded') === 'true') {
                    toggle.setAttribute('aria-expanded', 'false');
                }
            }
        });
        
        // Toggle current dropdown
        if (isExpanded) {
            closeDropdown();
        } else {
            // Position the dropdown before showing it
            const toggleRect = this.getBoundingClientRect();
            languageDropdown.style.top = `${toggleRect.bottom + window.scrollY}px`;
            languageDropdown.style.right = `${window.innerWidth - toggleRect.right}px`;
            
            // Show the dropdown
            languageDropdown.classList.add('show');
            this.setAttribute('aria-expanded', 'true');
            
            // Focus first option when opening
            const firstOption = languageDropdown.querySelector('.language-option');
            if (firstOption) firstOption.focus();
        }
    });
    
    // Handle window resize to reposition dropdown if open
    window.addEventListener('resize', function() {
        if (languageDropdown.classList.contains('show')) {
            const toggleRect = languageToggle.getBoundingClientRect();
            languageDropdown.style.top = `${toggleRect.bottom + window.scrollY}px`;
            languageDropdown.style.right = `${window.innerWidth - toggleRect.right}px`;
        }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!languageToggle.contains(e.target) && !languageDropdown.contains(e.target)) {
            closeDropdown();
        }
    });
    
    // Handle keyboard navigation for toggle button
    languageToggle.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
            e.preventDefault();
            this.click();
        } else if (e.key === 'Escape') {
            closeDropdown();
            this.focus();
        } else if (e.key === 'ArrowDown' && languageOptions.length > 0) {
            e.preventDefault();
            if (!languageDropdown.classList.contains('show')) {
                languageDropdown.classList.add('show');
                this.setAttribute('aria-expanded', 'true');
            }
            const firstOption = languageOptions[0];
            if (firstOption) firstOption.focus();
        } else if (e.key === 'ArrowUp' && languageOptions.length > 0) {
            e.preventDefault();
            if (!languageDropdown.classList.contains('show')) {
                languageDropdown.classList.add('show');
                this.setAttribute('aria-expanded', 'true');
            }
            languageOptions[languageOptions.length - 1].focus();
        }
    });
    
    // Handle keyboard navigation for dropdown options
    languageOptions.forEach((option, index) => {
        option.addEventListener('keydown', function(e) {
            const isLastItem = index === languageOptions.length - 1;
            const isFirstItem = index === 0;
            
            switch(e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    const nextItem = isLastItem ? languageOptions[0] : languageOptions[index + 1];
                    if (nextItem) nextItem.focus();
                    break;
                    
                case 'ArrowUp':
                    e.preventDefault();
                    if (isFirstItem) {
                        languageToggle.focus();
                    } else {
                        languageOptions[index - 1].focus();
                    }
                    break;
                    
                case 'Escape':
                    e.preventDefault();
                    closeDropdown();
                    languageToggle.focus();
                    break;
                    
                case 'Home':
                    e.preventDefault();
                    languageOptions[0].focus();
                    break;
                    
                case 'End':
                    e.preventDefault();
                    languageOptions[languageOptions.length - 1].focus();
                    break;
                    
                case 'Tab':
                    if (!e.shiftKey && isLastItem) {
                        // If tabbing forward from last option, close dropdown
                        closeDropdown();
                    } else if (e.shiftKey && isFirstItem) {
                        // If shift+tabbing from first option, focus the toggle
                        e.preventDefault();
                        languageToggle.focus();
                    }
                    break;
                    
                case ' ':
                case 'Enter':
                    e.preventDefault();
                    this.click();
                    break;
            }
        });
    });
});