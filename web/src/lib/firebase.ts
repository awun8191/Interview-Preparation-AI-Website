import { initializeApp, type FirebaseApp } from "firebase/app";

/**
 * Firebase web configuration for the theplan-9311e project.
 *
 * This is client-side config, not a secret. Firebase web API keys are
 * identifiers designed to ship in the browser bundle; access is controlled by
 * Security Rules and by server-side ID token verification, not by hiding them.
 */
export const firebaseConfig = {
  apiKey: "AIzaSyBmKFq0rF9ncymkBJjQNSxtRhAaD_st6K0",
  authDomain: "theplan-9311e.firebaseapp.com",
  projectId: "theplan-9311e",
  storageBucket: "theplan-9311e.firebasestorage.app",
  messagingSenderId: "480187173082",
  appId: "1:480187173082:web:9345ff93fdcc82256cbde3",
  measurementId: "G-ENLJCHV7T7",
};

export const firebaseApp: FirebaseApp = initializeApp(firebaseConfig);
