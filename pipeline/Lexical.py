from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class Lexical:

    def get_transcript(self, audio_file, apikey, url):
        self.authenticator = IAMAuthenticator(apikey)
        self.stt = SpeechToTextV1(authenticator=self.authenticator)
        self.stt.set_service_url(url)
        with open(audio_file, 'rb') as f:
            self.res = self.stt.recognize(audio=f, content_type='audio/wav', model='en-US_NarrowbandModel').get_result()
        self.transcript = ""
        for sentence in self.res['results']:
            self.transcript += sentence['alternatives'][0]['transcript'].lower()
        return self.transcript

    def get_lexical(self, text, emotions_list, word_list, nlp):
        self.categories = ['i', 'we', 'they', 'Filler','Positive', 'Negative', 'Anger', 'Anticipation',
                        'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust', 'DET', 'VERB', 'ADV',
                        'ADP', 'CONJ', 'NEG', 'NUM', 'WC', 'UWC']
        self.features_dict = {key:0 for key in self.categories}
        self.features_dict['Filler'] = self.text.count('%hesitation')
        self.text = text.replace('%hesitation', '')
        self.doc = nlp(self.text)
        for self.token in self.doc:
            try:
                self.row = emotions_list.loc[word_list.searchsorted(self.token.text)]
                if(self.row['Word'] == self.token.text):
                    for self.key in self.row.keys():
                        if self.key != 'Word':
                            self.features_dict[self.key] += self.row[self.key]
            except:
                pass
            if(self.token.text in self.features_dict.keys()):
                self.features_dict[self.token.text] += 1
            if(self.token.dep_.upper() in self.features_dict.keys()):
                self.features_dict[self.token.dep_.upper()] += 1
            if(self.token.pos_ in self.features_dict.keys()):
                self.features_dict[self.token.pos_] += 1
        self.features_dict['WC'] = len(list(self.text.split()))
        self.features_dict['UWC'] = len(set(list(self.text.split())))
        return list(self.features_dict.values())