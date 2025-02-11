import openai
import speech_recognition as sr
import pyttsx3

# OpenAI API anahtarınızı buraya ekleyin
# Enter your OpenAI API key here
openai.api_key = "xxx"

def openai_chat(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # or gpt-4, etc.
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"An error occurred: {e}"

def listen_voice():
    """
    Mikrofondan sesi alır ve Google STT servisini kullanarak metne dönüştürür.
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("Listening... Please speak your question.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        # Dil ayarını ihtiyaçlarınıza göre değiştirebilirsiniz, örneğin "tr-TR" Türkçe için
        text = recognizer.recognize_google(audio, language="en-US")
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from speech recognition service; {e}")
    
    return None

def speak_text(text):
   
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # 1. Adım: Mikrofondan sesi alıp metne çevir.
    question = listen_voice()
    if question:
        # 2. Adım: OpenAI API'ye metin sorgusunu gönder ve yanıtı al.
        answer = openai_chat(question)
        print("Response from OpenAI:")
        print(answer)
        # 3. Adım: Alınan yanıtı sese dönüştürüp çal.
        speak_text(answer)
    else:
        print("No valid input was received.")
