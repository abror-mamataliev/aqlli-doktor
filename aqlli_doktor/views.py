# # import speech_recognition as sr
# # recognizer = sr.Recognizer()
# # audio_file_ = sr.AudioFile("voices/AwACAgEAAxkBAAEB5jJgOcyXUveraJ6l1UBp_xyvoh4FtgACLQEAAhRt0UVSZEIwIVrI3B4E.wav")
# # with audio_file_ as source:
# #     audio_file = recognizer.record(source)
# #     result = recognizer.recognize_google(audio_data=audio_file, language="uz")
# #     print(result)

# import pyaudio
# import wave
# import speech_recognition

# chunk = 1024  # Record in chunks of 1024 samples
# sample_format = pyaudio.paInt16  # 16 bits per sample
# channels = 2
# fs = 44100  # Record at 44100 samples per second
# seconds = 3
# filename = "output.wav"

# p = pyaudio.PyAudio()  # Create an interface to PortAudio

# print('Recording')

# stream = p.open(format=sample_format,
#                 channels=channels,
#                 rate=fs,
#                 frames_per_buffer=chunk,
#                 input=True)

# frames = []  # Initialize array to store frames

# # Store data in chunks for 3 seconds
# for i in range(0, int(fs / chunk * seconds)):
#     data = stream.read(chunk)
#     frames.append(data)

# # Stop and close the stream
# stream.stop_stream()
# stream.close()
# # Terminate the PortAudio interface
# p.terminate()

# print('Finished recording')

# # Save the recorded data as a WAV file
# wf = wave.open(filename, 'wb')
# wf.setnchannels(channels)
# wf.setsampwidth(p.get_sample_size(sample_format))
# wf.setframerate(fs)
# wf.writeframes(b''.join(frames))
# wf.close()

# recognizer = speech_recognition.Recognizer()
# audio_file_ = speech_recognition.AudioFile("output.wav")
# with audio_file_ as source:
#     audio_file = recognizer.record(source)
#     result = recognizer.recognize_google(audio_data=audio_file, language="ru")
#     # print(result)

# import speech_recognition

# recognizer = speech_recognition.Recognizer()
# micro = speech_recognition.Microphone()
# with micro:
#     recognizer.adjust_for_ambient_noise(micro, duration=5)

#     # while True:
#     audio = recognizer.listen(micro, phrase_time_limit=2)
#     print(audio)

#     speech = recognizer.recognize_google(audio, language='ru', show_all=True)

#     print('Você disse: ', speech)

from flask import render_template

from .forms import *
from . import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/auth/login")
def login():
    return render_template("login.html")


@app.route("/assistant")
def assistant():
    return render_template("assistant.html")
