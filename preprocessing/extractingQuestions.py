from datetime import datetime
import ffmpeg

def get_time_duration(start, end):
  FMT = '%M:%S.%f'
  timestamp = []
  timestamp.append(start)
  timestamp.append(datetime.strptime(end, FMT) - datetime.strptime(start, FMT))
  return timestamp

def split_questions(file_name, timestamp, question, audio_path, out_path):
  stream = ffmpeg.input(audio_path + file_name + '.wav', f = 'wav', ss = timestamp[0], t = timestamp[1])
  stream = ffmpeg.output(stream, out_path + file_name + 'Q' + str(question) + '.wav')
  stream = ffmpeg.overwrite_output(stream)
  try:
    ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
  except ffmpeg.Error as e:
    print('stdout:', e.stdout.decode('utf8'))
    print('stderr:', e.stderr.decode('utf8'))
    raise e

def extracting_questions(prefix, timestamp_path, audio_path, out_path, start = 1, end = 90):
  for i in range(start, end):
    try:
        with open(timestamp_path + prefix + str(i) + '.txt') as timestamp_file:
          for l, line in enumerate(timestamp_file):
            line = line.split(' ')
            timestamp = get_time_duration(line[0], line[1][:-1])
            split_questions(prefix + str(i), timestamp, l + 1, audio_path, out_path)
    except Exception: 
      continue