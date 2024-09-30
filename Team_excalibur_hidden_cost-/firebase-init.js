// firebase-init.js

// Load Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.13.2/firebase-auth.js";

// Your Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDdg-IirFVbsG9lwbHStq8chVAy_0U1o80",
  authDomain: "extension-b7927.firebaseapp.com",
  projectId: "extension-b7927",
  storageBucket: "extension-b7927.appspot.com",
  messagingSenderId: "999223446706",
  appId: "1:999223446706:web:a1632d9584626092d20dab",
  measurementId: "G-THKTDMPQ8E"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore and Auth
const db = getFirestore(app);
const auth = getAuth(app);
