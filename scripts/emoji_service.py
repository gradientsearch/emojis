import requests
import json 
import os



def getEmojiList():
    
    res = requests.get('https://unicode.org/emoji/charts/full-emoji-list.txt')

    with open('static/full-emoji-list.txt', 'w') as f:
        f.write(res.text)
        f.flush()
        os.fsync(f.fileno())

def printEmoji():
    with open('static/grinning', 'w') as f:
        f.write("\U0001F601")
        f.flush()
        os.fsync(f.fileno())
        
printEmoji()