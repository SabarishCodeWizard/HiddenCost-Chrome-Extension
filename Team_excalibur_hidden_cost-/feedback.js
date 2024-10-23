document.getElementById('feedbackForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    const formData = new FormData(this);

    try {
        const response = await fetch('https://formspree.io/f/xrbgbyek', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: formData
        });

        if (response.ok) {
            // Show thank you animation
            displayThankYouAnimation();

            // Redirect to popup.html after 3 seconds (adjust as needed)
            setTimeout(() => {
                window.location.href = "popup.html";
            }, 3000);
        } else {
            alert('Something went wrong. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error submitting feedback.');
    }
});

function displayThankYouAnimation() {
    // Create an animation element
    const thankYouMessage = document.createElement('div');
    thankYouMessage.textContent = 'Thank you for your feedback!';
    thankYouMessage.classList.add('thank-you-message');

    // Create a thumbs-up icon element
    const thumbsUpIcon = document.createElement('div');
    thumbsUpIcon.classList.add('thumbs-up-icon');
    thumbsUpIcon.innerHTML = '<img src="anime-girl.gif" alt="Thumbs Up" />'; // Use the GIF as an icon

    // Style the animation elements
    thankYouMessage.style.position = 'fixed';
    thankYouMessage.style.top = '50%';
    thankYouMessage.style.left = '50%';
    thankYouMessage.style.transform = 'translate(-50%, -50%) scale(0.8)';
    thankYouMessage.style.background = 'linear-gradient(90deg, #00DBDE 0%, #FC00FF 100%)'; // Gradient background
    thankYouMessage.style.padding = '20px';
    thankYouMessage.style.fontSize = '24px';
    thankYouMessage.style.color = '#002b9d';
    thankYouMessage.style.borderRadius = '12px';
    thankYouMessage.style.textAlign = 'center';
    thankYouMessage.style.zIndex = '1000';
    thankYouMessage.style.opacity = '0'; // Start with opacity 0
    thankYouMessage.style.transition = 'opacity 0.8s ease, transform 0.8s ease'; // Set transition for the message

    // Style the thumbs-up icon
    thumbsUpIcon.style.display = 'block'; // Center the icon above the text
    thumbsUpIcon.style.margin = '0 auto'; // Center the icon

    // Add the icon and message to the thank-you message element
    thankYouMessage.appendChild(thumbsUpIcon);
    document.body.appendChild(thankYouMessage);

    // Trigger the animation (fade-in and scale-up)
    setTimeout(() => {
        thankYouMessage.style.opacity = '1';
        thankYouMessage.style.transform = 'translate(-50%, -50%) scale(1)';
    }, 100);

    // Fade-out after 2 seconds
    setTimeout(() => {
        thankYouMessage.style.opacity = '0';
        thankYouMessage.style.transform = 'translate(-50%, -50%) scale(0.9)';
    }, 2000);

    // Remove the element after the animation completes
    setTimeout(() => {
        document.body.removeChild(thankYouMessage);
    }, 2800); // 800ms for fade-out + 2000ms for initial display
}

