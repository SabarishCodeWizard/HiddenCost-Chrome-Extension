// Import Firebase functions
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.1/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.13.1/firebase-auth.js";

// Firebase config
const firebaseConfig = {
    apiKey: "AIzaSyBpdNsnBdInQv3mVsMvzr_PwDCOzRb3cw8",
    authDomain: "extension-e7604.firebaseapp.com",
    projectId: "extension-e7604",
    storageBucket: "extension-e7604.appspot.com",
    messagingSenderId: "321576555908",
    appId: "1:321576555908:web:50526dece986898aaef9d1",
    measurementId: "G-K0982J26ZY"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();

// Google Login
const provider = new GoogleAuthProvider();

document.getElementById('googleLogin').addEventListener('click', () => {
    signInWithPopup(auth, provider)
        .then((result) => {
            // Successful login
            window.location.href = 'popup.html'; // Redirect to popup.html
        })
        .catch((error) => {
            console.error('Login failed', error);
        });
});

// Check if user is already logged in
onAuthStateChanged(auth, (user) => {
    if (user) {
        window.location.href = 'popup.html'; // Redirect to home page if already logged in
    }
});
