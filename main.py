import speech_recognition
from datetime import datetime
from os.path import isfile
from playsound import playsound
import requests


texts = [
    "Assalomu aleykum",
    "Salom",
    "Hayr",
    "Xayr",
    "Siz qachondan beri o'zingizni yomon his qilayapsiz?",
    "Mazzam bo'lmayapti",
    "Mazzam bo'lmadi",
    "Mazzam bo'madi",
    "Mazam bo'madi",
    "Mazam bo'lmadi",
    "Mazam bo'lmayapti"
    "Tishim og'riyapti",
    "Tishim og'ridi",
    "Bir hafta",
    "Uch kun",
    "Bir kun",
    "2-3 soat"
]
global illness
illness = False
global tooth
tooth = False
recognizer = speech_recognition.Recognizer()
micro = speech_recognition.Microphone()


def loader():
    if not isfile("voices/greeting.wav"):
        request = requests.get(
            "https://internal.nutq.uz/api/v1/cabinet/synthesize/",
            params={
                't': "Assalomu aleykum, Qadrli foydalanuvchi!\n\t\tSizga qanday yordam berolaman?"
            }
        )
        filename = "voices/greeting.wav"
        with open(filename, "wb") as file:
            file.write(request.content)
    if not isfile("voices/greeting-min.wav"):
        request = requests.get(
            "https://internal.nutq.uz/api/v1/cabinet/synthesize/",
            params={
                't': "Sizga qanday yordam berolaman?"
            }
        )
        filename = "voices/greeting-min.wav"
        with open(filename, "wb") as file:
            file.write(request.content)
    if not isfile("voices/thinking.wav"):
        request = requests.get(
            "https://internal.nutq.uz/api/v1/cabinet/synthesize/",
            params={
                't': "O'ylab olay"
            }
        )
        filename = "voices/thinking.wav"
        with open(filename, "wb") as file:
            file.write(request.content)
    if not isfile("voices/retry.wav"):
        request = requests.get(
            "https://internal.nutq.uz/api/v1/cabinet/synthesize/",
            params={
                't': "Boshqattan gapiring"
            }
        )
        filename = "voices/retry.wav"
        with open(filename, "wb") as file:
            file.write(request.content)
    if not isfile("voices/goodbye.wav"):
        request = requests.get(
            "https://internal.nutq.uz/api/v1/cabinet/synthesize/",
            params={
                't': "Salomat bo'ling"
            }
        )
        filename = "voices/goodbye.wav"
        with open(filename, "wb") as file:
            file.write(request.content)
    if not isfile("voices/illness.wav"):
        request = requests.get(
            "https://internal.nutq.uz/api/v1/cabinet/synthesize/",
            params={
                't': "Siz qachondan beri o'zingizni yomon his qilayapsiz?"
            }
        )
        filename = "voices/illness.wav"
        with open(filename, "wb") as file:
            file.write(request.content)
        


def speaker(question):
    if question == "Assalomu aleykum, Qadrli foydalanuvchi!\n\t\tSizga qanday yordam berolaman?":
        playsound("voices/greeting.wav")
    elif question == "Sizga qanday yordam berolaman?":
        playsound("voices/greeting-min.wav")
    elif question == "O'ylab olay":
        playsound("voices/thinking.wav")
    elif question == "Boshqattan gapiring":
        playsound("voices/retry.wav")
    elif question == "Salomat bo'ling":
        playsound("voices/goodbye.wav")
    elif question == "Siz qachondan beri o'zingizni yomon his qilayapsiz?":
        playsound("voices/illness.wav")
    else:
        request = requests.get(
            "https://internal.nutq.uz/api/v1/cabinet/synthesize/",
            params={
                't': question
            }
        )
        filename = f"voices/{datetime.now().strftime('%Y-%m-%d.%H-%M-%S')}.wav"
        with open(filename, "wb") as file:
            file.write(request.content)
        # tts.save(filename)
        playsound(filename)


def listener(question):
    with micro:
        recognizer.adjust_for_ambient_noise(micro)
        print(f"Aqlli doktor:\t{question}")
        speaker(question)
        if question in ["Assalomu aleykum, Qadrli foydalanuvchi!\n\t\tSizga qanday yordam berolaman?", "Sizga qanday yordam berolaman?"]:
            print("1) Mazzam bo'lmayapti\n2) Tishim og'riyapti")
        elif question in ["Siz qachondan beri o'zingizni yomon his qilayapsiz?", "Qachondan beri tishingiz bezovta qilmoqda?"]:
            print("1) Bir hafta\n2) Uch kun\n3)Bir kun\n4) 2-3 soat")
        audio = recognizer.listen(micro, phrase_time_limit=3)
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
    global illness
    global tooth
    if answer in ["Hayr", "Xayr"]:
        print("Aqlli doktor:\tSalomat bo'ling")
        speaker("Salomat bo'ling")
        return
    elif answer in ["Assalomu aleykum", "Salom"]:
        main(listener("Sizga qanday yordam berolaman?"), "Sizga qanday yordam berolaman?")
    elif answer in ["Mazzam bo'lmayapti", "Mazzam bo'lmadi", "Mazzam bo'madi", "Mazam bo'madi", "Mazam bo'lmadi", "Mazam bo'lmayapti"]:
        main(listener("Siz qachondan beri o'zingizni yomon his qilayapsiz?"), "Siz qachondan beri o'zingizni yomon his qilayapsiz?")
        illness = True
    elif answer in ["Tishim og'riyapti", "Tishim og'ridi"]:
        main(listener("Qachondan beri tishingiz bezovta qilmoqda?"), "Qachondan beri tishingiz bezovta qilmoqda?")
        tooth = True
    elif answer in ["Bir hafta", "Uch kun", "Bir kun", "2-3 soat"]:
        if illness:
            main(listener("Biz sizni terapevtimiz bilan bog'laymiz\n\t\tSog'ligizni asrang"), "Biz sizni terapevtimiz bilan bog'laymiz\n\t\tSog'ligizni asrang")
        elif tooth:
            main(listener("Biz sizni terapevtimiz bilan bog'laymiz\n\t\tSog'ligizni asrang"), "Biz sizni terapevtimiz bilan bog'laymiz\n\t\tSog'ligizni asrang")
        return
    elif answer == "Aqlli doktor:\tBoshqattan gapiring":
        print(answer)
        speaker("Boshqattan gapiring")
        main(listener(previous_question), previous_question)
    elif answer == "":
        main(listener("Assalomu aleykum, Qadrli foydalanuvchi!\n\t\tSizga qanday yordam berolaman?"), "Assalomu aleykum, Qadrli foydalanuvchi!\n\t\tSizga qanday yordam berolaman?")
    else:
        print(answer)

if __name__ == "__main__":
    loader()
    main()
