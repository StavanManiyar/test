// Enhanced JavaScript for Animations and Modern Features

// Wait for the DOM content to load
window.addEventListener('DOMContentLoaded', function() {
  // Initialize page transitions
  document.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href && href.indexOf('#') !== 0) {
        e.preventDefault();
        document.querySelector('.page-transition').classList.add('active');
        setTimeout(function() {
          window.location.href = href;
        }, 500);
      }
    });
  });

  // Scroll animations
  const scrollElements = document.querySelectorAll('.scroll-fade-in, .scroll-slide-left, .scroll-slide-right');
  const elementInView = (el, dividend = 1) => {
    const elementTop = el.getBoundingClientRect().top;
    return (
      elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
    );
  };
  const displayScrollElement = (element) => {
    element.classList.add('active');
  };
  const hideScrollElement = (element) => {
    element.classList.remove('active');
  };
  const handleScrollAnimation = () => {
    scrollElements.forEach((el) => {
      if (elementInView(el, 1.25)) {
        displayScrollElement(el);
      } else {
        hideScrollElement(el);
      }
    });
  };
  window.addEventListener('scroll', () => {
    handleScrollAnimation();
  });

  // Loading spinner for data retrieval
  function showLoadingSpinner() {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    document.body.appendChild(spinner);
  }

  function removeLoadingSpinner() {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) {
      spinner.remove();
    }
  }

  // Example usage: Add to button click to simulate loading
  const loadButton = document.querySelector('.load-button');
  if (loadButton) {
    loadButton.addEventListener('click', function() {
      showLoadingSpinner();
      setTimeout(removeLoadingSpinner, 3000); // Simulate 3s loading
    });
  }

  // Initialize counters
  const counters = document.querySelectorAll('.counter');
  counters.forEach(counter => {
    counter.innerText = '0';
    const updateCounter = () => {
      const target = +counter.getAttribute('data-target');
      const c = +counter.innerText;
      const increment = target / 200;
      if (c < target) {
        counter.innerText = `${Math.ceil(c + increment)}`;
        setTimeout(updateCounter, 1);
      } else {
        counter.innerText = target;
      }
    };
    updateCounter();
  });
});
