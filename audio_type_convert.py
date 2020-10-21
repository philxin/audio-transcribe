"""
This is a simple python script for converting audio types using pydub pa.

Usage: python3 audio_type_convert.py <audio_file> <to_format>

example: python3 audio_type_convert.py audio_file.wav mp3
"""

from pydub import AudioSegment
import sys
import os

audio_file = ""
try: 
	audio_file = str(sys.argv[1])
except:
	print("A path of an audio file is needed. (python3 audio_type_convert.py <audio_file> <to_format>)")
	sys.exit(1)


to_format = ""
try: 
	to_format = str(sys.argv[2])
except:
	print("A format to which the audio will be converted is needed. (python3 audio_type_convert.py <audio_file> <to_format>)")
	sys.exit(1)

print("Start converting...")

# get the audio file name and type of the input file
origin_format = audio_file.split('.')[-1]
origin_name = os.path.splitext(audio_file)[0]

audio_convert = AudioSegment.from_file(audio_file, format = origin_format)

print("Audio file read.")

audio_convert.export(origin_name + "." + to_format, format = to_format)

print("Conversion completed.")