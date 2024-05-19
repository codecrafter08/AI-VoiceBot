from dotenv import load_dotenv
load_dotenv()
import assemblyai as aai
import openai
import elevenlabs
import os
from elevenlabs.client import ElevenLabs

from queue import Queue
from aai_helper import handle_file_conversation, handle_real_time_conversation

openai.api_key = os.getenv('OPENAI_KEY')
el_client = ElevenLabs(
  api_key=os.getenv('ELLABS_KEY')
)


transcript_queue = Queue()

def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return
    if isinstance(transcript, aai.RealtimeFinalTranscript):
        transcript_queue.put(transcript.text + '')
        print("User:", transcript.text, end="\r\n")
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print("An error occured:", error)

# Conversation loop
def handle_conversation():
    while True:
        
        # handle real time conversation 

        transcript_result = handle_real_time_conversation()

        # to read audio from a file

        # FILE_URL = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

        # transcript_result = handle_file_conversation(FILE_URL)

        # Send the transcript to OpenAI for response generation
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo-0125',
            messages = [
                {"role": "system", "content": 'You are a highly skilled AI, answer the questions given within a maximum of 1000 characters.'},
                {"role": "user", "content": transcript_result}
            ]
        )

        text = response['choices'][0]['message']['content']

        # Convert the response to audio and play it
        audio = el_client.generate(
            text=text,
            voice="Rachel" # or any voice of your choice
        )

        print("\nAI:", text, end="\r\n")

        elevenlabs.play(audio)

handle_conversation()





