# Bibliotheken einbinden
import tkinter as tk
from tkinter import messagebox
import pyrebase
import subprocess
import time
import os

def is_connected():
    # Check if there is a network connection by pinging a reliable external host
    try:
        # Use Google's public DNS server for the test
        subprocess.check_call(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

while not is_connected():
    print("No WiFi connection detected. Retrying...")
    time.sleep(5)  # Wait for 5 seconds before retrying
    
print("WiFi connection established!")
# Firebase initialisieren
firebaseConfig = {
    "apiKey": "AIzaSyCst7QRNnFR9eC0YpiDYjYuAyjsrDdUtT4",
    "authDomain": "tbstudios-aoi.firebaseapp.com",
    "databaseURL": "https://tbstudios-aoi-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "tbstudios-aoi",
    "storageBucket": "tbstudios-aoi.appspot.com",
    "messagingSenderId": "875785319966",
    "appId": "1:875785319966:web:8211d34038a1ed2d8a600f"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Anlage starten
def start_action():
    db.child("/machine_mode/mode").set("active")
    db.child("/machine/machine").set("active")

def read_from_firebase(path):
    data = db.child(path).get()
    if data.val():
        return data.val()
    else:
        return "No data available"
    
# SSIM updaten wenn Nutzer den neuen Wert sehen möchte
def update_ssim():
    ssim_value = read_ssim()
    ssim_label.config(text=f"SSIM: {ssim_value}")

    notaus = read_from_firebase("/Not_Aus/Not_Aus")
    door = read_from_firebase("/door/door")

    NOT_AUS_label.config(text=read_from_firebase("/Not_Aus/Not_Aus"))
    TÜR_Label.config(text=read_from_firebase("/door/door"))

    if door == "closed":
        TÜR_Label.config(text=f"Tür: {door}", fg = "green")
    elif door == "open":
        TÜR_Label.config(text=f"Tür: {door}", fg = "red")

    if notaus == "inactive":
        NOT_AUS_label.config(text=f"Not-Aus: {notaus}", fg = "green")
    elif notaus == "active":
        NOT_AUS_label.config(text=f"Not-Aus: {notaus}", fg = "red")

    if read_from_firebase("/machine/machine") == "inactive":
        if ssim_value > 90:
            pass_label.config(text="Test: approved", fg="green")
        elif ssim_value < 90:
            pass_label.config(text="Test: rejected", fg="red")
    
    elif read_from_firebase("/machine/machine") == "active":
        pass_label.config(text="Testing", fg="white")
        ssim_label.config(text=f"N.A.")

# SSIM von Firebase auslesen
def read_ssim():
    try:
        ssim_value = db.child("ssim").get().val()
        ssim_value = round(ssim_value, 2)
        return ssim_value
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read ssim: {e}")
        return None

# Funktion zum kontinuierlichen Aktualisieren der SSIM-Werte
def continuous_update():
    update_ssim()
    root.after(2000, continuous_update)  # Ruft diese Funktion alle 2 Sekunden auf

# Tkinter GUI erstellen mit Auslesen der SSIM
root = tk.Tk()
root.title("Firebase Tkinter App")

root.attributes('-fullscreen', True)
root.configure(bg='gray12')

frame = tk.Frame(root, bg='gray12')
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
label_frame = tk.Frame(frame, bg='gray12')

ssim_value = read_ssim()
if ssim_value is not None:
    ssim_label = tk.Label(label_frame, text=f"SSIM: {ssim_value}", bg='gray12', fg='white', font=("Helvetica", 24))
    ssim_label.pack(pady=20)
else:
    ssim_label = tk.Label(label_frame, text="Failed to load SSIM", bg='gray12', fg='white', font=("Helvetica", 24))
    ssim_label.pack(pady=20)

if ssim_value > 90:
    pass_label = tk.Label(label_frame, text="Passed", bg='gray12', fg='green', font=("Helvetica", 24))
    pass_label.pack(pady=20)
elif ssim_value < 90:
    pass_label = tk.Label(label_frame, text="Not Passed", bg='gray12', fg='red', font=("Helvetica", 24))
    pass_label.pack(pady=20)

NOT_AUS_label = tk.Label(label_frame, bg='gray12', font=("Helvetica", 24))
NOT_AUS_label.pack(pady=20)

TÜR_Label = tk.Label(label_frame, bg='gray12', font=("Helvetica", 24))
TÜR_Label.pack(pady=20)

label_frame.pack(side=tk.RIGHT, padx=75)

button_frame = tk.Frame(frame, bg='gray12')
button_style = {"font": ("Helvetica", 24), "bg": "darkgreen", "fg": "white", "activebackground": "green", "activeforeground": "white", "width": 20, "height": 6}

start_button = tk.Button(button_frame, text="Start", command=start_action, **button_style)
start_button.pack(pady=20, padx=20)

button_frame.pack(side=tk.RIGHT)

root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Starte das kontinuierliche Aktualisieren
continuous_update()

root.mainloop()
