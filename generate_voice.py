from elevenlabs import ElevenLabs, VoiceSettings
from dotenv import load_dotenv
import os
# Initialize ElevenLabs client with your API key

load_dotenv()
API_KEY = os.environ['ELEVENLABS_API_KEY']
client = ElevenLabs(api_key = API_KEY)

# Define a function to convert text to speech and save to a file
def generate_speech_from_text(file_path, output_audio_file, voice_id, stability=0.5, similarity_boost=0.5, style=0.5):
    # Open and read the text file
    with open(file_path, "r") as f:
        text = f.read()

    # Generate speech from the text using ElevenLabs API (returns a generator)
    audio_generator = client.text_to_speech.convert(
        voice_id=voice_id,
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        voice_settings=VoiceSettings(
            stability=stability,
            similarity_boost=similarity_boost,
            style=style
        ),
    )

    # Write the generated audio to the output file
    with open(output_audio_file, "wb") as audio_file:
        for chunk in audio_generator:
            audio_file.write(chunk)  # Write each chunk to the file
    print(f"Generated audio saved to {output_audio_file}")

# File paths for speaker A and speaker B texts
speaker_a_text_file = "speaker_a.txt"
speaker_b_text_file = "speaker_b.txt"

# Define the voice IDs for Speaker A and Speaker B (replace these with actual IDs or use different voices)
voice_id_a = "JBFqnCBsd6RMkjVDRZzb"  # Replace with actual voice ID for Speaker A
voice_id_b = "XB0fDUnXU5powFXDhCwa"  # Replace with actual voice ID for Speaker B

# Generate speech and save to separate audio files for each speaker
generate_speech_from_text(speaker_a_text_file, "speaker_a_audio.mp3", voice_id_a, stability=0.1, similarity_boost=0.3, style=0.2)
generate_speech_from_text(speaker_b_text_file, "speaker_b_audio.mp3", voice_id_b, stability=0.2, similarity_boost=0.4, style=0.3)
