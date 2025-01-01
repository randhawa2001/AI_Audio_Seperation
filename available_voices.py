import requests
from dotenv import load_dotenv
from elevenlabs import ElevenLabs,VoiceSettings

load_dotenv()
url = "https://api.elevenlabs.io/v1/voices"

response = requests.request("GET", url)

print(response.text)