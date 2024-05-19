import assemblyai as aai
import os

from queue import Queue

# Set API keys
aai.settings.api_key = os.getenv('AAI_KEY')

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
def handle_real_time_conversation():
    transcriber = aai.RealtimeTranscriber(
        on_data=on_data,
        on_error=on_error,
        sample_rate=44_100,
    )

    # Start the connection
    transcriber.connect()

    # Open  the microphone stream
    microphone_stream = aai.extras.MicrophoneStream()

    # Stream audio from the microphone
    transcriber.stream(microphone_stream)

    # Close current transcription session with Crtl + C
    transcriber.close()

    # Retrieve data from queue
    transcript_result = transcript_queue.get()
    return transcript_result






def handle_file_conversation(FILE_URL):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
        transcript_result = "What is the capital of India ?"
    else:
        transcript_result = transcript.text
    return transcript_result

        
   









