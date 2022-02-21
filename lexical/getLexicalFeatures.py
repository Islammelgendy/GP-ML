import spacy

def get_lexical(text, emotions_list, words_list):
  """
    Load data from path
    Arguments:
      text (str) : The transcript of the interview
      emotions_list (pd.dataframe) : A list containing the full emotion list
      words_list (pd.series) : A list contains the words [used for : binary search for the word]
    Return:
      Dictionary containing the full lexical features
  """
  categories = ['i', 'we', 'they', 'Filler','Positive', 'Negative', 'Anger', 'Anticipation',
                'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust', 'DET', 'VERB', 'ADV',
                'ADP', 'CONJ', 'NEG', 'NUM', 'WC', 'UWC']
  features_dict = {key:0 for key in categories}
  features_dict['Filler'] = text.count('%HESITATION')
  text = text.replace('%HESITATION', '')
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(text)
  for token in doc:
    row = emotions_list.loc[words_list.searchsorted(token.text)]
    if(row['Word'] == token.text):
      for key in row.keys():
        if key != 'Word':
          features_dict[key] += row[key]
    if(token.text in features_dict.keys()):
      features_dict[token.text] += 1
    if(token.dep_.upper() in features_dict.keys()):
      features_dict[token.dep_.upper()] += 1
    if(token.pos_ in features_dict.keys()):
      features_dict[token.pos_] += 1
  features_dict['WC'] = len(list(text.split()))
  features_dict['UWC'] = len(set(list(text.split())))
  return features_dict