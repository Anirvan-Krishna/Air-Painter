import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode = self.mode, max_num_hands = self.max_hands,
                                         min_detection_confidence=self.detection_confidence,
                                        min_tracking_confidence=self.tracking_confidence)

        self.mp_draw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return img

    def find_positions(self, img, hand_num=0, draw=True):
        self.lmList = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_num]

            for id, landmark in enumerate(hand.landmark):
                
                h, w, c = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                self.lmList.append((id, cx, cy))

                if draw:
                    if id == 0:
                        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return self.lmList
    

    def fingers_up(self):
        
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(0)
        else:
            fingers.append(1)
    
        # Fingers
        for id in range(1, 5):
            
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
    
            # totalFingers = fingers.count(1)
    
        return fingers


def main():
    p_time = 0
    c_time = 0
    cap = cv2.VideoCapture(0)  # Use the correct camera index if 0 doesn't work
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        positions = detector.find_positions(img)

        if positions:
            print(positions[4])

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
