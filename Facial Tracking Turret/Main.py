import cv2
import numpy as np
import serial
import time

# Initialize serial connection to Arduino
arduino = serial.Serial('COM6', 9600)  # Change port as needed
time.sleep(2)  # Allow connection to establish

# Face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# Camera setup
cap = cv2.VideoCapture(0)  # Use 0 for default camera
screen_width, screen_height = 640, 480  # Match your camera resolution
cap.set(3, screen_width)
cap.set(4, screen_height)

# Servo parameters
servo_x = 90  # Initial X position (degrees)
servo_y = 90  # Initial Y position (degrees)
deadzone = 30  # Pixel tolerance to prevent servo jitter

def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Calculate face center
        face_center_x = x + w//2
        face_center_y = y + h//2
        
        # Calculate position differences
        diff_x = face_center_x - screen_width//2
        diff_y = face_center_y - screen_height//2
        
        # Update servo positions only if outside deadzone
        if abs(diff_x) > deadzone:
            servo_x = map_value(face_center_x, 0, screen_width, 180, 0)
        
        if abs(diff_y) > deadzone:
            servo_y = map_value(face_center_y, 0, screen_height, 180, 0)
        
        # Send coordinates to Arduino
        arduino.write(f"{servo_x},{servo_y}\n".encode())
        
    cv2.imshow('Face Tracking', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()