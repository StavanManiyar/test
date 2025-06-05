document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap carousel
    var carousel = document.querySelector('#homeCarousel');
    if (carousel) {
        new bootstrap.Carousel(carousel, {
            interval: 5000,
            wrap: true,
            keyboard: true
        });
    }
    // Function to adjust footer position
    function adjustFooter() {
        const body = document.body;
        const main = document.querySelector('main');
        const footer = document.querySelector('.footer');
        
        if (!footer || !main) return;
        
        // Ensure the body has the necessary classes for flexbox layout
        if (!body.classList.contains('d-flex')) {
            body.style.display = 'flex';
            body.style.flexDirection = 'column';
            body.style.minHeight = '100vh';
        }
        
        // Ensure main content grows to fill available space
        main.style.flex = '1 0 auto';
        
        // For pages with minimal content, add a minimum height to main
        const windowHeight = window.innerHeight;
        const contentHeight = document.body.scrollHeight;
        
        // If content is less than viewport, ensure main fills available space
        if (contentHeight < windowHeight) {
            const headerHeight = document.querySelector('header')?.offsetHeight || 0;
            const footerHeight = footer.offsetHeight || 0;
            const carouselHeight = document.querySelector('#homeCarousel')?.offsetHeight || 0;
            
            // Calculate minimum height needed
            const minHeight = windowHeight - headerHeight - footerHeight - carouselHeight;
            
            if (minHeight > 0) {
                main.style.minHeight = `${minHeight}px`;
            }
        }
    }
    
    // Call the function on initial load
    adjustFooter();
    
    // Call on resize
    window.addEventListener('resize', function() {
        adjustFooter();
    });

    // Call after the page is fully loaded with a slight delay
    window.addEventListener('load', function() {
        // Initial adjustment
        adjustFooter();
        
        // Delayed adjustment to account for any dynamic content
        setTimeout(function() {
            adjustFooter();
        }, 500);
    });

    // Create a MutationObserver to watch for DOM changes
    const observer = new MutationObserver(function(mutations) {
        // Delay the adjustment slightly to allow DOM to settle
        setTimeout(function() {
            adjustFooter();
        }, 300);
    });

    // Start observing the document with the configured parameters
    observer.observe(document.body, { childList: true, subtree: true, attributes: true });

    // Wait for images to load before final adjustment
    window.addEventListener('load', function() {
        const images = document.querySelectorAll('img');
        let loadedImages = 0;
        
        if (images.length === 0) {
            adjustFooter();
            return;
        }
        
        images.forEach(function(img) {
            if (img.complete) {
                loadedImages++;
                if (loadedImages === images.length) {
                    adjustFooter();
                }
            } else {
                img.addEventListener('load', function() {
                    loadedImages++;
                    if (loadedImages === images.length) {
                        adjustFooter();
                    }
                });
                
                img.addEventListener('error', function() {
                    loadedImages++;
                    if (loadedImages === images.length) {
                        adjustFooter();
                    }
                });
            }
        });
    });
    
    // Add a periodic check and adjustment after DOMContentLoaded for 5 seconds
    document.addEventListener('DOMContentLoaded', function() {
        let checkCount = 0;
        const maxChecks = 10; // 10 checks at 500ms intervals = 5 seconds
        
        const intervalId = setInterval(function() {
            adjustFooter();
            checkCount++;
            
            if (checkCount >= maxChecks) {
                clearInterval(intervalId);
            }
        }, 500);
    });
    
    // Fix for navbar dropdown issues
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    // Close all other dropdowns when one is opened
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            // Prevent default behavior
            e.preventDefault();
            
            // Get the parent dropdown item
            const parentDropdown = this.closest('.dropdown');
            
            // Check if this dropdown is already open
            const isOpen = parentDropdown.classList.contains('show');
            
            // Close all dropdowns
            document.querySelectorAll('.dropdown').forEach(dropdown => {
                dropdown.classList.remove('show');
                const dropdownMenu = dropdown.querySelector('.dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.classList.remove('show');
                }
            });
            
            // If the clicked dropdown wasn't open, open it
            if (!isOpen) {
                parentDropdown.classList.add('show');
                const dropdownMenu = parentDropdown.querySelector('.dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.classList.add('show');
                }
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown').forEach(dropdown => {
                dropdown.classList.remove('show');
                const dropdownMenu = dropdown.querySelector('.dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.classList.remove('show');
                }
            });
        }
    });
    
    // Map functionality for contact page
    if (document.querySelector('.map-tab-btn')) {
        const mapButtons = document.querySelectorAll('.map-tab-btn');
        
        // Add click event listeners to map buttons
        mapButtons.forEach(button => {
            button.addEventListener('click', function() {
                const mapId = this.getAttribute('onclick').match(/'([^']+)'/)[1];
                showMap(mapId);
            });
        });
        
        // Initialize the first map (map1) by default
        showMap('map1');
    }
});

// Function to show selected map
function showMap(mapId) {
    // Hide all maps
    document.querySelectorAll('.map-container iframe').forEach(function(iframe) {
        iframe.style.display = 'none';
    });
    
    // Show selected map
    document.getElementById(mapId).style.display = 'block';
    
    // Update active button
    document.querySelectorAll('.map-tab-btn').forEach(function(btn) {
        btn.classList.remove('active');
    });
    
    // Find the button that triggered this and add active class
    document.querySelectorAll('.map-tab-btn').forEach(function(btn) {
        if (btn.getAttribute('onclick').includes(mapId)) {
            btn.classList.add('active');
        }
    });
}
