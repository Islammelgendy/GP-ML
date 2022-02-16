import re

def voice_report_dict(voice_report_str):
  report_list = [''.join(e) for e in voice_report_str.split('\n')]
  remove_list = ['Pitch:', 'Pulses:', 'Voicing:', 'Jitter:', 'Shimmer:', 'Harmonicity of the voiced parts only:', '']
  report_list = list(set(report_list).difference(set(remove_list)))
  pattern = re.compile("^.*\w*: \d+\.?\d+E?-?\d?\%?")
  result = [''.join(e) for e in list(map(pattern.findall, report_list))]
  keyval_list = list(map(str.strip, result))
  keyval_list = [w.replace('%', 'E-2') for w in keyval_list]
  keyval_dict = {keyval.split(': ')[0]:float(keyval.split(': ')[1]) for keyval in keyval_list}
  return keyval_dict