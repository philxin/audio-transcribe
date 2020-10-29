from __future__ import print_function
import time
import boto3
import urllib.request
import os
import json
import sys

# Usage: python3 aws_transport.py job_name file_uri audio_type landuage_code download_destination
# Example: python3 aws_transport.py audio_1 "https://...." mp3 en-US "/downloads/transcript.txt"


"""
get system argument for AWS job name, url of audio file to be transcribed (in AWS S3 bucket),
    audio file type, language code, and the destination path of trascribe text
"""
try:
	job_name = sys.argv[1]
	job_uri = sys.argv[2]
	media_format = sys.argv[3]
	landuage_code = sys.argv[4]
	download_file = sys.argv[5]
except:
	print("Wrong arguments.")
	sys.exit(1)

# transcribe the audio file using AWS Transcribe service
transcribe = boto3.client('transcribe')

transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat=media_format,
    LanguageCode=landuage_code
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
print(status)

# extract the url of transcript from the json returned
transcript_url = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

# use the url to get the transcript json
temp_json_path = os.path.dirname(os.path.abspath(__file__))+"/"+ job_name +".json"
urllib.request.urlretrieve(transcript_url, temp_json_path)

with open(temp_json_path) as j:
	temp_json = json.load(j)

# extract transcript text from json file
transcript = temp_json["results"]["transcripts"][0]["transcript"]

# save transcript as an txt file
with open(download_file, "w") as txt:
	txt.write(transcript)
print("Transcript saved at " + download_file)