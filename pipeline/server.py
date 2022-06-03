import pickle
import FileProcessing
from dotenv import dotenv_values
import json
import pika

from Features import Features

config = dotenv_values('.env')
apikey = config['APIKEY']
url = config['URL']
emotion_path = config['EMOTION_PATH']
predictor_path = config['PREDICTOR_PATH']

mq_url = config['MQ_URL']
mq_publisher = config['MQ_PUBLISHER']
mq_consumer = config['MQ_CONSUMER']

params = pika.URLParameters(mq_url)
connection = pika.BlockingConnection(params)

features = Features(apikey, url, emotion_path, predictor_path)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('models/evaluator-model.pkl', 'rb') as f:
    model = pickle.load(f)

def predictionResponse(pred):
    json = {
        'Excited': str(pred[0][0][0]),
        'Engaged': str(pred[1][0][0]),
        'Smiled': str(pred[2][0][0]),
        'RecommendHiring': str(pred[3][0][0]),
        'NoFillers': str(pred[4][0][0]),
        'StructuredAnswers': str(pred[5][0][0]),
        'Friendly': str(pred[6][0][0]),
        'Focused': str(pred[7][0][0]),
        'NotAwkward': str(pred[8][0][0]),
        'Paused': str(pred[9][0][0]),
        'EyeContact': str(pred[10][0][0]),
        'Authentic': str(pred[11][0][0]),
        'Calm': str(pred[12][0][0]),
        'SpeakingRate': str(pred[13][0][0]),
        'NotStressed': str(pred[14][0][0])
    }
    return json

def publishToQueue(body):
    channel = connection.channel()
    channel.queue_declare(queue=mq_publisher, durable=True)
    channel.basic_publish(exchange='',
                            routing_key=mq_publisher,
                            body=body)
    channel.close()

def predict(interviewPath):
    interviewPath = interviewPath.split('.')[0]
    FileProcessing.split_audio(interviewPath)
    feature = features.get_features(interviewPath)
    normalized_features = scaler.transform(feature)
    predictions = model.predict(normalized_features)
    jsonPredictions = predictionResponse(predictions)
    publishToQueue(json.dumps({"predictions": jsonPredictions}))

def consuemFromQueue():
    channel = connection.channel()

    channel.queue_declare(queue=mq_consumer, durable=True)

    def callback(ch, method, properties, body):
        body = json.loads(body.decode('utf-8').replace("'", '"'))
        predict(body['path'])

    channel.basic_consume(queue=mq_consumer, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

consuemFromQueue()