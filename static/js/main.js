document.addEventListener('DOMContentLoaded', function() {
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
