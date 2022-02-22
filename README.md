# GP-ML

## Features
|Prosodic Feature|Label|Description|
|-|-|-|
|Duration|``duration``||
|Mean spectral energy|``energy``|The expression of emotion impacts the spectral energy distribution. On the one hand emotional states characterized by a breathy voice quality such as tenderness, sadness, and eroticism present a low harmonic energy. On the other hand, emotional states such as joy, anger, and fear are characterized by high harmonic energy.|
|Power|``power``||
|Pitch|``min_pitch``<br/>``max_pitch``<br/>``mean_pitch``<br/>``pitch_std``<br/>``diff_pitch_max_min``<br/>``diff_pitch_max_mean``|Pitch is how high or low the voice sounds, The pitch of a voice may change based on the situation like in stressful situations the voice's fundamental frequency raises, and that "active" emotions such as anger and fear tend to be reflected in increased mean pitch and pitch variance, whereas "low energy" states such as sorrow and indifference are associated with a lower mean pitch and a slower speech rate.|
|Intensity|``min_intensity``<br/>``max_intensity``<br/>``mean_intensity``<br/>``intensity_std``<br/>``diff_intensity_max_min``<br/>``diff_intensity_max_mean``|It has often been suggested that there are affects that are expressed loudly and others for which a low intensity is typical. Acoustic profiles of emotional expressions suggest that anger and happiness are signaled by increased pitch, increased loudness, and a faster rate of speech, whereas boredom and grief are characterized by low pitch and a slow speaking rate.|
|Fundamental Formant|``f1mean``<br/>``f2mean``<br/>``f3mean``<br/>``f1std``<br/>``f2std``<br/>``f3std``<br/>``f2meanf1``<br/>``f3meanf1``<br/>``f2stdf1``<br/>``f3stdf1``|The frequencies of the first and second formant of the vowels ``i``, ``u``, and ``a``was measured and shown to be significantly affected by emotion dimension. High arousal resulted in a higher mean F1 in all vowels, whereas positive valence resulted in higher mean values for F2.|
|Jitter and Shimmer|``jitter``<br/>``shimmer``<br/>``rap_jitter``|Jitter and shimmer can be indicators of underlying stress in human speech|
|Pauses|``dur_pauses``<br/>``avg_pause``<br/>``max_pause``<br/>``cnt_pauses``||

|Lexical Feature|Label|Example|
|-|-|-|
|I|``i``|I, I’m, I’ve, I’ll, I’d, etc.|
|We|``we``|we, we’ll, we’re, us, our, etc.|
|They|``They``|they, they’re, they’ll, them, etc.|
|Filler words| ``Fillers``|uh, umm, etc.|
|Positive words|``Positive``|accomplishment, encourage, helpful, etc.|
|Negative words|``Negative``|bad, hate, lose, etc.|
|Anger|``Anger``|argue, clash, angry, etc.|
|Anticipation|``Anticipation``|achievement, deal, medal, etc.|
|Fear|``Fear``|afraid, cruel, fright, etc.|
|Joy|``Joy``|enjoy, advent, miracle, etc.|
|Sadness|``Sadness``|sad, disappointment, punishment, etc|
|Surprise|``Surprise``|surprised, alarming, emergency, etc.|
|Trust|``Trust``|trust, ensemble, leader, etc.|
|Articles|``DET``|a, an, the, etc.|
|Verbs|``VERB``|common English verbs.|
|Adverbs|``ADV``|common English adverbs.|
|Prepositions|``ADP``|common prepositions|
|Conjunctions|``CONJ``|common conjunctions|
|Negations|``NEG``|no, never, none, cannot, don’t, etc|
|Number|``NUM``|words related to number, e.g.,first, second, hundred, etc.|
|Words count|``WC``||
|Unique words count|``UWC``||
