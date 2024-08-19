import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller as KeyboardController

class HandMajor:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.hand_result = None

    def get_gesture(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        self.hand_result = results
        gesture_name = "Unknown"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Example: Check the position of thumb and index finger
                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

                if thumb_tip.y < index_tip.y:
                    gesture_name = "Thumb Up"
                else:
                    gesture_name = "Thumb Down"
        
        return gesture_name

class Controller:
    keyboard = KeyboardController()
    prev_hand = None

    @staticmethod
    def handle_controls(gesture_name, hand_result):
        if gesture_name == "Thumb Up":
            Controller.keyboard.press(Key.space)
            Controller.keyboard.release(Key.space)
        elif gesture_name == "Thumb Down":
            Controller.keyboard.press(Key.esc)
            Controller.keyboard.release(Key.esc)
        # Add more gestures and corresponding controls as needed

def main():
    handmajor = HandMajor()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        gesture_name = handmajor.get_gesture(frame)
        Controller.handle_controls(gesture_name, handmajor.hand_result)

        if handmajor.hand_result.multi_hand_landmarks:
            for hand_landmarks in handmajor.hand_result.multi_hand_landmarks:
                handmajor.mp_drawing.draw_landmarks(frame, hand_landmarks, handmajor.mp_hands.HAND_CONNECTIONS)
        else:
            Controller.prev_hand = None

        cv2.putText(frame, gesture_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Gesture Controller', frame)

        if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
