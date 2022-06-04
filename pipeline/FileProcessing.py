import moviepy.editor as mp
import os

def split_audio(file_path):
    my_clip = mp.VideoFileClip(file_path + '.avi')
    my_clip.audio.write_audiofile(file_path + '.wav', codec = 'pcm_s16le', verbose=False, logger=None)

def remove_audio(file_path):
    os.remove(file_path + '.wav')