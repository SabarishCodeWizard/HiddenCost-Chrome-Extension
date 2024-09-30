// firebase-init.js

// Import necessary functions from Firebase SDK
import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.19.1/firebase-app.js';
import { getAuth } from 'https://www.gstatic.com/firebasejs/9.19.1/firebase-auth.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/9.19.1/firebase-firestore.js';

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCGxYuVK8K5CYQAhbYbHf9VCkSfCdvEQSw",
    authDomain: "mail-dc436.firebaseapp.com",
    projectId: "mail-dc436",
    storageBucket: "mail-dc436.appspot.com",
    messagingSenderId: "34622970017",
    appId: "1:34622970017:web:a92267616e006ae63078e0",
    measurementId: "G-JYG2W6RKBN"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Export the auth and db objects to be used in other files
export { auth, db };
