from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import pickle
from dotenv import dotenv_values
import urllib.request
import json

from Features import Features

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:80",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

callbackURL = 'http://127.0.0.1:3000/callback'

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
    
def callback(interviewPath, predictions):
    jsonPredictions = predictionResponse(predictions)    
    body = {'predictions': jsonPredictions}
    callback = f"{callbackURL}/{interviewPath}"
    req = urllib.request.Request(callback)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)

def predict(interviewPath):
    feature = features.get_features(interviewPath)
    normalized_features = scaler.transform(feature)
    predictions = model.predict(normalized_features)
    callback(interviewPath, predictions)

@app.get("/get-features/{interviewPath:path}")
async def getFeatures(interviewPath: str, background_tasks: BackgroundTasks):
    interviewPath = interviewPath.split('.')[0]
    background_tasks.add_task(predict, interviewPath)
    return {"status": "processing"}
