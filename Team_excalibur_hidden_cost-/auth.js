// auth.js

// Login form
document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  
    auth.signInWithEmailAndPassword(email, password)
      .then((userCredential) => {
        console.log('Logged in:', userCredential.user);
        window.location.href = "popup.html"; // Redirect to popup.html
      })
      .catch((error) => {
        console.error('Error logging in:', error);
        alert("Error logging in: " + error.message);
      });
  });
  
  // Google sign-in
  document.getElementById('google-signin').addEventListener('click', () => {
    const provider = new firebase.auth.GoogleAuthProvider();
  
    auth.signInWithPopup(provider)
      .then((result) => {
        console.log('Google sign-in:', result.user);
        window.location.href = "popup.html"; // Redirect to popup.html
      })
      .catch((error) => {
        console.error('Error during Google sign-in:', error);
        alert("Error during Google sign-in: " + error.message);
      });
  });
  
  // Register form
  document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
  
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }
  
    try {
      // Check if user already exists
      const userDoc = db.collection("users").doc(email);
      const userSnapshot = await userDoc.get();
  
      if (userSnapshot.exists) {
        alert("User already registered. Please log in.");
        return;
      }
  
      // Create user in Firebase Authentication
      const userCredential = await auth.createUserWithEmailAndPassword(email, password);
  
      // Create user document in Firestore
      await userDoc.set({
        email: email,
        uid: userCredential.user.uid,
      });
  
      console.log('Registered:', userCredential.user);
      alert("Registration successful! Redirecting to the main page...");
  
      // Redirect to popup.html after successful registration
      window.location.href = "popup.html";
    } catch (error) {
      console.error('Error registering:', error);
      alert("Error registering: " + error.message);
    }
  });
  