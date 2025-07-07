document.addEventListener('DOMContentLoaded', function() {
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
