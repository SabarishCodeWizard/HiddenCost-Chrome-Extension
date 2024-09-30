// firebase-auth.js

import { auth, db } from './firebase-init.js'; // Import auth and db from firebase-init
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'https://www.gstatic.com/firebasejs/9.19.1/firebase-auth.js';
import { doc, setDoc, serverTimestamp } from 'https://www.gstatic.com/firebasejs/9.19.1/firebase-firestore.js';

document.addEventListener('DOMContentLoaded', function () {
    // Registration logic
    document.getElementById('register-btn')?.addEventListener('click', async () => {
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        try {
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            await setDoc(doc(db, 'users', userCredential.user.uid), {
                email: userCredential.user.email,
                createdAt: serverTimestamp()
            });
            window.location.href = "popup.html"; // Redirect to popup.html
        } catch (error) {
            document.getElementById('error-message').textContent = error.message; // Show error message
        }
    });

    // Login logic
    document.getElementById('login-btn')?.addEventListener('click', async () => {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        try {
            await signInWithEmailAndPassword(auth, email, password);
            window.location.href = "popup.html"; // Redirect to popup.html
        } catch (error) {
            document.getElementById('error-message').textContent = error.message; // Show error message
        }
    });
});
