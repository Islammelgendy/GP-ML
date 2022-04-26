import parselmouth
from parselmouth.praat import call
import numpy as np
import math
import re

class Prosodic:
    
    def voice_report_dict(self, voice_report_str):
        self.report_list = [''.join(e) for e in voice_report_str.split('\n')]
        self.remove_list = ['Pitch:', 'Pulses:', 'Voicing:', 'Jitter:', 'Shimmer:', 'Harmonicity of the voiced parts only:', '']
        self.report_list = list(set(self.report_list).difference(set(self.remove_list)))
        self.pattern = re.compile("^.*\w*: \d+\.?\d+E?-?\d?\%?")
        self.result = [''.join(e) for e in list(map(self.pattern.findall, self.report_list))]
        self.keyval_list = list(map(str.strip, self.result))
        self.keyval_list = [w.replace('%', 'E-2') for w in self.keyval_list]
        self.keyval_dict = {keyval.split(': ')[0]:float(keyval.split(': ')[1]) for keyval in self.keyval_list}
        return self.keyval_dict

    def hz_to_mel(self, hz):
        return 550 * math.log(1 + hz/550, math.e)

    def get_prosodic_features(self, audio_path):
        self.snd = parselmouth.Sound(audio_path)

        self.duration = self.snd.get_total_duration()
        self.energy = self.snd.get_energy()
        self.power = self.snd.get_power()

        self.pitch = self.snd.to_pitch()
        self.pitch_values = self.pitch.selected_array['frequency']
        self.pitch_values[self.pitch_values == 0] = np.nan
        self.min_pitch = self.hz_to_mel(np.nanmin(self.pitch_values))
        self.max_pitch = self.hz_to_mel(np.nanmax(self.pitch_values))
        self.mean_pitch = self.hz_to_mel(np.nanmean(self.pitch_values))
        self.pitch_std = self.hz_to_mel(np.nanstd(self.pitch_values))
        self.diff_pitch_max_min = self.max_pitch - self.min_pitch
        self.diff_pitch_max_mean = self.max_pitch - self.mean_pitch

        self.intensity = self.snd.to_intensity()
        self.intensity_values = self.intensity.as_array()
        self.min_intensity = np.nanmin(self.intensity_values)
        self.max_intensity = np.nanmax(self.intensity_values)
        self.mean_intensity = np.nanmean(self.intensity_values)
        self.intensity_std = np.nanstd(self.intensity_values)
        self.diff_intensity_max_min = (self.max_intensity - self.min_intensity)
        self.diff_intensity_max_mean = (self.max_intensity - self.mean_intensity)

        self.format = self.snd.to_formant_burg()
        self.f1mean = call(self.format, "Get mean", 1, 0, 0, "hertz")
        self.f2mean = call(self.format, "Get mean", 2, 0, 0, "hertz")
        self.f3mean = call(self.format, "Get mean", 3, 0, 0, "hertz")
        self.f1std = call(self.format, "Get standard deviation", 1, 0, 0, "hertz")
        self.f2std = call(self.format, "Get standard deviation", 2, 0, 0, "hertz")
        self.f3std = call(self.format, "Get standard deviation", 3, 0, 0, "hertz")
        self.f2meanf1 = self.f2mean / self.f1mean
        self.f3meanf1 = self.f3mean / self.f1mean
        self.f2stdf1 = self.f2std / self.f1std
        self.f3stdf1 = self.f3std / self.f1std

        self.point_process = call(self.snd, "To PointProcess (periodic, cc)", self.min_pitch, self.max_pitch)
        self.jitter = call(self.point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        self.shimmer =  call([self.snd, self.point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        self.rap_jitter = call(self.point_process, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)

        self.voice_report_str = call([self.snd, self.pitch, self.point_process], "Voice report", 0.0, 0.0, self.min_pitch, self.max_pitch, 1.3, 1.6, 0.03, 0.45)
        self.rep_dict = self.voice_report_dict(self.voice_report_str)
        self.precent_unvoiced = self.rep_dict['Fraction of locally unvoiced frames']
        self.num_voice_breaks = self.rep_dict['Number of voice breaks']
        self.precent_breaks = self.rep_dict['Degree of voice breaks']
        self.txt_grid = call(self.intensity, "To TextGrid (silences)", -25, 0.1, 0.1, "silent", "sounding")
        self.total = call(self.txt_grid, "Get number of intervals", 1)
        self.dur_pauses = 0
        self.avg_pause = 0
        self.max_pause = 0
        self.cnt_pauses = 0
        for i in range(self.total):
            typ = call(self.txt_grid, "Get label of interval", 1, i + 1)
            if(typ == "silent"):
                self.start = call(self.txt_grid, "Get starting point", 1, i + 1)
                self.end = call(self.txt_grid, "Get end point", 1, i + 1)
                self.max_pause = max(self.max_pause, self.end - self.start)
                self.cnt_pauses += 1
                self.dur_pauses += self.end - self.start

        self.avg_pause = self.dur_pauses / max(self.cnt_pauses, 1)
        self.features = np.array([self.duration, self.energy, self.power, self.min_pitch, self.max_pitch, self.mean_pitch, 
                            self.pitch_std, self.diff_pitch_max_min, self.diff_pitch_max_mean, self.min_intensity,
                            self.max_intensity, self.mean_intensity, self.intensity_std, self.diff_intensity_max_min,
                            self.diff_intensity_max_mean, self.f1mean, self.f2mean, self.f3mean, self.f1std, self.f2std, self.f3std,
                            self.f2meanf1, self.f3meanf1, self.f2stdf1, self.f3stdf1, self.jitter, self.shimmer, self.rap_jitter, self.precent_unvoiced,
                            self.num_voice_breaks, self.precent_breaks, self.cnt_pauses, self.max_pause, self.avg_pause, self.dur_pauses])
        return self.features
