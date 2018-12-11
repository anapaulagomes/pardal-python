import os
import pyttsx3
import sys


engine = pyttsx3.init()


def say(message):
    # FIXME it seems there is a problem when running on MacOS
    # catch exception and try gTTS
    if sys.platform == 'darwin':
        os.system(f'say "{message}"')
    else:
        engine.say(message)
        engine.runAndWait()
