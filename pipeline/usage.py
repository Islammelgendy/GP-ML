import pickle 
from Features import Features
from dotenv import dotenv_values

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
    feature = features.get_features('/home/sloaka/Desktop/GP-ML/example/interview/P1')
    scaled_features = scaler.fit(feature)
    print(model.predict(scaled_features))


if __name__ == '__main__':
    main()