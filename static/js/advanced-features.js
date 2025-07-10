// Advanced JavaScript Features for School Website

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Animated Counter with Intersection Observer
    const animatedCounters = document.querySelectorAll('.animated-counter');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const duration = parseInt(counter.getAttribute('data-duration')) || 2000;
                
                animateCounter(counter, target, duration);
                counterObserver.unobserve(counter);
            }
        });
    });
    
    animatedCounters.forEach(counter => {
        counterObserver.observe(counter);
    });
    
    function animateCounter(element, target, duration) {
        const startTime = Date.now();
        const startValue = 0;
        
        function update() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = Math.floor(startValue + (target - startValue) * progress);
            element.textContent = currentValue.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        update();
    }
    
    // 2. Smooth Scroll with Offset for Fixed Header
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.navbar')?.offsetHeight || 0;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 3. Parallax Effect for Background Images
    const parallaxElements = document.querySelectorAll('.parallax-bg');
    
    function updateParallax() {
        parallaxElements.forEach(element => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            element.style.transform = `translateY(${rate}px)`;
        });
    }
    
    window.addEventListener('scroll', updateParallax);
    
    // 4. Sticky Navigation with Color Change
    const navbar = document.querySelector('.navbar');
    const stickyThreshold = 100;
    
    function handleStickyNavbar() {
        if (window.scrollY > stickyThreshold) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    }
    
    window.addEventListener('scroll', handleStickyNavbar);
    
    // 5. Image Lazy Loading with Fade-in Effect
    const lazyImages = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('fade-in');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => {
        imageObserver.observe(img);
    });
    
    // 6. Testimonial Slider with Auto-play (only for non-carousel testimonials)
    const testimonialSlider = document.querySelector('.testimonial-slider');
    if (testimonialSlider && !document.querySelector('#homeCarousel')) {
        // Only initialize if there's no home carousel on the page
        let currentSlide = 0;
        const slides = testimonialSlider.querySelectorAll('.testimonial-slide');
        const totalSlides = slides.length;
        
        // Check if already initialized
        if (testimonialSlider.hasAttribute('data-slider-initialized')) {
            return;
        }
        testimonialSlider.setAttribute('data-slider-initialized', 'true');
        
        function showSlide(index) {
            slides.forEach((slide, i) => {
                slide.classList.toggle('active', i === index);
            });
        }
        
        function nextSlide() {
            currentSlide = (currentSlide + 1) % totalSlides;
            showSlide(currentSlide);
        }
        
        // Auto-play testimonials (only if totalSlides > 1)
        if (totalSlides > 1) {
            setInterval(nextSlide, 5000);
        }
        
        // Manual navigation
        const prevBtn = testimonialSlider.querySelector('.prev-btn');
        const nextBtn = testimonialSlider.querySelector('.next-btn');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
                showSlide(currentSlide);
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', nextSlide);
        }
    }
    
    // 7. Progress Bars Animation
    const progressBars = document.querySelectorAll('.progress-bar-animated');
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.getAttribute('data-width');
                
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 500);
                
                progressObserver.unobserve(progressBar);
            }
        });
    });
    
    progressBars.forEach(bar => {
        progressObserver.observe(bar);
    });
    
    // 8. Modal with Enhanced Animations
    const modalTriggers = document.querySelectorAll('[data-modal-target]');
    const modals = document.querySelectorAll('.modal');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const targetModal = document.querySelector(this.getAttribute('data-modal-target'));
            if (targetModal) {
                targetModal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });
    
    modals.forEach(modal => {
        const closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
            });
        }
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    });
    
    // 9. Typing Animation
    const typingElements = document.querySelectorAll('.typing-text');
    
    function typeText(element, text, speed = 50) {
        let i = 0;
        element.textContent = '';
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }
    
    const typingObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const text = element.getAttribute('data-text');
                const speed = parseInt(element.getAttribute('data-speed')) || 50;
                
                typeText(element, text, speed);
                typingObserver.unobserve(element);
            }
        });
    });
    
    typingElements.forEach(element => {
        typingObserver.observe(element);
    });
    
    // 10. Enhanced Form Validation with Animations
    const forms = document.querySelectorAll('.animated-form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (this.value === '') {
                    this.parentElement.classList.remove('focused');
                }
            });
            
            input.addEventListener('input', function() {
                validateField(this);
            });
        });
    });
    
    function validateField(field) {
        const value = field.value.trim();
        const fieldContainer = field.parentElement;
        
        fieldContainer.classList.remove('error', 'success');
        
        if (value === '') {
            fieldContainer.classList.add('error');
            return false;
        } else if (field.type === 'email' && !isValidEmail(value)) {
            fieldContainer.classList.add('error');
            return false;
        } else {
            fieldContainer.classList.add('success');
            return true;
        }
    }
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // 11. Lightbox Gallery
    const galleryImages = document.querySelectorAll('.gallery-image');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxClose = document.querySelector('.lightbox-close');
    
    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            const fullSrc = this.getAttribute('data-full-src') || this.src;
            lightboxImg.src = fullSrc;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });
    
    if (lightboxClose) {
        lightboxClose.addEventListener('click', closeLightbox);
    }
    
    if (lightbox) {
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
    }
    
    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
    
    // 12. Back to Top Button with Smooth Animation
    const backToTopBtn = document.querySelector('.back-to-top');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });
        
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // 13. Preloader
    const preloader = document.querySelector('.preloader');
    
    window.addEventListener('load', function() {
        if (preloader) {
            preloader.classList.add('fade-out');
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 500);
        }
    });
    
    // 14. Mobile Menu Animation
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
    
    // 15. Scroll Progress Indicator
    const scrollProgressBar = document.querySelector('.scroll-progress');
    
    if (scrollProgressBar) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset;
            const docHeight = document.body.offsetHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            
            scrollProgressBar.style.width = scrollPercent + '%';
        });
    }
});

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
