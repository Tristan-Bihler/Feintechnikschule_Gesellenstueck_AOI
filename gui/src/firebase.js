import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/storage';


const app = firebase.initializeApp({
    apiKey: "AIzaSyCst7QRNnFR9eC0YpiDYjYuAyjsrDdUtT4",
    authDomain: "tbstudios-aoi.firebaseapp.com",
    projectId: "tbstudios-aoi",
    storageBucket: "tbstudios-aoi.appspot.com",
    messagingSenderId: "875785319966",
    appId: "1:875785319966:web:8211d34038a1ed2d8a600f",
    measurementId: "G-G28PMSQPBE"
  })

  export const auth = app.auth()
  export const storage = app.storage()
  export default app