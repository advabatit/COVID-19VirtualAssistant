#import pyttsx3
from gtts import gTTS
import playsound
import os
import speech_recognition
import speech_recognition
from WebScapingCOVID19 import sort_info

goodbye = 'You are welcome. If you want to know more, you more than welcome to ask again. goodbye.'
no_question = 'I am waiting for you to aske me a question. '
no_question += "If you don't have any question, please say 'quit' or 'thank you'"
dont_know = "I am sorry but I think I don't know the answer. "
dont_know += "If you have another question I'd be happy to help." 

questions_and_answers = {}
possible_questions = [['what is coronavirus'],
                    ['symptoms of covid-19', 'symptoms of coronavirus', 'what symptoms'],
                    ['seriously ill', 'ill', 'having hard symptoms'],
                    ['who is most at risk', 'can i get sick', 'am i at risk'],
                    ['how can we be protected', 'how to protect'],
                    ['test for', 'when'],
                    ['what test sould i get', 'which test', 'having covid-19', 'having coronavirus'],
                    ['rapid test', 'fast test'],
                    ['had covid-19', 'had coronavirus'],
                    ['isolation', 'quarantine'],
                    ['exposed to', 'met with someone who has covid-19', 'met with someone who has coronavirus'],
                    ['when will i have symptoms', 'how long it will take to have symptoms'],
                    ['having symptoms', 'i have covid-19 symptoms', 'i have coronavirus symptoms'],
                    ['vaccine', 'cure', 'medication'],
                    ['treatments', 'how to deal with'],
                    ['antibiotic'],
                    ['thank you', 'quit'],
                    ['']]

''' Never judge anyone shortly. Every saint has a past and every sinner has a future. '''


def speak(text : str):
    """
    Function that speak the text it gets
    Args:
        text (str) : The text the function speak
    Return:
        Nothing
    """
    tts = gTTS(text=text, lang="en")
    filename = "sample2.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def get_audio():
    """
    Function that gets audio from the user and convert it to string
    Args:
        Nothing
    Return:
        returns a string of the user's audio
    """
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
    question = ''
    questions, answers, last_update = sort_info()
    init_dict(questions, answers)

    welcome = 'Welcome, I am Stella. I am going to answer to any question you have about the COVID-19. '
    welcome += 'All the informetion that I know is from the world health organization. '
    welcome += 'The last time the information was updated was: ' + last_update
    speak(welcome)
    flag = True

    while flag:
        question = get_audio()

        answer = get_answer(question)
        speak(answer)

        if 'thank you' in question or 'quit' in question:
            flag = False
        
def init_dict(questions, answers):
    """
    Function that initialize the dictionary with questions and answers
    Args:
        questions (list) and answers (list) we initialize in the dictionary
    Return:
        Nothing
    """
    i = 0
    for i, question in enumerate(questions):
        possible_questions[i].append(question.lower())
        questions_and_answers[tuple(possible_questions[i])] = answers[i]

    questions_and_answers[tuple(possible_questions[i+1])] = goodbye
    questions_and_answers[tuple(possible_questions[i+2])] = no_question
    questions_and_answers["don't know"] = dont_know

def get_answer(said : str) -> str:
    """
    Function that search the question in the dictionary and returns an answer
    Args:
        said (str): string that the user said
    Return:
        answer (str): returns the answer we will speak to the user
    """
    for questions in questions_and_answers.keys():
        for question in questions:
            if question in said:
                return questions_and_answers[questions]

    return questions_and_answers["don't know"]

if __name__ == '__main__':
    main()
