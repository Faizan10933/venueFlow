import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getAnalytics, isSupported } from "firebase/analytics";

// TODO: Replace this with your actual Firebase config from console.firebase.google.com
const firebaseConfig = {
  apiKey: "AIzaSyDiAYeXPGuZkpbyYbd24pa9_zto7z3P8IU",
  authDomain: "mindmate-b7d7a.firebaseapp.com",
  projectId: "mindmate-b7d7a",
  storageBucket: "mindmate-b7d7a.firebasestorage.app",
  messagingSenderId: "631009377883",
  appId: "1:631009377883:web:a256bc360cdd3aedb1897e",
  measurementId: "G-NWE1V0XSJ7"
};

let app, auth, db, analytics, provider;

try {
  app = initializeApp(firebaseConfig);
  auth = getAuth(app);
  db = getFirestore(app);
  provider = new GoogleAuthProvider();
  
  // Only initialize analytics in browser environments that support it
  isSupported().then(yes => yes ? analytics = getAnalytics(app) : null);
} catch (error) {
  console.warn("Firebase initialization failed (missing config). App will still run in fallback mode.");
}

export { auth, db, provider, analytics };
