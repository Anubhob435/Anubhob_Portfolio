//NAVIGATION BAR EFFECTS ON SCROLL
window.addEventListener("scroll", function() {
    const header = document.querySelector("header");
    header.classList.toggle("sticky", window.scrollY > 0);
});

//DARK THEME TOGGLE
var icon = document.getElementById("icon");
var logo = document.getElementsByClassName("logo")[0];
var image = document.getElementById("image");

icon.onclick = function() {
    document.body.classList.toggle("dark-theme");

    if (document.body.classList.contains("dark-theme")) {
        icon.src = "/static/images/sun.png"; // Change to sun icon in dark mode
        logo.src = "/static/images/logo-light.png"; // Use dark mode logo
        // Don't change the profile picture source
    } else {
        icon.src = "/static/images/moon.png"; // Change to moon icon in light mode
        logo.src = "/static/images/logo-light.png"; // Use light mode logo
        // Don't change the profile picture source
    }
}

//PROJECTS SECTION MODAL
const projectModals = document.querySelectorAll(".project-model");
const imgCards = document.querySelectorAll(".img-card");
const projectcloseBtns = document.querySelectorAll(".project-close-btn");

var projectModal = function(modalclick) {
    projectModals[modalclick].classList.add("active");
}

imgCards.forEach((imgCard, index) => {
    imgCard.addEventListener("click", () => {
        projectModal(index);
    });
});

projectcloseBtns.forEach((closeBtn) => {
    closeBtn.addEventListener("click", (event) => {
        event.stopPropagation();
        projectModals.forEach((projectModalView) => {
            projectModalView.classList.remove("active");
        });
    });
});

//SCROLL REVEAL ANIMATION 
//COMMON REVEAL OPTIONS TO CREATE REVEAL ANIMATIONS
ScrollReveal({
    reset: true,
    distance: '60px',
    duration: 2500,
    delay: 100
});

ScrollReveal().reveal('.home .info h2, .section-title-01, .section-title-02', {
    delay: 500,
    origin: 'left'
});
ScrollReveal().reveal('.home .info h3, .home .info p, .about-info .btn', {
    delay: 600,
    origin: 'right'
});
ScrollReveal().reveal('.home .info .btn', {
    delay: 700,
    origin: 'bottom'
});
ScrollReveal().reveal('.media-icons i, .contact-left li', {
    delay: 500,
    origin: 'left',
    interval: 200
});
ScrollReveal().reveal('.home-img, .about-img', {
    delay: 500,
    origin: 'bottom'
});
ScrollReveal().reveal('.about .description, .contact-right', {
    delay: 600,
    origin: 'right'
});
ScrollReveal().reveal('.about .professional-list li', {
    delay: 500,
    origin: 'right',
    interval: 200
});
ScrollReveal().reveal('.skills-description, .contact-card, .contact-left h2', {
    delay: 700,
    origin: 'left'
});
ScrollReveal().reveal('.education, .projects .img-card', {
    delay: 800,
    origin: 'bottom',
    interval: 200
});
ScrollReveal().reveal('.footer-container .group', {
    delay: 500,
    origin: 'top'
});

//RESPONSIVE NAVIGATION BAR
const menuBtn = document.querySelector(".nav-menu-btn");
const closeBtn = document.querySelector(".nav-close-btn");
const navMenu = document.querySelector(".navigation");
const navItems = document.querySelectorAll(".nav-items a");

menuBtn.addEventListener("click", () => {
    navMenu.classList.add("active");
});

closeBtn.addEventListener("click", () => {
    navMenu.classList.remove("active");
});

navItems.forEach((navItem) => {
    navItem.addEventListener("click", () => {
        navMenu.classList.remove("active");
    });
});

//CHATBOT FUNCTIONALITY
document.addEventListener("DOMContentLoaded", function() {
    // Set initial theme state
    icon.src = "/static/images/sun.png"; // Start with sun icon
    logo.src = "/static/images/logo-light.png"; // Use dark mode logo

    const chatbotMessages = document.getElementById("chatbot-messages");
    const chatbotInput = document.getElementById("chatbot-input");
    const chatbotSendBtn = document.getElementById("chatbot-send-btn");
    const chatbotMinimizeBtn = document.getElementById("chatbot-minimize-btn");
    const chatbotReopenBtn = document.getElementById("chatbot-reopen-btn");

    // Function to display a message
    function displayMessage(message, className) {
        const messageElement = document.createElement("div");
        messageElement.className = `chatbot-message ${className}`;
        messageElement.textContent = message;
        chatbotMessages.appendChild(messageElement);
    }

    // Function to handle sending a message
    async function handleSendMessage() {
        const userMessage = chatbotInput.value;
        if (userMessage.trim() === "") return;

        // Display user message
        displayMessage(userMessage, "user-message");

        // Clear input
        chatbotInput.value = "";

        // Send message to backend
        const response = await fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });
        const data = await response.json();
        const botMessage = data.response;

        // Display bot message
        displayMessage(botMessage, "bot-message");
    }

    // Event listeners
    chatbotSendBtn.addEventListener("click", handleSendMessage);
    chatbotInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            handleSendMessage();
        }
    });
    chatbotMinimizeBtn.addEventListener("click", function() {
        document.getElementById("chatbot").style.display = "none";
        chatbotReopenBtn.style.display = "block";
    });
    chatbotReopenBtn.addEventListener("click", function() {
        document.getElementById("chatbot").style.display = "flex";
        chatbotReopenBtn.style.display = "none";
    });

    // Add window resize handler
    function handleResize() {
        if (window.innerWidth <= 768) { // Adjust breakpoint as needed
            document.getElementById("chatbot").style.display = "none";
            document.getElementById("chatbot-reopen-btn").style.display = "block";
        }
    }

    // Listen for window resize
    window.addEventListener('resize', handleResize);

    // Check initial window size
    handleResize();

    // Greet the user on page load
    displayMessage("Hola, I am master Dey's Assistant, How can I help", "bot-message");
});