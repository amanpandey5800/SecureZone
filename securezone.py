import cv2
import numpy as np
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import torch
from ultralytics import YOLO
import mediapipe as mp

yolo_model = YOLO('yolov5s.pt')

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

EMAIL_ADDRESS = 'enter the mail address from which u wanna sent file'
EMAIL_PASSWORD = 'generate app password from manage my account'
RECIPIENT_ADDRESS = 'enter the mail address where u wanna sent the file'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_email_with_attachment(filename):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_ADDRESS
    msg['Subject'] = 'Recorded Video - Weapon or Distress Detected'
    
    body = 'An alert has been triggered. Please find the recorded video attached.'
    msg.attach(MIMEText(body, 'plain'))
    
    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
        msg.attach(part)
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print(f"Email sent with attachment: {filename}")

def record_and_send(duration=6):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = f"alert_record_{int(time.time())}.avi"
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
    
    t_end = time.time() + duration
    while time.time() < t_end:
        success, image = cap.read()
        if not success:
            print("Failed to read from camera.")
            break
        out.write(image)
        cv2.putText(image, "Recording...", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Recording', image)
        cv2.waitKey(1)
    
    out.release()
    print(f"Recording saved as {filename}")
    
    send_email_with_attachment(filename)
    os.remove(filename)

frame_counter = 0
prev_frame_time = 0

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        yolo_results = yolo_model(image)
        weapon_detected = False

        for result in yolo_results:
            for box in result.boxes:
                label = result.names[int(box.cls)]
                print(f"Detected: {label}")
                if label in ['knife', 'pistol']:
                    weapon_detected = True
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if weapon_detected:
            print("Weapon detected! Starting recording...")
            record_and_send(duration=6)
            break

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
