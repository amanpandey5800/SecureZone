
**_SecureZone: Advanced Threat Detection System_**

SecureZone is a cutting-edge, Convolutional Neural Network (CNN) based model designed to enhance safety in retail environments such as shops and banks. Its primary function is to detect potential threats, like weapons, and automatically respond by sending a recording to designated recipients. This intelligent system not only safeguards assets but also ensures the well-being of personnel and customers.

Features
1. Real-Time Weapon Detection
Utilizing the YOLO (You Only Look Once) object detection model, SecureZone can identify various weapons, such as knives and firearms, within seconds. When a weapon is detected, the system immediately triggers a recording.

2. Automatic Emergency Response
Upon detecting a weapon, the system records the surroundings for a specified duration (default: 6 seconds) and sends the video footage via email to predefined contacts. This feature ensures that relevant parties are informed promptly during critical situations.

3. Pose Detection for Distress Signals
In addition to weapon detection, SecureZone employs MediaPipe Pose technology to monitor the physical posture of individuals. If a shop owner or staff member raises their hands—indicating a possible distress signal—the system will automatically initiate the recording and email alert.

4. User-Friendly Interface
The system leverages the camera feed to display live video along with alerts. Users can easily identify threats and receive immediate notifications on their actions.

How It Works
SecureZone combines several advanced technologies to ensure a robust threat detection mechanism:

1. Initialization
YOLO Model: The YOLO model is initialized with the pre-trained weights from yolov5s.pt (custom paths can be used).
MediaPipe Setup: The MediaPipe library is configured for pose detection, allowing the system to analyze human body landmarks in real-time.
2. Video Capture
The webcam continuously captures video frames, which are processed to detect objects and analyze poses.

3. Object Detection
Each frame is processed by the YOLO model to identify objects. If a detected object matches a predefined weapon class (e.g., knife, pistol), the system triggers a recording.
Detected weapons are highlighted in the video feed with bounding boxes and labels.
4. Pose Analysis
The MediaPipe Pose solution analyzes the video frames to extract keypoints of human figures.
The positions of the left and right wrists are monitored. If both wrists are raised above a certain threshold (indicating a distress signal), the system counts this as a potential threat.
5. Recording and Notification
If a weapon is detected or a distress signal is recognized (e.g., raised hands), the system records the video for a set duration and sends it via email to the specified recipient.
The recorded video is saved, emailed, and subsequently deleted to manage storage efficiently.
Email Configuration
To ensure successful email notifications, the system is set up with SMTP configurations. Users must enter their own email address and app password to facilitate secure communication.

Important Note: When using Gmail, it's recommended to create an App Password for your account, especially if two-factor authentication is enabled.

Usage Example
