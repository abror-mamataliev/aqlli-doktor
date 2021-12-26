import speech_recognition
from gtts import gTTS
from datetime import datetime
from playsound import playsound
import requests


texts = [
    "Assalomu aleykum",
    "Salom",
    "Hayr",
    "Xayr"
]
recognizer = speech_recognition.Recognizer()
micro = speech_recognition.Microphone()


def speaker(question):
    # tts = gTTS(question, lang="tr")
    request = requests.get(
        "https://internal.nutq.uz/api/v1/cabinet/synthesize/",
        params={
            't': question
        }
    )
    filename = "voices/"+ datetime.now().strftime('%Y-%m-%d.%H:%M:%S') + ".wav"
    print(type(filename))
    with open(filename, "wb") as file:
        file.write(request.content)
    # tts.save(filename)
    playsound(filename)


def listener(question):
    with micro:
        recognizer.adjust_for_ambient_noise(micro, duration=5)
        print(f"Aqlli doktor:\t{question}")
        speaker(question)
        audio = recognizer.listen(micro, phrase_time_limit=2)
        print("Aqlli doktor:\tO'ylab olay")
        speaker("O'ylab olay")
        speech = recognizer.recognize_google(audio, language='uz', show_all=True)
    if speech != []:
        transcripts = speech['alternative']
        for transcript in transcripts:
            if 'confidence' in transcript:
                text = transcript['transcript'].capitalize()
                print(f"Foydalanuvchi:\t{text}")
                if text in texts:
                    return text
                else:
                    return "Aqlli doktor:\tBoshqattan gapiring"
        return ""
    else:
        return "Aqlli doktor:\tBoshqattan gapiring"

def main(answer="", previous_question=""):
    if answer in ["Hayr", "Xayr"]:
        print("Aqlli doktor:\tSalomat bo'ling")
        speaker("Salomat bo'ling")
        return
    elif answer in ["Assalomu aleykum", "Salom"]:
        main(listener("Sizga qanday yordam berolimiz?"), "Sizga qanday yordam berolimiz?")
    elif answer in ["Aziza"]:
        main(listener("Aziza yaxshi qiz"), "Aziza yaxshi qiz")
    elif answer == "Aqlli doktor:\tBoshqattan gapiring":
        print(answer)
        speaker("Boshqattan gapiring")
        main(listener(previous_question), previous_question)
    elif answer == "":
        main(listener("Assalomu aleykum, Qadrli foydalanuvchi!\n\t\tSizga qanday yordam berolimiz?"), "Assalomu aleykum, Qadrli foydalanuvchi!\n\t\tSizga qanday yordam berolimiz?")
    else:
        print(answer)

if __name__ == "__main__":
    main()
