# Hand Gesture Recognition and Drawing Application

This Python project demonstrates hand gesture recognition and a simple drawing application using OpenCV and the MediaPipe library. The application allows users to draw on the screen by tracking hand movements and recognizing specific gestures.

## Features

### Hand Gesture Recognition

- Detects hand landmarks in real-time.
- Identifies the positions of fingers for gesture recognition.
- Recognizes specific hand gestures to switch between different drawing modes.

### Drawing Application

- Enables users to draw on the screen using different colors and eraser functionalities.
- Offers a variety of color options available through hand gesture recognition.
- Allows switching between drawing and selection modes using hand gestures.

## Code Overview

### `handTrackingModule.py`

Contains a Python module (`handTrackingModule`) that defines a `HandDetector` class for hand tracking and gesture recognition. The class uses the MediaPipe library for detecting hand landmarks, identifying finger positions, and recognizing gestures.

### `main.py`

The `main.py` script integrates the `HandDetector` class to create a real-time drawing application. It utilizes the OpenCV library to capture video from the webcam, track hand movements, and enable drawing functionalities based on recognized gestures.

## Getting Started

### Prerequisites

- Python 3.x
- OpenCV (`cv2`) library
- MediaPipe (`mediapipe`) library

### Running the Application

1. Install the required dependencies using `pip install opencv-python mediapipe`.
2. Run the `main.py` script to start the application.

## How to Use

1. Launch the application by running `main.py`.
2. Place your hand in front of the webcam to start detecting hand gestures.
3. Use specific hand gestures to switch between drawing modes and colors.
4. For Drawing, stretch your palm with index finger open and all others closed, for switching between colors, open index and middle finger
5. Draw on the screen by moving your hand while in drawing mode.
6. Press 'q' to exit the application.

## Credits

This project was created using the `OpenCV` and `MediaPipe` libraries.
