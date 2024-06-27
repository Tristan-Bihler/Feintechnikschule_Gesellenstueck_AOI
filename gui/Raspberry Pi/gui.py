# Bibliotheken einbinden
import tkinter as tk
from tkinter import messagebox
import pyrebase

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

#SSIM updaten wenn nutzer den neuen wert sehen möchte
def update_ssim():
    ssim_value = read_ssim()
    ssim_label.config(text=f"SSIM: {ssim_value}")

    if ssim_value > 90:
        pass_label.config(text ="Passed", fg = "green")
    elif ssim_value < 90:
        pass_label.config(text = "Not Passed", fg = "red")

# Ssim von Firebase auslesen
def read_ssim():
    try:
        ssim_value = db.child("ssim").get().val()
        ssim_value = round(ssim_value, 2)
        return ssim_value
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read ssim: {e}")
        return None

# Tkinter Gui erstellen mit auslesen der Ssim
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
    pass_label = tk.Label(label_frame, text=f"Passed", bg='gray12', fg='green', font=("Helvetica", 24))
    pass_label.pack(pady=20)
elif ssim_value < 90:
    pass_label = tk.Label(label_frame, text="Not Passed", bg='gray12', fg='red', font=("Helvetica", 24))
    pass_label.pack(pady=20)

label_frame.pack(side=tk.RIGHT)


button_frame = tk.Frame(frame, bg='gray12')
button_style = {"font": ("Helvetica", 24), "bg": "darkgreen", "fg": "white", "activebackground": "green", "activeforeground": "white"}

start_button = tk.Button(button_frame, text="Start", command=start_action, **button_style)
start_button.pack(pady=20)

update_button = tk.Button(button_frame, text="Update", command=update_ssim, **button_style)
update_button.pack(pady=20)

button_frame.pack(side=tk.RIGHT)

root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

root.mainloop()

