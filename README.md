
# AI Hands-Free Control System



The **AI Hands-Free Control System** is a computer vision–based project that enables users to control their computer using hand gestures detected through a webcam. The system uses **MediaPipe** for real-time hand tracking and **OpenCV** for video processing to detect hand landmarks and interpret gestures.

By using simple hand gestures, users can perform common computer actions such as moving the cursor, clicking, scrolling, and adjusting system volume without using a physical mouse or keyboard. The gestures are captured through the webcam and translated into system commands using **PyAutoGUI**.

This project demonstrates the practical use of **Artificial Intelligence, Computer Vision, and Human-Computer Interaction (HCI)** to create a touchless interface. It can be useful for accessibility solutions, smart interfaces, and interactive computing systems.

---

## Features

* Control mouse cursor using hand gestures
* Click using a finger pinch gesture
* Scroll up and down using index finger movement
* Adjust system volume using thumb direction
* Real-time hand tracking using MediaPipe
* Smooth cursor movement with gesture recognition

---

## Gesture Controls

| Gesture                 | Action          |
| ----------------------- | --------------- |
| ✌ Index + Middle Finger | Move Cursor     |
| 🤏 Thumb + Index Finger | Mouse Click     |
| ☝ Index Finger Only     | Scroll Page     |
| 👍 Thumb Up             | Increase Volume |
| 👎 Thumb Down           | Decrease Volume |

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* NumPy

---

## Project Structure

```
AI-Hands-Free-Control-System
│
├── main.py
├── hand_tracker.py
└── README.md
```

---

## Installation

1. Clone the repository

```
https://github.com/Priyanka17-08/Hand-Gesture.git
```

2. Navigate to the project folder

```
cd Hand-Gesture
```

3. Install required libraries

```
pip install -r requirements.txt
```

Or install manually:

```
pip install opencv-python mediapipe pyautogui numpy
```

---

## How to Run the Project

Run the following command:

```
py -3.11 main.py
```

Make sure your **webcam is enabled**.

Press **Q** to exit the program.

---

## Demo


---

## Applications

* Touchless computer control
* Gesture-based interaction systems
* Human-computer interaction research

---

## Future Improvements

* Add gesture recognition for opening applications
* Add on-screen gesture indicators
* Improve gesture detection accuracy
* Implement machine learning-based gesture classification
* Add multi-hand gesture support

---

## Author

Priyanka

---

## License

This project is open-source and available under the MIT License.
