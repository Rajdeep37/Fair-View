import speech_recognition as sr
from pydub import AudioSegment
import sys
import os

# Convert MP3/WAV to WAV format 
def convert_to_wav(audio_path):
    if audio_path.endswith(".mp3"):
        sound = AudioSegment.from_mp3(audio_path)
        wav_path = audio_path.replace(".mp3", ".wav")
        sound.export(wav_path, format="wav")
        return wav_path
    elif audio_path.endswith(".webm"):
        sound = AudioSegment.from_file(audio_path, format="webm")
        wav_path = audio_path.replace(".webm", ".wav")
        sound.export(wav_path, format="wav")
        return wav_path
    return audio_path

# Function to convert audio to text
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    audio_file = convert_to_wav(audio_file)

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError as e:
            return f"Could not request results; {e}"

# Main execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide an audio file path")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    if not os.path.exists(audio_path):
        print(f"Error: File not found at {audio_path}")
        sys.exit(1)
        
    result = audio_to_text(audio_path)
    print(result)
