# coding=utf-8
from random import shuffle
import pyttsx3


engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 125)

volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)

a=ord('a')
letter=[chr(i) for i in range(a,a+26)]

shuffle(letter)

# interval=7
# slow=','*interval
# msg = slow.join(letter)
# print(msg)



#voiceid = engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

num=3
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
for c in letter:
    for j in range(num):
        engine.say(c)
        engine.runAndWait()

engine.stop()
