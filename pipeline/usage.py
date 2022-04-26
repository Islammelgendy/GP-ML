from Features import Features
from dotenv import dotenv_values

def main():
    config = dotenv_values('.env')
    apikey = config['APIKEY']
    url = config['URL']
    emotion_path = config['EMOTION_PATH']
    predictor_path = config['PREDICTOR_PATH']
    features = Features(apikey, url, emotion_path, predictor_path)
    # there should be a .wav (audio) and .avi (video) in that folder and you 
    # should pass the path to the interview without and extension
    # when you test you should download the video and save it to interview folder
    feature = features.get_features('../examples/interview/P1')
    print(feature)

if __name__ == '__main__':
    main()