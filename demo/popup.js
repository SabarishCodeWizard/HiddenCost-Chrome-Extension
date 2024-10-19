// Firebase Configuration
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

// Sign in with Google using Chrome Identity API
document.getElementById('login').addEventListener('click', () => {
  chrome.identity.getAuthToken({ interactive: true }, function(token) {
    if (chrome.runtime.lastError) {
      console.error(chrome.runtime.lastError);
      return;
    }
    
    // Use the token to authenticate with your Firebase project
    const credential = firebase.auth.GoogleAuthProvider.credential(null, token);
    
    // Sign in with Firebase using the credential
    firebase.auth().signInWithCredential(credential)
      .then((result) => {
        console.log('User signed in: ', result.user);
        // Redirect to home page
        chrome.tabs.create({ url: "home.html" });
      })
      .catch((error) => {
        console.error('Error during sign-in:', error);
      });
  });
});

