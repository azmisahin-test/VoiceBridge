import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import time

# Uygulama ayarları
MIC_INDEX = 3  # Mikrofon indeksi
SPEECH_RATE = 150  # Konuşma hızı
VOLUME_LEVEL = 1  # Ses seviyesi

# TTS için pyttsx3'i başlat
engine = pyttsx3.init()
engine.setProperty('rate', SPEECH_RATE)
engine.setProperty('volume', VOLUME_LEVEL)

def speak(text):
    """Metni sesli olarak okur."""
    engine.say(text)
    engine.runAndWait()
    time.sleep(1)  # Bekleme süresi

def recognize_and_translate():
    """Ses tanıma ve çeviri işlemlerini gerçekleştirir."""
    recognizer = sr.Recognizer()
    translator = Translator()

    # Ortam gürültüsüne ayar yapma
    with sr.Microphone(device_index=MIC_INDEX) as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

    while True:
        try:
            with sr.Microphone(device_index=MIC_INDEX) as source:
                print("Please say something...")
                print("Listening...")
                
                # Ses kaydetme ve zaman aşımı kontrolü
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            # Ses kaydını metne çevir
            start_recognition = time.time()
            recognized_text = recognizer.recognize_google(audio, language="en-US")
            recognition_time = time.time() - start_recognition
            print("Recognized text:", recognized_text)
            print(f"Recognition time: {recognition_time:.2f} seconds.")

            # Metni Türkçeye çevir
            start_translation = time.time()
            translated_text = translator.translate(recognized_text, dest='tr').text
            translation_time = time.time() - start_translation
            print("Translated text:", translated_text)
            print(f"Translation time: {translation_time:.2f} seconds.")

            # Çevirilen metni sesli hale getir ve oynat
            speak(translated_text)

            # Dinleme döngüsüne geçiş yapmadan önce kısa bir bekleme süresi
            time.sleep(0.5)

        except sr.UnknownValueError:
            print("Could not understand audio: Possibly due to background noise or unclear speech.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    recognize_and_translate()
