import cv2
import numpy as np
import math
import dlib


def get_landmarks(detector, predictor, img):
  gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
  faces = detector(gray)
  if(len(faces) == 0):
    return []
  for face in faces:
    landmarks = predictor(image=gray, box=face)
  return landmarks

def get_euclidean_distance(x, y):
  return math.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)

def get_yaw_angle(landmarks):
  left_line = get_euclidean_distance([landmarks.part(21).x, landmarks.part(17).x], [landmarks.part(21).y, landmarks.part(17).y])
  right_line = get_euclidean_distance([landmarks.part(26).x, landmarks.part(22).x], [landmarks.part(26).y, landmarks.part(22).y])
  return math.asin(1 - min(left_line, right_line) / max(left_line, right_line)) * (-1 if right_line < left_line else 1)

def get_pitch_angle(landmarks):
  left_line = get_euclidean_distance([landmarks.part(29).x, landmarks.part(1).x], [landmarks.part(29).y, landmarks.part(1).y])
  right_line = get_euclidean_distance([landmarks.part(29).x, landmarks.part(15).x], [landmarks.part(29).y, landmarks.part(15).y])
  vertical_distance = np.cross([landmarks.part(15).x - landmarks.part(1).x, landmarks.part(15).y - landmarks.part(1).y], [landmarks.part(29).x - landmarks.part(1).x, landmarks.part(29).y - landmarks.part(1).y]) / np.linalg.norm([landmarks.part(15).x - landmarks.part(1).x, landmarks.part(15).y - landmarks.part(1).y])
  return (math.asin(vertical_distance / left_line) + math.asin(vertical_distance / right_line)) / 2

def get_roll_angle(landmarks):
  real_line = get_euclidean_distance([landmarks.part(15).x, landmarks.part(1).x], [landmarks.part(15).y, landmarks.part(1).y])
  virtual_line = get_euclidean_distance([landmarks.part(15).x, landmarks.part(1).x], [landmarks.part(1).y, landmarks.part(1).y])
  return math.acos(virtual_line / real_line) * (-1 if(landmarks.part(15).y > landmarks.part(1).y) else 1 )

def get_facial_features(img, predictor_path):
  detector = dlib.get_frontal_face_detector()
  predictor = dlib.shape_predictor(predictor_path)
  landmarks = get_landmarks(detector, predictor, img)
  if(landmarks):
    yaw = math.degrees(get_yaw_angle(landmarks))
    pitch = math.degrees(get_pitch_angle(landmarks))
    roll = math.degrees(get_roll_angle(landmarks))
  features = np.array([yaw, pitch, roll])
  return features