// Ensure Firebase auth is initialized from the global firebase object
const auth = firebase.auth();

// Login form
document.getElementById('login-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  auth.signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // Successfully logged in
      console.log('Logged in:', userCredential.user);
    })
    .catch((error) => {
      console.error('Error logging in:', error);
    });
});

// Google sign-in
document.getElementById('google-signin').addEventListener('click', () => {
  const provider = new firebase.auth.GoogleAuthProvider();

  auth.signInWithPopup(provider)
    .then((result) => {
      // Google sign-in successful
      console.log('Google sign-in:', result.user);
    })
    .catch((error) => {
      console.error('Error during Google sign-in:', error);
    });
});
