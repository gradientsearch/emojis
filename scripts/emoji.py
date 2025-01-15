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
    name: str


def getEmojiList():
    res = requests.get('https://unicode.org/emoji/charts/full-emoji-list.txt')
    with open('static/full-emoji-list.txt', 'w') as f:
        f.write(res.text)
        f.flush()
        os.fsync(f.fileno())

    res = requests.get('https://api.github.com/emojis')
    with open('static/emojis.json', 'w') as f:
        f.write(res.text)
        f.flush()
        os.fsync(f.fileno())


def printEmoji(name, unicode):
    with open(f'static/{name}', 'w') as f:
        f.write(unicode)
        f.flush()
        os.fsync(f.fileno())


def buildUnicodeMap():
    unicodeDescriptionList = []
    with open('scripts/full-emoji-list.txt', 'r') as file:
        unicodeDescriptionList = file.readlines()

    with open('scripts/unicodeMap.py', 'w') as f:
        f.write('UNICODE_MAP = {\n')

        for item in unicodeDescriptionList:
            item = item.strip()
            if len(item) == 0:
                continue

            if item.startswith('@@'):
                continue
            if item.startswith('@'):
                continue

            itemUnicodeDescription = item.split('\t')

            for v in itemUnicodeDescription[0].upper().split(' '):
                pad = 8 - len(v)
                code = f"\\U{''.join(['0'] * pad)}{v}"
                f.write(f'"{v}": "{code}",\n')

        f.write("}")


def buildEmojiMap():
    unicodeEmojiList = []
    with open('scripts/full-emoji-list.txt', 'r') as file:
        unicodeEmojiList = file.readlines()

    githubListWithNames = []
    with open('scripts/emojis.json', 'r') as file:
        githubListWithNames = json.load(file)

    githubNameUnicodeMap = {}
    for k in githubListWithNames:
        namedKey = githubListWithNames[k].split('/')[-1].replace('.png?v8', '')
        githubNameUnicodeMap[namedKey] = k

    emojisMap = {}
    currentCategory: str
    currentSubcategory: str

    for item in unicodeEmojiList:
        item = item.strip()
        if len(item) == 0:
            continue

        if item.startswith('@@'):
            currentCategory = item.replace('@@', '').lower()
            emojisMap[currentCategory] = {}
            continue
        if item.startswith('@'):
            currentSubcategory = item.replace('@', '').lower()
            emojisMap[currentCategory][currentSubcategory] = {}
            continue

        unicodeDescription = item.split('\t')

        emojiUnicode = ''
        githubUnicodeKey = ''  # <unicode>[-<unicode>[-<unidcode>]]
        for v in unicodeDescription[0].upper().split(' '):
            githubUnicodeKey += v.lower() + '-'
            emojiUnicode += unicodeMap.UNICODE_MAP[v]

        # remove last -
        githubUnicodeKey = githubUnicodeKey[:-1]

        e = Emoji()
        e.category = currentCategory
        e.subcategory = currentSubcategory
        e.emoji = emojiUnicode
        e.unicode = githubUnicodeKey
        e.description = unicodeDescription[1]

        # skip emoji if its not in the github list
        if githubUnicodeKey in githubNameUnicodeMap:
            e.name = githubNameUnicodeMap[githubUnicodeKey]
        else:
            continue

        emojisMap[currentCategory][currentSubcategory][e.name] = {
            'name': e.name,
            'category': e.category,
            'subcategory': e.subcategory,
            'emoji': f'{e.emoji}',
            'unicode': e.unicode,
            'description': e.description
        }

        printEmoji(e.name, e.emoji)

    # Note the unicode chars will be encoded
    with open('static/emojis.json', 'w') as f:
        json.dump(emojisMap, f)


def main():
    # uncomment this if you need to rebuild the unicode map.
    # Can't create unicode strings dynamically.
    # buildUnicodeMap()
    buildEmojiMap()


if __name__ == '__main__':
    main()
