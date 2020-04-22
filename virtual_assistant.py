#virtual assistance program 

#pip install pipwin
#pipwin install pyaudio

#pip install SpeechRecognition 
#pip install gTTS
#pip install wikipedia


import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia


#ignore any warning messages
warnings.filterwarnings('ignore')

#record audio and return it as string
def recordAudio():
    #record the audio
    r = sr.Recognizer()
    #open the mic and start recording
    with sr.Microphone() as source:
        print('Say something')
        audio = r.listen(source)

    #use google speech recognition
    data  = ''
    try:
        data = r.recognize_google(audio)
        print(f'You said: {data}' )
    except sr.UnknownValueError: #check for unknown error
        print('Google speech recognition cannot understand')
    except sr.RequestError as e:
        print(f'Requests error {e}')
    
    return data

#recordAudio()

#Virtual assistant response
def assistantResponse(text):
    print (text)
    #Convert the text to speech
    myobj = gTTS(text=text, lang='en', slow=False)

    #save the converted audio
    myobj.save('assistant_response.mp3')

    #play the converted file
    os.system('start assistant_response.mp3')

#assistantResponse(text)

#magic word

def wakeWord(text):
    WAKE_WORDS = ['hey computer','ok computer']

    text = text.lower()

    #check if user command contains wakeword
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    return False

#get the current date
def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']

    #get ordina numbers
    ordinalNumbers = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11','12th',
                    '13th','14th','15th','16th','17th','18th','19th','20th','21st','22nd','23rd','24th',
                    '25th','26th','27th','28th','29th','30th','31st']

    return f'Today is {weekday} {month_names[monthNum - 1]} the {ordinalNumbers[dayNum - 1]}'

#random greeting response

def greeting(text):
    GREETING_INPUTS = ['yo','hola','zup']

    GREETING_REPONSE = ['yes','hello friend', 'hallo friend']

    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_REPONSE)
    return ''

def getPerson(text):
    wordList = text.split()

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]

while True:
    # Record the audio
    text = recordAudio()
    response = '' #Empty response string
     
    # Checking for the wake word/phrase
    if (wakeWord(text) == True):
         # Check for greetings by the user
        response = response + greeting(text)
         # Check to see if the user said date
        if ('date' in text):
            get_date = getDate()
            response = response + ' ' + get_date
         # Check to see if the user said time
        if('time' in text):
            now = datetime.datetime.now()
            meridiem = ''
            if now.hour >= 12:
                meridiem = 'p.m' #Post Meridiem (PM)
                hour = now.hour - 12
            else:
                meridiem = 'a.m'#Ante Meridiem (AM)
                hour = now.hour
           # Convert minute into a proper string
                if now.minute < 10:
                    minute = '0'+str(now.minute)
                else:
                    minute = str(now.minute)
                    response = response + ' '+ 'It is '+ str(hour)+ ':'+minute+' '+meridiem+' .'
                
        # Check to see if the user said 'who is'
        if ('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)            
            response = response + ' ' + wiki

       # Assistant Audio Response
        assistantResponse(response)
