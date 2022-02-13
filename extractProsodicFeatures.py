from pyexpat import features
from moviepy.editor import VideoFileClip
import parselmouth
from parselmouth.praat import call
import numpy as np
from math import log, e, isnan 

def hz_to_mel(hz):
        return 550 * log(1 + hz/550, e)

class VideoToProsodic: 
    

    def getsound(video):
        clip = VideoFileClip(video)
        audioclip = clip.audio
        return audioclip.write_audiofile("audio.Wav")
    
    def getProsodicFeatures(audio):

        snd = parselmouth.Sound(audio  )
        duration = snd.get_total_duration()
        energy = snd.get_energy()
        power = snd.get_power()

        pitch = snd.to_pitch()
        pitch_values = pitch.selected_array['frequency']
        pitch_values[pitch_values == 0] = np.nan
        min_pitch = hz_to_mel(np.nanmin(pitch_values))
        max_pitch = hz_to_mel(np.nanmax(pitch_values))
        mean_pitch = hz_to_mel(np.nanmean(pitch_values))
        pitch_std = hz_to_mel(np.nanstd(pitch_values))
        diff_pitch_max_min = max_pitch - min_pitch
        diff_pitch_max_mean = max_pitch - mean_pitch

        intensity = snd.to_intensity()
        intensity_values = intensity.as_array()
        min_intensity = np.nanmin(intensity_values)
        max_intensity = np.nanmax(intensity_values)
        mean_intensity = np.nanmean(intensity_values)
        intensity_std = np.nanstd(intensity_values)
        diff_intensity_max_min = (max_intensity - min_intensity)
        diff_intensity_max_mean = (max_intensity - mean_intensity)

        format = snd.to_formant_burg()
        f1mean = call(format, "Get mean", 1, 0, 0, "hertz")
        f2mean = call(format, "Get mean", 2, 0, 0, "hertz")
        f3mean = call(format, "Get mean", 3, 0, 0, "hertz")
        f1std = call(format, "Get standard deviation", 1, 0, 0, "hertz")
        f2std = call(format, "Get standard deviation", 2, 0, 0, "hertz")
        f3std = call(format, "Get standard deviation", 3, 0, 0, "hertz")
        f2meanf1 = f2mean / f1mean
        f3meanf1 = f3mean / f1mean
        f2stdf1 = f2std / f1std
        f3stdf1 = f3std / f1std

        point_process = call(snd, "To PointProcess (periodic, cc)", min_pitch, max_pitch)
        jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        shimmer =  call([snd, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        rap_jitter = call(point_process, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
        features = np.array([duration,energy,power])
        
       
        return print(features)
VideoToProsodic.getProsodicFeatures("P1.wav")

         


 
        



    