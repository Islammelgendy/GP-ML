import spacy
import dlib
import pandas as pd
from Prosodic import Prosodic
from Lexical import Lexical
from Facial import Facial

class Features:
    def __init__(self, apikey, url, emotion_path, predictor_path):
        self.audio_extension = '.wav'
        self.video_extension = '.avi'
        self.predictor_path = predictor_path
        self.apikey = apikey
        self.url = url
        self.emotion_list = pd.read_excel(emotion_path)
        self.word_list = self.emotion_list['Word'].squeeze()
        self.nlp = spacy.load("en_core_web_sm")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.predictor_path)
        self.Prosodic = Prosodic()
        self.Facial = Facial()
        self.Lexical = Lexical()

    def get_features(self, file_path):
        self.npdataset = []
        try:
            self.dataset = []
            self.dataset.extend(self.Prosodic.extract_prosodic(file_path + self.audio_extension, 'filename'))
            self.transcript = self.Lexical.get_transcript(file_path + self.audio_extension, self.apikey, self.url)
            self.dataset.extend(self.Lexical.get_lexical(self.transcript, self.emotion_list, self.word_list, self.nlp))
            self.dataset.extend(self.Facial.get_facial(file_path + self.video_extension, self.detector, self.predictor))
        except Exception as e:
            print(e)
        self.npdataset.append(self.dataset)
        return pd.DataFrame(self.npdataset, columns=['duration', 'energy', 'power', 'min_pitch', 'max_pitch', 'mean_pitch', 
                                        'pitch_std', 'diff_pitch_max_min', 'diff_pitch_max_mean', 'min_intensity',
                                        'max_intensity', 'mean_intensity', 'intensity_std', 'diff_intensity_max_min',
                                        'diff_intensity_max_mean', 'f1mean', 'f2mean', 'f3mean', 'f1std', 'f2std', 'f3std',
                                        'f2meanf1', 'f3meanf1', 'f2stdf1', 'f3stdf1', 'jitter', 'shimmer', 'rap_jitter', 
                                        'dur_pauses', 'avg_pause', 'max_pause', 'cnt_pauses', 'i', 'we', 'they', 'Filler', 
                                        'Positive', 'Negative', 'Anger', 'Anticipation', 'Fear', 'Joy', 'Sadness', 'Surprise', 
                                        'Trust', 'DET', 'VERB', 'ADV', 'ADP', 'CONJ', 'NEG', 'NUM', 'WC', 'UWC', 'avg_pitch', 'avg_roll', 'avg_yaw'])
