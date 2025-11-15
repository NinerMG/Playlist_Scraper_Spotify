// Animacja podczas ładowania strony
document.addEventListener('DOMContentLoaded', function() {
    // Dodaj klasy animacji do elementów
    const formCard = document.querySelector('.form-card');
    const features = document.querySelectorAll('.feature-item');
    
    if (formCard) {
        setTimeout(() => {
            formCard.style.opacity = '1';
            formCard.style.transform = 'translateY(0)';
        }, 100);
    }
    
    // Animuj features z opóźnieniem
    features.forEach((feature, index) => {
        setTimeout(() => {
            feature.style.opacity = '1';
            feature.style.transform = 'translateY(0)';
        }, 300 + (index * 100));
    });
});

// Obsługa formularza z animacją ładowania
const form = document.getElementById('playlistForm');
if (form) {
    form.addEventListener('submit', function(e) {
        const button = this.querySelector('.btn-generate');
        const btnText = button.querySelector('.btn-text');
        const btnLoader = button.querySelector('.btn-loader');
        
        // Pokaż loader
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-flex';
        button.disabled = true;
        button.style.cursor = 'not-allowed';
        button.style.opacity = '0.7';
    });
}

// Animacja pól input przy focusie
const inputs = document.querySelectorAll('input[type="date"], input[type="text"]');
inputs.forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
        this.parentElement.style.transition = 'transform 0.2s ease';
    });
    
    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Parallax effect dla background notes
document.addEventListener('mousemove', function(e) {
    const notes = document.querySelectorAll('.music-note');
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    notes.forEach((note, index) => {
        const speed = (index + 1) * 20;
        const x = (mouseX * speed) - (speed / 2);
        const y = (mouseY * speed) - (speed / 2);
        note.style.transform = `translate(${x}px, ${y}px)`;
    });
});

// Dodaj efekt ripple do przycisku
const buttons = document.querySelectorAll('button, .spotify-link');
buttons.forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple-effect');
        
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
});

// Dodaj style dla ripple effect
const style = document.createElement('style');
style.textContent = `
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    button, .spotify-link {
        position: relative;
        overflow: hidden;
    }
`;
document.head.appendChild(style);

// Walidacja daty z animowanym komunikatem
const dateInput = document.getElementById('date');
if (dateInput) {
    dateInput.addEventListener('change', function() {
        const selectedDate = new Date(this.value);
        const minDate = new Date('1958-08-04');
        const maxDate = new Date();
        
        if (selectedDate < minDate || selectedDate > maxDate) {
            this.classList.add('shake');
            setTimeout(() => this.classList.remove('shake'), 500);
        }
    });
}

// Auto-focus na pierwsze pole po załadowaniu
window.addEventListener('load', function() {
    const firstInput = document.querySelector('input[type="date"]');
    if (firstInput) {
        setTimeout(() => firstInput.focus(), 500);
    }
});

// Dodaj efekt hover do feature items
const featureItems = document.querySelectorAll('.feature-item');
featureItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.querySelector('i').style.transform = 'scale(1.2) rotate(10deg)';
        this.querySelector('i').style.transition = 'transform 0.3s ease';
    });
    
    item.addEventListener('mouseleave', function() {
        this.querySelector('i').style.transform = 'scale(1) rotate(0deg)';
    });
});

// Konfetti dla sukcesu (jeśli jest na stronie)
const successIcon = document.querySelector('.success-icon');
if (successIcon) {
    // Trigger confetti animation
    setTimeout(() => {
        createMoreConfetti();
    }, 500);
}

function createMoreConfetti() {
    const container = document.querySelector('.success-card');
    if (!container) return;
    
    for (let i = 0; i < 30; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti-piece';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.animationDelay = Math.random() * 2 + 's';
        confetti.style.background = getRandomColor();
        container.querySelector('.confetti').appendChild(confetti);
    }
}

function getRandomColor() {
    const colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c'];
    return colors[Math.floor(Math.random() * colors.length)];
}
