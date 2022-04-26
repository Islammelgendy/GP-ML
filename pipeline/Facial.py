import numpy as np
import math
import cv2

class Facial:

    def get_landmarks(self, detector, predictor, img):
        self.gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
        self.faces = detector(self.gray)
        if(len(self.faces) == 0):
            return None
        for self.face in self.faces:
            self.landmarks = predictor(image=self.gray, box=self.face)
        return self.landmarks


    def get_euclidean_distance(x, y):
        return math.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)

    def get_yaw_angle(self, landmarks):
        self.left_line = self.get_euclidean_distance([landmarks.part(21).x, landmarks.part(17).x], [landmarks.part(21).y, landmarks.part(17).y])
        self.right_line = self.get_euclidean_distance([landmarks.part(26).x, landmarks.part(22).x], [landmarks.part(26).y, landmarks.part(22).y])
        return math.asin(1 - min(self.left_line, self.right_line) / max(self.left_line, self.right_line)) * (-1 if self.right_line < self.left_line else 1)

    def get_pitch_angle(self, landmarks):
        self.left_line = self.get_euclidean_distance([landmarks.part(29).x, landmarks.part(1).x], [landmarks.part(29).y, landmarks.part(1).y])
        self.right_line = self.get_euclidean_distance([landmarks.part(29).x, landmarks.part(15).x], [landmarks.part(29).y, landmarks.part(15).y])
        self.vertical_distance = np.cross([landmarks.part(15).x - landmarks.part(1).x, landmarks.part(15).y - landmarks.part(1).y], [landmarks.part(29).x - landmarks.part(1).x, landmarks.part(29).y - landmarks.part(1).y]) / np.linalg.norm([landmarks.part(15).x - landmarks.part(1).x, landmarks.part(15).y - landmarks.part(1).y])
        return (math.asin(self.vertical_distance / self.left_line) + math.asin(self.vertical_distance / self.right_line)) / 2

    def get_roll_angle(self, landmarks):
        self.real_line = self.get_euclidean_distance([landmarks.part(15).x, landmarks.part(1).x], [landmarks.part(15).y, landmarks.part(1).y])
        self.virtual_line = self.get_euclidean_distance([landmarks.part(15).x, landmarks.part(1).x], [landmarks.part(1).y, landmarks.part(1).y])
        return math.acos(self.virtual_line / self.real_line) * (-1 if(landmarks.part(15).y > landmarks.part(1).y) else 1 )

    def get_facial(self ,video_file, detector, predictor):
        self.vidcap = cv2.VideoCapture(video_file)
        self.success, self.img = self.vidcap.read()
        self.data = np.empty((0, 3), np.double)
        self.pitch = 0
        self.yaw = 0
        self.roll = 0
        self.count = 0
        while self.success:
            self.landmarks = self.get_landmarks(detector, predictor, self.img)
            if(self.landmarks != None):
                self.pitch += self.get_pitch_angle(self.landmarks)
                self.yaw += self.get_yaw_angle(self.landmarks)
                self.roll += self.get_roll_angle(self.landmarks)
                self.count += 1

            self.success, self.img = self.vidcap.read()
        self.count = max(self.count, 1)
        return [self.pitch / self.count, self.roll / self.count, self.yaw / self.count]