import assemblyai as aai

# Set your AssemblyAI API key
aai.settings.api_key = "48bc357263ce47a2aa99b7a967ac60bf"

# You can use a local filepath or a publicly accessible URL
audio_file = "audio.wav"

# Define transcription configuration to include speaker labels
config = aai.TranscriptionConfig(speaker_labels=True)

# Transcribe the audio file
transcript = aai.Transcriber().transcribe(audio_file, config)

# File paths for saving speaker texts
speaker_a_file = "speaker_a.txt"
speaker_b_file = "speaker_b.txt"

# Open the files for writing
with open(speaker_a_file, "w") as a_file, open(speaker_b_file, "w") as b_file:
    # Loop through each utterance and save to the corresponding file
    for utterance in transcript.utterances:
        if utterance.speaker == "A":
            a_file.write(f"{utterance.text}\n")
        elif utterance.speaker == "B":
            b_file.write(f"{utterance.text}\n")

print(f"Text files created: '{speaker_a_file}' for Speaker A and '{speaker_b_file}' for Speaker B")
