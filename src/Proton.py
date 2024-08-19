import eel
import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import app
from threading import Thread

# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status

# ------------------Functions----------------------
@eel.expose
def addAppMsg(message):
    app.eel.addProtonMsg(message)

def reply(audio):
    addAppMsg(f"Proton: {audio}")
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
    reply("I am Proton, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:
    r.energy_threshold = 500 
    r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)
        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry, my service is down. Please check your Internet connection.')
        except sr.UnknownValueError:
            print('Cannot recognize')
            pass
        return voice_data.lower()

# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data = voice_data.replace('proton', '')
    app.eel.addUserMsg(f"User: {voice_data}")

    if not is_awake:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Proton!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        search_query = voice_data.split('search')[1]
        reply('Searching for ' + search_query)
        url = 'https://google.com/search?q=' + search_query
        try:
            webbrowser.get().open(url)
            reply('This is what I found.')
        except Exception as e:
            reply('Please check your Internet.')
            print(f"Error: {e}")

    elif 'location' in voice_data:
        reply('Which place are you looking for?')
        temp_audio = record_audio()
        app.eel.addUserMsg(f"User: {temp_audio}")
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found.')
        except Exception as e:
            reply('Please check your Internet.')
            print(f"Error: {e}")

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Goodbye! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        app.ChatBot.close()
        sys.exit()

    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter += 1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory.')
        app.eel.addAppMsg(f"Proton: {filestr}")
        
    elif file_exp_status:
        counter = 0   
        if 'open' in voice_data:
            try:
                file_index = int(voice_data.split(' ')[-1]) - 1
                if isfile(join(path, files[file_index])):
                    os.startfile(join(path, files[file_index]))
                    file_exp_status = False
                else:
                    path = join(path, files[file_index]) + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter += 1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully.')
                    app.eel.addAppMsg(f"Proton: {filestr}")
            except Exception as e:
                reply('You do not have permission to access this folder.')
                print(f"Error: {e}")

        elif 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory.')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter += 1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok.')
                app.eel.addAppMsg(f"Proton: {filestr}")

    else: 
        reply('I am not programmed to do this!')

# ------------------Driver Code--------------------
# Start ChatBot in a separate thread
t1 = Thread(target=app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        # Take input from GUI
        voice_data = app.ChatBot.popUserInput()
    else:
        # Take input from Voice
        voice_data = record_audio()

    # Process voice_data
    if 'proton' in voice_data:
        try:
            # Handle sys.exit()
            respond(voice_data)
        except SystemExit:
            reply("Exit Successful")
            break
        except Exception as e:
            print(f"EXCEPTION raised while closing: {e}")
            break
