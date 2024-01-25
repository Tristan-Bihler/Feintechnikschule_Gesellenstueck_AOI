import pyrebase
import subprocess

program_name = 'Vergleicher.py'


# Funktion für das einloggen und abfragen der daten, sowie ein scipt auzuführen
def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"User signed in successfully. User ID: {user['localId']}")

        # nach login datenbank abfragen und daten entnemen
        data = db.child("machines").child("lumina_mk1").get()
        print("Data from the 'users' node:")
        print(data)
        for test in data.each(): 
            print(test.val())
            if test.val() == 1:
                try:
                    positioner = r'hardware\\Raspberry_PI\\Camera\\positioning.py'  # Replace with the path to your actual script
                    subprocess.run(["python", positioner])
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")
                try:
                    similarity_script = r'hardware\\Raspberry_PI\\Camera\\Vergleicher.py'
                    subprocess.run(['python', similarity_script], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")
        machine_ref = db.child("machines").child("lumina_mk1")
        machine_ref.update({"status": 0})

    except Exception as e:
        print(f"Login failed. Error: {e}")

if __name__ == "__main__":
    # firebase verküpfungsadaten
    firebase_config = {
                    "apiKey": "AIzaSyCst7QRNnFR9eC0YpiDYjYuAyjsrDdUtT4",
                    "authDomain": "tbstudios-aoi.firebaseapp.com",
                    "databaseURL": "https://tbstudios-aoi-default-rtdb.europe-west1.firebasedatabase.app",
                    "projectId": "tbstudios-aoi",
                    "storageBucket": "tbstudios-aoi.appspot.com",
                    "messagingSenderId": "875785319966",
                    "appId": "1:875785319966:web:8211d34038a1ed2d8a600f",
                    "measurementId": "G-G28PMSQPBE"
                }

    firebase = pyrebase.initialize_app(firebase_config)

    auth = firebase.auth()

    db = firebase.database()
    login_user("tristanbihler@outlook.com", "123456")
