from Features import Features
from dotenv import dotenv_values

def main():
    config = dotenv_values('.env')
    apikey = config['APIKEY']
    url = config['URL']
    emotion_path = config['EMOTION_PATH']
    predictor_path = config['PREDICTOR_PATH']
    features = Features(apikey, url, emotion_path, predictor_path)
    print(features)

if __name__ == '__main__':
    main()