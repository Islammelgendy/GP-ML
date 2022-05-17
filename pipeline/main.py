from fastapi import FastAPI
import pickle 
from Features import Features
from dotenv import dotenv_values

app = FastAPI()

config = dotenv_values('.env')
apikey = config['APIKEY']
url = config['URL']
emotion_path = config['EMOTION_PATH']
predictor_path = config['PREDICTOR_PATH']

features = Features(apikey, url, emotion_path, predictor_path)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('models/evaluator-model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

def predictionResponse(pred):
    json = {
        'Excited': pred[0],
        'Engaged': pred[1],
        'Smiled': pred[2],
        'RecommendHiring': pred[3],
        'NoFillers': pred[4],
        'StructuredAnswers': pred[5],
        'Friendly': pred[6],
        'Focused': pred[7],
        'NotAwkward': pred[8],
        'Paused': pred[9],
        'EyeContact': pred[10],
        'Authentic': pred[11],
        'Calm': pred[12],
        'SpeakingRate': pred[13],
        'NotStressed': pred[14]
    }
    return json

@app.get("/get_features/{interviewPath:path}")
async def getFeatures(interviewPath: str):
    interviewPath = interviewPath.split('.')[0]
    feature = features.get_features(interviewPath)
    normalized_features = scaler.transform(feature)
    predictions = model.predict(normalized_features)
    # predictions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] # Used for testing the server without running the model
    jsonPredictions = predictionResponse(predictions)
    return {"predictions": jsonPredictions}
