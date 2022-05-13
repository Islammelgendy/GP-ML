import pickle 
from Features import Features
from dotenv import dotenv_values
import numpy as np 
import FileProcessing

with open('models/scaler.pkl', 'rb') as f:
  scaler = pickle.load(f)

with open('models/evaluator-model.pkl', 'rb') as f:
  model = pickle.load(f)

def main():
    config = dotenv_values('.env')
    apikey = config['APIKEY']
    url = config['URL']
    emotion_path = config['EMOTION_PATH']
    predictor_path = config['PREDICTOR_PATH']
    features = Features(apikey, url, emotion_path, predictor_path)
    # there should be a .wav (audio) and .avi (video) in that folder and you 
    # should pass the path to the interview without an extension
    # when you test you should download the video and save it to interview folder
    file_path = '/home/sloaka/Desktop/GP-ML/example/interview/P1'
    FileProcessing.split_audio(file_path)
    feature = features.get_features(file_path)
    FileProcessing.remove_audio(file_path)
    scaled_features =  scaler.transform(feature)

    print(model.predict(scaled_features))


if __name__ == '__main__':
    main()