/**
 * Scrollbar Fix for Double Scrollbar Issue
 * This script ensures proper scrollbar behavior across different browsers
 * and prevents the double scrollbar issue that occurs during page loading
 */

(function() {
    'use strict';
    
    // Fix for double scrollbar issue
    function fixScrollbars() {
        // Simple fix - ensure only HTML has the main scrollbar
        document.documentElement.style.overflowX = 'hidden';
        document.documentElement.style.overflowY = 'auto';
        
        // Prevent body from creating additional scrollbars
        document.body.style.overflowX = 'hidden';
        
        // Fix container overflow issues but not navbar containers
        const containers = document.querySelectorAll('.container, .container-fluid');
        containers.forEach(container => {
            // Don't apply overflow hidden to navbar containers
            if (!container.closest('.navbar')) {
                container.style.overflowX = 'hidden';
                container.style.maxWidth = '100%';
            }
        });
        
        // Fix main content overflow
        const main = document.querySelector('main');
        if (main) {
            main.style.overflowX = 'hidden';
            main.style.width = '100%';
            main.style.maxWidth = '100%';
        }
        
        // Ensure navbar is visible
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.style.visibility = 'visible';
            navbar.style.display = 'flex';
        }
    }
    
    // Run on DOM content loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixScrollbars);
    } else {
        fixScrollbars();
    }
    
    // Run on window load as well (for any dynamic content)
    window.addEventListener('load', fixScrollbars);
    
    // Run on window resize to handle responsive changes
    window.addEventListener('resize', function() {
        setTimeout(fixScrollbars, 100);
    });
    
    // Monitor for dynamic content changes
    if (window.MutationObserver) {
        const observer = new MutationObserver(function(mutations) {
            let shouldFix = false;
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    shouldFix = true;
                }
            });
            if (shouldFix) {
                setTimeout(fixScrollbars, 50);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
})();
