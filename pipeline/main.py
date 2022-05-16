from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    feature = features.get_features("/home/sloaka/Desktop/GP-ML/example/interview.a/P1vi")
    normalized_features = scaler.transform(feature)
    predictions = model.predict(normalized_features)

    return {"predictions":str(predictions)}


@app.get("/file/{filePath:path}")
def getFileByPath(filePath: str):
    return {'received' : filePath}
