/**
 * Footer Fix Script
 * This script ensures the footer stays at the bottom of the page on all pages.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Function to ensure footer is at the bottom of the page
    function fixFooter() {
        const windowHeight = window.innerHeight;
        const bodyHeight = document.body.offsetHeight;
        const footer = document.querySelector('.footer');
        const main = document.querySelector('main');
        
        if (!footer || !main) return;
        
        // If page content is less than viewport height, adjust main content height
        if (bodyHeight < windowHeight) {
            const headerHeight = document.querySelector('header')?.offsetHeight || 0;
            const footerHeight = footer.offsetHeight || 0;
            const carouselHeight = document.querySelector('.carousel-container')?.offsetHeight || 0;
            
            // Calculate the space that main should fill
            const mainHeight = windowHeight - headerHeight - footerHeight - carouselHeight;
            
            if (mainHeight > 0) {
                main.style.minHeight = mainHeight + 'px';
            }
        }
    }
    
    // Run on page load
    fixFooter();
    
    // Run on window resize
    window.addEventListener('resize', fixFooter);
    
    // Run after images and other resources are loaded
    window.addEventListener('load', function() {
        fixFooter();
        
        // Run again after a slight delay to account for any dynamic content
        setTimeout(fixFooter, 500);
    });
    
    // Create a MutationObserver to watch for DOM changes
    const observer = new MutationObserver(function() {
        setTimeout(fixFooter, 300);
    });
    
    // Start observing the document body for changes
    observer.observe(document.body, { 
        childList: true, 
        subtree: true, 
        attributes: true,
        attributeFilter: ['style', 'class', 'height']
    });
});