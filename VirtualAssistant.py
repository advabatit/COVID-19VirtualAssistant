import playsound
import speech_recognition
from gtts import gTTS
from WebScapingCOVID19 import sort_info

def speak(text : str, n : int):
    tts = gTTS(text = text, lang='en')
    file_name = 'voice' + str(n) + '.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)

def get_audio():
    print("You can speak now!")
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print('You said: ', said)
        except Exception as e:
            print("Exception is: " + str(e))

    return said.lower()

def main():
    n = 0
    question = ''
    questions, answers, last_update = sort_info()
    welcome = 'Welcome, I am Stella. I am going to answer to any question you have about the COVID-19.'
    welcome += 'All the informetion that I know is from the world health organization.'
    welcome += 'The last time the information was updated was: ' + last_update
    
    speak(welcome, n)    

    while not 'thank you' in question or not 'quit' in question:
        n += 1
        question = get_audio()

        if question == questions[0].lower() or ('covid-19' in question and 'what is' in question):
            speak(answers[0].lower(), n)

        elif question == questions[1].lower() or ('covid-19 symptomes' in question) or ('symptoms' in question):
            speak(answers[1].lower(), n)
        
        elif question == question[2].lower() or ('get ill' in question) or ('seriously ill' in question):
            speak(answers[2].lower(), n)
        
        elif  question == question[3].lower() or 'who is in risk' in question or 'severe illness' in question or 'risk' in question:
            speak(answers[3].lower(), n)

        elif question == "":
            no_question = 'I am waiting for you to aske me a question.'
            no_question += "If you don't have any question, please say 'quit' or 'thank you'" 
            speak(no_question, n)
        else:
            dont_know = "I am sorry but I think I don't know the answer."
            dont_know += "If you have another question I'd be happy to help." 
            speak(dont_know, n)
        

if __name__ == '__main__':
    main()