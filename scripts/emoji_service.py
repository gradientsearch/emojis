import requests
import json 
import os
import unicodeMap
class Emoji:
    unicode: str 
    category: str
    subcategory: str
    description: str
    emoji: str

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
        
def buildUnicodeMap(): 
    list1 = []
    with open('scripts/full-emoji-list.txt', 'r') as file:
        list1 = file.readlines()
    
    
    with open('scripts/unicodeMap.py', 'w') as f:
        
        f.write(" UNICODE_MAP = {\n")
        
        for l in list1:
            l = l.strip()
            if len(l) == 0:
                continue
            
            if l.startswith('@@'):
                currentCategory=l.replace('@@','').lower()
                continue
            if l.startswith('@'):
                currentSubcatgory = l.replace('@','').lower()
                continue
            
            
            
            ls = l.split('\t')

            
            
            for v in ls[0].upper().split(' '):
                #if len()
                code = f"\\U000{v}"
                f.write(f'"{v}": "{code}",\n')
        f.write("}")

def buildEmojiMap(): 
    list1 = []
    with open('scripts/full-emoji-list.txt', 'r') as file:
        list1 = file.readlines()
    
    list2 = []
    with open('scripts/emojis.json', 'r') as file:
        list2 = json.load(file)
    #print(list)
    #print(list2)
    
    currentCategory: str
    currentSubcatgory: str

    
    for l in list1:
        l = l.strip()
        if len(l) == 0:
            continue
        
        if l.startswith('@@'):
            currentCategory=l.replace('@@','').lower()
            continue
        if l.startswith('@'):
            currentSubcatgory = l.replace('@','').lower()
            continue
        
        
        
        ls = l.split('\t')

        
        
        for v in ls[0].upper().split(' '):
            code = unicodeMap.UNICODE_MAP[v]
            print(code)
        
        desc = ls[1]
        
        
      #  print((code, desc))
        


def main():
    buildEmojiMap()
    #buildUnicodeMap()

if __name__ == '__main__':
    main()