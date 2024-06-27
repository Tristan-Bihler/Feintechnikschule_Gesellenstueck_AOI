#Bibliotheken einbinden
import cv2
from picamera2 import Picamera2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import time
import pyrebase
import smbus
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

#Firebase configurieren und initialisieren
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
storage = firebase.storage()

#Kamera configurieren und initialisieren
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

#Funktion für das aufnehemen eines Bildes
def capture_image(picam2):
    frame = picam2.capture_array()
    if frame is None:
        raise Exception("Failed to capture image")
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

#Funktion für das Vergleichen von den Bildern
def compare_images(image1, image2, threshold=30):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)#SSIM Funktioniert nur mit Farblosen Bildern daher müssen die farblos gemacht werden
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    abs_diff = cv2.absdiff(gray1, gray2)
    
    _, thresh_diff = cv2.threshold(abs_diff, threshold, 255, cv2.THRESH_BINARY)
    
    mask = thresh_diff.astype(bool)
    
    if np.sum(mask) > 0:  
        ssim_score, _ = ssim(gray1[mask], gray2[mask], full=True)
    else:
        ssim_score = 1.0

    score, diff = ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")
    
    return ssim_score, diff, thresh_diff

#Firebase variablen auslesen
def read_from_firebase(path):
    data = db.child(path).get()
    if data.val():
        return data.val()
    else:
        return "No data available"

#Wenn der Modus activ ist und die Kamera über die Platine ist ein Bild aufnehmen und verleichen
def machine_active(picam2):
    while True:
        frame = picam2.capture_array()
        if frame is not None:
            time.sleep(3)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            image2 = capture_image(picam2)
            cv2.imwrite("taken.jpg", image2)
            break
    
    comp_picture = cv2.imread("comoparrasion.jpg")
    ssim_score, diff, thresh_diff = compare_images(image2, comp_picture)
    cv2.imwrite("compared_image.jpg", thresh_diff)
    db.child("/ssim").set((ssim_score*100))
    cv2.destroyAllWindows()
    print(ssim_score)

#Bild hochladen
def upload_image(image_path, storage_path):
    """Uploads an image to Firebase Storage."""
    storage.child(storage_path).put(image_path)
    url = storage.child(storage_path).get_url(None)
    print(f'File {image_path} uploaded to {storage_path}.')
    print(f'Public URL: {url}')

#Wenn der Modus activ ist und die Kamera über die Platine ist ein Bild aufnehmen für das spätere vergleichen
def machine_scan(picam2):

    while True:
        frame = picam2.capture_array()
        if frame is not None:
            time.sleep(3)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            image1 = capture_image(picam2)
            cv2.imwrite("comoparrasion.jpg", image1)
            break
    cv2.destroyAllWindows()
        
#Arduino auslesen und zurückschreiben
def write(address, data):
    bus = smbus.SMBus(1)
    
    try:
        bus.write_byte(address, data)
        time.sleep(0.2)
        return None
    except Exception as e:
        print(f"Failed to communicate with Arduino: {e}")
        return None

def read(address):
    bus = smbus.SMBus(1)
    try:
        response = bus.read_byte(address)
        return response
    except:
        print(f"Failed to communicate with Arduino: {e}")
        return 0
#Schrittkettenartige Programmierung um die Kamera schrittartig auf die Poition zu fahren und he nach modus das Bild zu vergleichen oder für das spätere verhgleichen aufzunehmen
def main():
    if read_from_firebase("/machine/machine") == "active": #Wenn die Anlage an ist
        write(0x08, 110)
        data = read(0x08)
        print(data)
        if data == 10:
            write(0x08, int(read_from_firebase("/x/x")))
            while data != 20:
                data = read(0x08)#X Werte übermitteln
                print("x")
                print(data)
                if data == 90 or read_from_firebase("/machine/machine") == "inactive":# Wenn entweder der Arduino oder Firebase sagt das ein Problem auftritt oder die Anlage nicht mehr laufen soll
                    print("power off")
                    return 0
            if data == 20:
                write(0x08, int(read_from_firebase("/y/y")))
                while data != 30:
                    data = read(0x08)#Y Werte übermitteln
                    print("y")
                    print(data)
                    if data == 90 or read_from_firebase("/machine/machine") == "inactive":
                        print("power off")
                        db.child("/machine/machine").set("inactive")
                        return 0
                if data == 30:
                    write(0x08, 120)
                    while data != 40:
                        data = read(0x08)#Bestätigen das die Verbindung noch aufrecht ist und der Arduino die Leds anschalten soll
                        print("passed")
                        print(data)
                        if data == 90 or read_from_firebase("/machine/machine") == "inactive":
                            print("power off")
                            return 0
                    if data == 40:
                        write(0x08, 130)#Bestägitgen das die LEDs an sind und je nach Modus das Bild aufzunehemen
                        while data != 50:
                            data = read(0x08)
                            print("passed")
                            print(data)
                            if data == 90 or read_from_firebase("/machine/machine") == "inactive":
                                print("power off")
                                return 0
                        if data == 50:
                            print("picture")
                            if read_from_firebase("/machine_mode/mode") == "active": # Wenn der Modus auf vergleichen gestellt ist
                                machine_active(picam2)
                                upload_image('compared_image.jpg', 'images/compared.jpg')
                                upload_image('taken.jpg', 'images/taken.jpg')
                                data = write(0x08, 140)
                                while data != 60:
                                    data = read(0x08)# Arduino bescheid geben auf Home zu fahren und die Neopixels auszuschalten
                                    print("finish")
                                    print(data)
                                    if data == 90 or read_from_firebase("/machine/machine") == "inactive":
                                        print("power off")
                                        return 0
                                if data == 60:# Programm ist zuende und der Arduino ist auf Home
                                    db.child("/machine/machine").set("inactive")#Anlage auf inaktiv schalten
                                    data = 0
                                    return 0
                
                            elif read_from_firebase("/machine_mode/mode") == "scan": # Wenn der Modus auf Bild aufnehmen für das spätere Vergleichen gestellt ist
                                machine_scan(picam2)
                                upload_image('comoparrasion.jpg', 'images/comoparrasion.jpg')
                                data = write(0x08, 140)
                                while data != 60:
                                    data = read(0x08)# Arduino bescheid geben auf Home zu fahren und die Neopixels auszuschalten
                                    print("finish")
                                    print(data)
                                    if data == 90 or read_from_firebase("/machine/machine") == "inactive":
                                        print("power off")
                                        db.child("/machine/machine").set("inactive")
                                        return 0
                                if data == 60:# Programm ist zuende und der Arduino ist auf Home
                                    db.child("/machine/machine").set("inactive")#Anlage auf inaktiv schalten
                                    data = 0
                                    return 0
        else:
            print(data)
    elif read_from_firebase("/machine/machine") == "inactive":
        return 0

while 1:
    main()
        
