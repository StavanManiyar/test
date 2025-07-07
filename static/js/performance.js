// Performance Optimizations for Kapadia High School Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all performance optimizations
    initLazyLoading();
    initImageOptimization();
    initCacheOptimization();
    initServiceWorker();
    initPerformanceMonitoring();
});

// Lazy Loading Images
function initLazyLoading() {
    // Use Intersection Observer for lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    loadImage(img);
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });

        // Observe all images with lazy-image class
        document.querySelectorAll('.lazy-image, img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for older browsers
        loadAllImages();
    }
}

function loadImage(img) {
    // Add loading skeleton
    img.classList.add('image-skeleton');
    
    const src = img.dataset.src || img.src;
    if (!src) return;

    const imageLoader = new Image();
    imageLoader.onload = function() {
        img.src = this.src;
        img.classList.remove('image-skeleton');
        img.classList.add('loaded');
        
        // Trigger fade-in animation
        requestAnimationFrame(() => {
            img.style.opacity = '1';
        });
    };
    
    imageLoader.onerror = function() {
        img.classList.remove('image-skeleton');
        img.src = '/static/images/placeholder.jpg'; // Add a placeholder image
        img.alt = 'Image not available';
    };
    
    imageLoader.src = src;
}

function loadAllImages() {
    // Fallback for browsers without Intersection Observer
    document.querySelectorAll('.lazy-image, img[data-src]').forEach(loadImage);
}

// Image Optimization
function initImageOptimization() {
    // Preload critical images
    preloadCriticalImages();
    
    // Optimize image formats based on browser support
    optimizeImageFormats();
    
    // Implement progressive image loading
    implementProgressiveLoading();
}

function preloadCriticalImages() {
    const criticalImages = [
        '/static/images/logo.png',
        '/static/images/hero-bg.jpg'
    ];
    
    criticalImages.forEach(src => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = src;
        document.head.appendChild(link);
    });
}

function optimizeImageFormats() {
    // Check for WebP support
    const webpSupported = checkWebPSupport();
    
    if (webpSupported) {
        // Convert JPEG/PNG sources to WebP where available
        document.querySelectorAll('img[data-webp]').forEach(img => {
            img.src = img.dataset.webp;
        });
    }
}

function checkWebPSupport() {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 1;
    return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
}

function implementProgressiveLoading() {
    // Load low-quality placeholders first, then high-quality images
    document.querySelectorAll('.progressive-image').forEach(container => {
        const lowQualityImg = container.querySelector('.low-quality');
        const highQualityImg = container.querySelector('.high-quality');
        
        if (lowQualityImg && highQualityImg) {
            lowQualityImg.onload = function() {
                this.style.opacity = '1';
                
                // Start loading high-quality image
                const highQualityLoader = new Image();
                highQualityLoader.onload = function() {
                    highQualityImg.src = this.src;
                    highQualityImg.onload = function() {
                        this.style.opacity = '1';
                        lowQualityImg.style.opacity = '0';
                    };
                };
                highQualityLoader.src = highQualityImg.dataset.src;
            };
        }
    });
}

// Cache Optimization
function initCacheOptimization() {
    // Implement client-side caching for API responses
    const cache = new Map();
    const cacheTimeout = 5 * 60 * 1000; // 5 minutes
    
    window.cachedFetch = function(url, options = {}) {
        const cacheKey = url + JSON.stringify(options);
        const cached = cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < cacheTimeout) {
            return Promise.resolve(cached.data);
        }
        
        return fetch(url, options)
            .then(response => response.json())
            .then(data => {
                cache.set(cacheKey, {
                    data: data,
                    timestamp: Date.now()
                });
                return data;
            });
    };
    
    // Clear cache periodically
    setInterval(() => {
        const now = Date.now();
        for (const [key, value] of cache.entries()) {
            if (now - value.timestamp > cacheTimeout) {
                cache.delete(key);
            }
        }
    }, cacheTimeout);
}

// Service Worker for Offline Support
function initServiceWorker() {
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('SW registered: ', registration);
                })
                .catch(registrationError => {
                    console.log('SW registration failed: ', registrationError);
                });
        });
    }
}

// Performance Monitoring
function initPerformanceMonitoring() {
    // Monitor Core Web Vitals
    if ('PerformanceObserver' in window) {
        // Largest Contentful Paint
        new PerformanceObserver((entryList) => {
            for (const entry of entryList.getEntries()) {
                console.log('LCP:', entry.startTime);
                // Send to analytics if needed
            }
        }).observe({entryTypes: ['largest-contentful-paint']});
        
        // First Input Delay
        new PerformanceObserver((entryList) => {
            for (const entry of entryList.getEntries()) {
                console.log('FID:', entry.processingStart - entry.startTime);
                // Send to analytics if needed
            }
        }).observe({entryTypes: ['first-input']});
        
        // Cumulative Layout Shift
        new PerformanceObserver((entryList) => {
            for (const entry of entryList.getEntries()) {
                if (!entry.hadRecentInput) {
                    console.log('CLS:', entry.value);
                    // Send to analytics if needed
                }
            }
        }).observe({entryTypes: ['layout-shift']});
    }
    
    // Monitor page load performance
    window.addEventListener('load', () => {
        setTimeout(() => {
            const navigation = performance.getEntriesByType('navigation')[0];
            console.log('Page Load Time:', navigation.loadEventEnd - navigation.fetchStart);
            
            // Report slow pages
            if (navigation.loadEventEnd - navigation.fetchStart > 3000) {
                console.warn('Slow page load detected');
                // Send to monitoring service if needed
            }
        }, 0);
    });
}

// Optimized Campus Gallery Functions
window.CampusGallery = {
    // Initialize campus photo gallery with lazy loading
    init: function() {
        this.setupLightbox();
        this.setupInfiniteScroll();
        this.setupImageFilters();
    },
    
    setupLightbox: function() {
        const lightbox = document.getElementById('lightbox');
        const lightboxImg = document.getElementById('lightbox-img');
        let currentImages = [];
        let currentIndex = 0;
        
        // Handle image clicks
        document.addEventListener('click', (e) => {
            if (e.target.matches('.campus-photo-item img, .gallery-card-image img')) {
                e.preventDefault();
                
                // Get all images in the current gallery
                const galleryContainer = e.target.closest('.campus-photo-grid, .gallery-grid');
                currentImages = Array.from(galleryContainer.querySelectorAll('img'));
                currentIndex = currentImages.indexOf(e.target);
                
                this.showLightbox(e.target.src);
            }
        });
        
        // Navigation
        document.getElementById('lightbox-next')?.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % currentImages.length;
            this.showLightbox(currentImages[currentIndex].src);
        });
        
        document.getElementById('lightbox-prev')?.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
            this.showLightbox(currentImages[currentIndex].src);
        });
    },
    
    showLightbox: function(src) {
        const lightbox = document.getElementById('lightbox');
        const lightboxImg = document.getElementById('lightbox-img');
        
        if (lightbox && lightboxImg) {
            lightboxImg.src = src;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    },
    
    setupInfiniteScroll: function() {
        const galleryContainer = document.querySelector('.gallery-grid');
        if (!galleryContainer) return;
        
        let loading = false;
        let page = 1;
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !loading) {
                    this.loadMoreImages(++page);
                }
            });
        });
        
        // Observe the last image in the gallery
        const lastImage = galleryContainer.querySelector('.gallery-card:last-child');
        if (lastImage) {
            observer.observe(lastImage);
        }
    },
    
    loadMoreImages: function(page) {
        // Implementation for loading more images via AJAX
        // This would connect to your Django view with pagination
        console.log('Loading page:', page);
    },
    
    setupImageFilters: function() {
        const filterButtons = document.querySelectorAll('.gallery-filter');
        const images = document.querySelectorAll('.gallery-card');
        
        filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const filter = button.dataset.filter;
                
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Filter images
                images.forEach(image => {
                    if (filter === 'all' || image.dataset.category === filter) {
                        image.style.display = 'block';
                        image.classList.add('fade-in');
                    } else {
                        image.style.display = 'none';
                    }
                });
            });
        });
    }
};

// Initialize campus gallery on load
document.addEventListener('DOMContentLoaded', () => {
    window.CampusGallery.init();
});

// Utility Functions
window.Utils = {
    // Debounce function for performance
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function for scroll events
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    },
    
    // Check if element is in viewport
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
};

// Error Handling
window.addEventListener('error', (e) => {
    console.error('JavaScript error:', e.error);
    // Send to error tracking service if needed
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    // Send to error tracking service if needed
});
