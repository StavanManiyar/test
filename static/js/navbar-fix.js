// Navbar dropdown fix
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit to ensure Bootstrap is loaded
    setTimeout(function() {
        initializeDropdownFixes();
    }, 150);
});

function initializeDropdownFixes() {
    // Enhanced dropdown functionality
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');
    
    // Ensure dropdowns are positioned correctly
    function fixDropdownPosition() {
        dropdownMenus.forEach(menu => {
            const toggle = menu.previousElementSibling;
            if (toggle && toggle.classList.contains('dropdown-toggle')) {
                const rect = toggle.getBoundingClientRect();
                const viewport = {
                    width: window.innerWidth,
                    height: window.innerHeight
                };
                const menuWidth = 220; // Approximate menu width
                
                // Check if dropdown would overflow viewport
                const wouldOverflow = rect.left + menuWidth > viewport.width;
                
                // Force correct positioning
                menu.style.position = 'absolute';
                menu.style.zIndex = '99999';
                menu.style.top = '100%';
                menu.style.margin = '0';
                menu.style.transform = 'none';
                menu.style.maxWidth = '250px';
                menu.style.minWidth = '200px';
                menu.style.whiteSpace = 'nowrap';
                menu.style.overflow = 'hidden';
                
                // Position based on available space
                if (wouldOverflow) {
                    menu.style.left = 'auto';
                    menu.style.right = '0';
                } else {
                    menu.style.left = '0';
                    menu.style.right = 'auto';
                }
            }
        });
    }
    
    // Fix positioning on window resize
    window.addEventListener('resize', fixDropdownPosition);
    
    // Set up positioning for dropdowns before any Bootstrap events
    dropdownToggles.forEach((toggle, index) => {
        const parentNavItem = toggle.closest('.nav-item');
        const navItemsWithDropdowns = document.querySelectorAll('.navbar-nav .nav-item.dropdown');
        const dropdownIndex = Array.from(navItemsWithDropdowns).indexOf(parentNavItem);
        const totalDropdowns = navItemsWithDropdowns.length;
        
        // Last 2 dropdowns should be right-aligned
        const isRightAligned = dropdownIndex >= totalDropdowns - 2;
        
        const dropdownMenu = toggle.nextElementSibling;
        if (dropdownMenu) {
            // Pre-set positioning
            if (isRightAligned) {
                dropdownMenu.style.left = 'auto';
                dropdownMenu.style.right = '0';
                dropdownMenu.setAttribute('data-position', 'right');
            } else {
                dropdownMenu.style.left = '0';
                dropdownMenu.style.right = 'auto';
                dropdownMenu.setAttribute('data-position', 'left');
            }
        }
    });
    
    // Use Bootstrap events for better compatibility
    document.addEventListener('show.bs.dropdown', function(e) {
        const dropdownMenu = e.target.querySelector('.dropdown-menu');
        if (dropdownMenu) {
            fixDropdownPosition();
        }
    });
    
    // Fix positioning when dropdown is shown
    document.addEventListener('shown.bs.dropdown', function(e) {
        const dropdownMenu = e.target.querySelector('.dropdown-menu');
        if (dropdownMenu) {
            fixDropdownPosition();
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
    
    // Ensure dropdowns don't interfere with other content
    function preventOverlap() {
        const mainContent = document.querySelector('main');
        const carousel = document.querySelector('.carousel-container');
        const homeCarousel = document.querySelector('#home-carousel-container');
        const contentWrapper = document.querySelector('.content-wrapper');
        const navbarWrapper = document.querySelector('.navbar-wrapper');
        
        // Ensure navbar wrapper is properly positioned
        if (navbarWrapper) {
            navbarWrapper.style.position = 'relative';
            navbarWrapper.style.zIndex = '9999';
            navbarWrapper.style.top = '0';
            navbarWrapper.style.left = '0';
            navbarWrapper.style.right = '0';
            navbarWrapper.style.width = '100%';
        }
        
        // Force navbar to be visible above carousel
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.style.zIndex = '9999';
            navbar.style.position = 'relative';
            navbar.style.visibility = 'visible';
            navbar.style.opacity = '1';
        }
        
        if (mainContent) {
            mainContent.style.position = 'relative';
            mainContent.style.zIndex = '1';
        }
        
        if (carousel) {
            carousel.style.position = 'relative';
            carousel.style.zIndex = '1';
        }
        
        if (homeCarousel) {
            homeCarousel.style.position = 'relative';
            homeCarousel.style.zIndex = '1';
        }
        
        if (contentWrapper) {
            contentWrapper.style.position = 'relative';
            contentWrapper.style.zIndex = '1';
        }
    }
    
    // Mobile-specific fixes
    function handleMobileNavbar() {
        const isMobile = window.innerWidth <= 992;
        
        if (isMobile) {
            // Mobile view - ensure dropdowns work with Bootstrap's native mobile behavior
            dropdownMenus.forEach(menu => {
                // Reset all positioning for mobile
                menu.style.position = 'static';
                menu.style.zIndex = 'auto';
                menu.style.left = 'auto';
                menu.style.right = 'auto';
                menu.style.transform = 'none';
                menu.style.width = 'calc(100% - 40px)';
                menu.style.margin = '5px 0 10px 20px';
                menu.style.float = 'none';
                menu.style.clear = 'both';
                
                // Ensure proper display control
                if (!menu.classList.contains('show')) {
                    menu.style.display = 'none';
                }
            });
            
            // Ensure nav items are properly spaced
            const navItems = document.querySelectorAll('.navbar-nav .nav-item');
            navItems.forEach(item => {
                item.style.clear = 'both';
                item.style.width = '100%';
                item.style.display = 'block';
            });
        } else {
            // Desktop view - restore original positioning
            dropdownMenus.forEach(menu => {
                menu.style.margin = '';
                menu.style.float = '';
                menu.style.clear = '';
            });
            fixDropdownPosition();
        }
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        setTimeout(() => {
            handleMobileNavbar();
            fixDropdownPosition();
        }, 100);
    });
    
    // Apply fixes on load
    setTimeout(() => {
        handleMobileNavbar();
        fixDropdownPosition();
        preventOverlap();
    }, 100);
}
