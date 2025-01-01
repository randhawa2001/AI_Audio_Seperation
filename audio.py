import os
import assemblyai as aai
import elevenlabs as el
from dotenv import load_dotenv
from elevenlabs import ElevenLabs,VoiceSettings
from pydub import AudioSegment  # You can install this library with 'pip install pydub'

load_dotenv()
# AssemblyAI configuration
aai.settings.api_key = os.environ['AAI_API_KEY']

# Define the transcription configuration
config = aai.TranscriptionConfig(speaker_labels=True)

# Transcribe the audio file
audio_file = "audio.wav"  # Replace with your actual file path
transcript = aai.Transcriber().transcribe(audio_file, config)

# Lists to store texts for each speaker
speaker_a_texts = []
speaker_b_texts = []

# Sort the utterances into separate lists for each speaker
for utterance in transcript.utterances:
    if utterance.speaker == "A":
        speaker_a_texts.append(utterance.text)
    elif utterance.speaker == "B":
        speaker_b_texts.append(utterance.text)

# ElevenLabs API for Text-to-Speech (TTS)
client = ElevenLabs(
    api_key= os.environ['ELEVENLABS_API_KEY'],
)
def generate_speech_a(text):
    output_voice = client.text_to_speech.convert(
            voice_id="9BWtsMINqrJLrRacOk9x",
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            voice_settings=VoiceSettings(
                stability=0.1,
                similarity_boost=0.3,
                style=0.2,
            ),
        )
    return output_voice

def generate_speech_b(text):
    output_voice = client.text_to_speech.convert(
            voice_id="pMsXgVXv3BLzUgSXRplE",
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            voice_settings=VoiceSettings(
                stability=0.1,
                similarity_boost=0.3,
                style=0.2,
            ),
        )
    return output_voice

# Function to generate speech and return audio file path
def generate_speech(text, speaker_name):
    file_path = f"{speaker_name}_output.wav"
    if speaker_name == "A":
        with open(file_path, "wb") as f:
            f.write(generate_speech_a(text))

    elif speaker_name == "B":
        with open(file_path, "wb") as f:
            f.write(generate_speech_b(text))

    return file_path

# Create audio for Speaker A and Speaker B
a_audio_segments = []
for text in speaker_a_texts:
    a_audio_file = generate_speech(text, "A")
    a_audio_segments.append(AudioSegment.from_wav(a_audio_file))

b_audio_segments = []
for text in speaker_b_texts:
    b_audio_file = generate_speech(text, "B")
    b_audio_segments.append(AudioSegment.from_wav(b_audio_file))

# Step 3: Combine the audios in sequence
final_audio = AudioSegment.empty()

# Assuming the transcript is ordered correctly, combine alternating speakers
for utterance in transcript.utterances:
    if utterance.speaker == "A":
        final_audio += a_audio_segments.pop(0)
    elif utterance.speaker == "B":
        final_audio += b_audio_segments.pop(0)

# Export the final combined audio
final_audio.export("final_conversation.wav", format="wav")

print("Final combined audio saved as 'final_conversation.wav'")
