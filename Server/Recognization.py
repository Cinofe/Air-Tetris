import cv2, mediapipe as mp, os

class Recognization:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_style = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
                    model_complexity=0,
                    max_num_hands=1)
        self.landmark = []

    def processing(self, frame):
        self.position = []
        self.landmark = []
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        if results.multi_hand_landmarks:
            self.landmark = results.multi_hand_landmarks
            # self.mp_drawing.draw_landmarks(
            #     frame,
            #     results.multi_hand_landmarks[0],
            #     self.mp_hands.HAND_CONNECTIONS,
            #     self.mp_drawing_style.get_default_hand_landmarks_style(),
            #     self.mp_drawing_style.get_default_hand_connections_style()
            # )
        return frame, self.landmark