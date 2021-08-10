from pynput.keyboard import Key, Listener
import pkb_client as pkbc

IP = "192.168.1.241"
PORT = 5560

class PKBSender():
    def __init__(self):
        self.commandKeysDown = set()
        self.keysDown = set()
        self.commandKeyMapping = {
            "ctrl":1,
            "shift":2,
            "alt": 4,
            "cmd": 8
        }
        self.keyMapping = {
            'a':4,
            'b':5,
            'c':6,
            'd':7,
            'e':8,
            'f':9,
            'g':10,
            'h':11,
            'i':12,
            'j':13,
            'k':14,
            'l':15,
            'm':16,
            'n':17,
            'o':18,
            'p':19,
            'q':20,
            'r':21,
            's':22,
            't':23,
            'u':24,
            'v':25,
            'w':26,
            'x':27,
            'y':28,
            'z':29,
            '1':30,
            '2':31,
            '3':32,
            '4':33,
            '5':34,
            '6':35,
            '7':36,
            '8':37,
            '9':38,
            '0':39,
            '!':30,
            '@':31,
            '#':32,
            '$':33,
            '%':34,
            '^':35,
            '&':36,
            '*':37,
            '(':38,
            ')':39,
            'enter':40,
            'esc':41,
            'backspace':42,
            'tab': 43,
            'space': 44,
            '-': 45,
            '_': 45,
            '=': 46,
            '+': 46,
            '[': 47,
            '{': 47,
            ']': 48,
            '}': 48,
            '\\\\\\\\': 49,
            '|': 49,
            ';': 51,
            ':': 51,
            '\'': 52,
            '"': 52,
            '`': 53,
            '~': 53,
            ',': 54,
            '<': 54,
            '.': 55,
            '>': 55,
            '/': 56,
            '?': 56,
            'f1':58,
            'f2':59,
            'f3':60,
            'f4':61,
            'f5':62,
            'f6':63,
            'f7':64,
            'f8':65,
            'f9':66,
            'f10':67,
            'f11':68,
            'f12':69,
            'home':74,
            'delete':75,
            'end':76,
            'right':79,
            'left':80,
            'down':81,
            'up':82,
        }

        self.client = pkbc.PKBClient(IP, PORT)
        self.client.connect()

    # Parse the sets and turn them into the List needed to send to the pi
    def generateKeyList(self):
        keyArray = [0,0,0,0,0,0,0,0]
        # Get sum of command keys for first slot
        for k in self.commandKeysDown:
            keyArray[0] += self.commandKeyMapping[k]
        # Fill remaining slots with keys
        for i in range(len(self.keysDown)):
            if i >= 6: break # max 6 keys
            key = list(self.keysDown)[i] # Set needs to be converted to list
            digit = self.keyMapping[key]
            keyArray[i+2] = digit

        return keyArray

    # Parse Key from raw event input
    def parseKey(self, key):
        key = str(key).replace("'", "").lower()
        key = key.replace('key.', '')
        return key

    def sendKeys(self):
        self.client.send({'key_press': self.generateKeyList()})

    def pressKey(self, key):
        key = self.parseKey(key)
        # Return if the key already exists
        if key in self.keysDown or key in self.commandKeysDown: return
        # Separate command keys from normal keys
        if key in self.commandKeyMapping.keys(): self.commandKeysDown.add(key)
        else: 
            if len(self.keysDown) >= 6: return # Max 6 keys at a time
            self.keysDown.add(key)

        self.sendKeys()

    def liftKey(self, key):
        key = self.parseKey(key)
        # Return if key doesn't exist to prevent errors
        if key not in self.keysDown and key not in self.commandKeysDown: return
        # Separate command keys from normal keys
        if key in self.commandKeyMapping.keys(): self.commandKeysDown.remove(key)
        else: self.keysDown.remove(key)

        self.sendKeys()

pkbSender = PKBSender()

with Listener(on_press=pkbSender.pressKey, on_release=pkbSender.liftKey) as listener:
    listener.join()



# TODO: switch between profiles
# TODO: cancel key presses when sending
# TODO: add a sound when switching

# TODO: figure out why running through console will not work