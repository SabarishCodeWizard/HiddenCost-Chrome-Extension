// firebase-init.js

// Initialize Firebase
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
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();
