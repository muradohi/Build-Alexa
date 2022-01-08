import os
import speech_recognition as sr
import pyttsx3
import datetime
import re
from auto2 import find_about

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

find_online = find_about()


def formatted_songs(song_list):
    all_songs = ','.join(song_list)

    pattern1 = re.compile(r"\([^()]*\)")
    string1 = pattern1.sub(r'', all_songs)
    pattern2 = re.compile(r"[^a-zA-Z0-9.,\s]+")
    string2 = pattern2.sub(r' ', string1)

    string3 = string2.replace('.mp3', '')
    string3 = string3.lower()

    string4 = string3.replace('  ', ' ')
    string5 = string4.split(',')

    string6 = list(enumerate(string5))

    return string6


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_cmd():
    try:
        with sr.Microphone() as src:
            print('listening...')
            voice = listener.listen(src)
            cmd = listener.recognize_google(voice)
            cmd = cmd.lower()
            if 'alexa' in cmd:
                cmd = cmd.replace('alexa', '')

                print(cmd)

    except:
        print("can't listen")
        talk('cannot listen')
        exit()

    return cmd


if __name__ == '__main__':
    clear = lambda: os.system('cls')

    # This Function will clean any cmd
    clear()


def run_alexa():
    global final_song
    cmd = take_cmd()
    try:
        if 'play' in cmd or 'on youtube' in cmd:
            song = cmd.replace('play', '')
            talk('playing' + song)
            print('playing' + song)
            song2 = song.replace('on youtube', '')
            find_online.youtube_song(song2)

        if 'search' in cmd and 'on youtube' in cmd:
            song = cmd.replace('search', '')
            talk('playing' + song)
            print('playing' + song)
            song2 = song.replace('on youtube', '')
            find_online.youtube_song(song2)


        elif 'time now' in cmd:
            time = datetime.datetime.now().strftime('%I:%M %p')
            now = datetime.datetime.now()
            hour = now.hour
            if hour >= 0 and hour <= 6:
                talk('hello you should sleep now because')
            elif hour > 6 and hour <= 12:
                talk('hello good morning')
            elif hour > 12 and hour <= 18:
                talk('hello good afternoon')
            else:
                talk('hello good night')
            print(time)
            talk('it is' + time)

        elif 'who is' in cmd:
            person = cmd.replace('who is', '')
            person = person.replace('wikipedia', '')
            info = find_online.search_wiki(person)
            print(info)
            talk(info)
        elif 'search about' and 'on wikipedia' in cmd:
            person = cmd.replace('search about', '')
            person = person.replace('on wikipedia', '')
            info = find_online.search_wiki(person)
            print(info)
            talk(info)

        elif 'what is the weather now' in cmd or 'what is the weather in' in cmd or 'what is the weather at' in cmd or 'weather now' in cmd:
            info = find_online.search_weather(cmd)
            print(info)
            talk(info)

        elif 'what is' in cmd:
            cmd = cmd.replace('find about', '')
            info = find_online.chrome_search(cmd)
            print(info)
            talk(info)

        elif 'from my playlist play' in cmd:
            song = cmd.replace('from my playlist play', '')
            song = str.strip(song)
            print(song)
            talk("from my playlist playing" + song)
            music_dir = "F:\music"
            songs = os.listdir(music_dir)
            print(songs)
            fm = formatted_songs(songs)
            print(fm)
            for idx, sng in fm:
                if song in sng:
                    i = idx
                    print(i)
                    final_song = songs[i]
                    print(final_song)
            random = os.startfile(os.path.join(music_dir, final_song))
            print(random)



        elif 'start game' in cmd:
            talk('starting valorant')
            path = 'E:\Valorant Files\Riot Games\Riot Client'
            files = os.listdir(path)
            os.startfile(os.path.join(path, files[3]))




        elif 'stop' or 'shutup' in cmd:

            find_online.close_window()
            # exit()


    except:
        talk('closing')


while True:
    run_alexa()
