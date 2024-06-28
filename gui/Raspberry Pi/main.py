# Bibliotheken einbinden
from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO
import board
import neopixel
from pyrebase import pyrebase

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

# Outputs und Inputs definieren
pixels = neopixel.NeoPixel(board.D21, 5)
INPUT_PIN1 = 18
INPUT_PIN2 = 23
OUTPUT_PIN = 9

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN1, GPIO.IN)
GPIO.setup(INPUT_PIN2, GPIO.IN)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

# Firebase initialisieren
firebase_config = {
    "apiKey": "AIzaSyCst7QRNnFR9eC0YpiDYjYuAyjsrDdUtT4",
    "authDomain": "tbstudios-aoi.firebaseapp.com",
    "databaseURL": "https://tbstudios-aoi-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "tbstudios-aoi.appspot.com"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Funktion zum lesen und schreiben der Variablen zu Firebase
def upload_variable(path, data):
	try:
		db.child(path).set(data)
		print(f"Data uploaded to {path}: {data}")
	except Exception as e:
		print(f"Failed to upload data: {e}")
	
def read_variable(path):
	try:
		data = db.child(path).get().val()
		print(f"Data read from {path}: {data}")
		return data
	except Exception as e:
		print(f"Failed to read data: {e}")
		return None

def main():
	try:
		while True:
			data = read_variable("/machine/machine")
			input_state1 = GPIO.input(INPUT_PIN1)
			input_state2 = GPIO.input(INPUT_PIN2)

			if input_state1 == GPIO.HIGH: # Wenn Not Aus gedrück Akkustisches und Optisches Signal 								senden, zudem den Zustand hochladen
				pixels.fill((100, 0, 0))  
				GPIO.output(OUTPUT_PIN, GPIO.HIGH)
				print("ON")
				upload_variable("/machine", {"machine": "inactive"})
				upload_variable("/Not_Aus", {"Not_Aus": "active"})
			
			elif input_state2 == GPIO.HIGH:# Wenn Tür offen Optisches Signal 										senden, zudem den Zustand hochladen.
				pixels.fill((100, 0, 0)) 
				GPIO.output(OUTPUT_PIN, GPIO.LOW) 
				print("ON")
				upload_variable("/machine", {"machine": "inactive"})
				upload_variable("/door", {"door": "open"})
				
				
			elif data == "active":	# Wenn Firebase sagt das die Mashine an ist. Optisches Signal Grün 						melden.
				pixels.fill((0, 100, 0))
				GPIO.output(OUTPUT_PIN, GPIO.LOW)
				time.sleep(0.1)
				upload_variable("/door", {"door": "closed"})
				upload_variable("/Not_Aus", {"Not_Aus": "inactive"})
				
			else: # Anlage auf Inaktiv schalten. Optisches Signal auf Gelb stellen.
				pixels.fill((100, 100, 0))
				GPIO.output(OUTPUT_PIN, GPIO.LOW)
				upload_variable("/Not_Aus", {"Not_Aus": "inactive"})
				upload_variable("/door", {"door": "closed"})
				upload_variable("/Not_Aus", {"Not_Aus": "inactive"})

	except KeyboardInterrupt:
		pass

	finally:
		# Wenn ein error ensteht alles zurückstellen.
		GPIO.cleanup()
		pixels.fill((0, 0, 0))

if __name__ == '__main__':
	main()
