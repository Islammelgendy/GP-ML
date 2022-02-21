import parselmouth
from parselmouth.praat import call
import numpy as np
from voiceReport import voice_report_dict
import math

def hz_to_mel(hz):
  """
    Convert the frequency from Hertz to MEL
    Arguments:
      hz (int) : the frequency in Hertz
    Return:
      the frequency in MEL (int)
  """
  return 550 * math.log(1 + hz/550, math.e)

def get_prosodic_features(audio_path):
  """
    Get the prosodic features of an interview
    Arguments:
      audio_path (str) : A path to the audio file
    Return:
      numpy array containing the full prosodic features
  """
  snd = parselmouth.Sound(audio_path)

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
  
  voice_report_str = call([snd, pitch, point_process], "Voice report", 0.0, 0.0, min_pitch, max_pitch, 1.3, 1.6, 0.03, 0.45)
  rep_dict = voice_report_dict(voice_report_str)
  precent_unvoiced = rep_dict['Fraction of locally unvoiced frames']
  num_voice_breaks = rep_dict['Number of voice breaks']
  precent_breaks = rep_dict['Degree of voice breaks']
  txt_grid = call(intensity, "To TextGrid (silences)", -25, 0.1, 0.1, "silent", "sounding")
  total = call(txt_grid, "Get number of intervals", 1)
  dur_pauses = 0
  avg_pause = 0
  max_pause = 0
  cnt_pauses = 0
  for i in range(total):
    typ = call(txt_grid, "Get label of interval", 1, i + 1)
    if(typ == "silent"):
      start = call(txt_grid, "Get starting point", 1, i + 1)
      end = call(txt_grid, "Get end point", 1, i + 1)
      max_pause = max(max_pause, end - start)
      cnt_pauses += 1
      dur_pauses += end - start

  avg_pause = dur_pauses / max(cnt_pauses, 1)
  features = np.array([duration, energy, power, min_pitch, max_pitch, mean_pitch, 
                       pitch_std, diff_pitch_max_min, diff_pitch_max_mean, min_intensity,
                       max_intensity, mean_intensity, intensity_std, diff_intensity_max_min,
                       diff_intensity_max_mean, f1mean, f2mean, f3mean, f1std, f2std, f3std,
                       f2meanf1, f3meanf1, f2stdf1, f3stdf1, jitter, shimmer, rap_jitter, precent_unvoiced,
                       num_voice_breaks, precent_breaks, cnt_pauses, max_pause, avg_pause, dur_pauses])
  return features

         


 
        



    