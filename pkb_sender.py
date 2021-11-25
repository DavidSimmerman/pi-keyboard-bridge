import keyboard
import winsound

import pkb_client as pkbc

IP = "192.168.1.241"
PORT = 5560

SOUND_PATH = './pi-keyboard-bridge/sounds/'

class PKBSender():
    def __init__(self):
        self.is_active = False
        self.command_keys_down = set()
        self.keys_down = set()
        self.HOTKEYS_LIST = ('f24','s')
        self.COMMAND_KEY_MAPPING = {
            "ctrl":1,
            "shift":2,
            "alt": 4,
            "cmd": 8
        }
        self.KEY_MAPPING = {
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
            '\\': 49,
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

        # Setup Hotkey
        self.HOTKEYS_STRING = '+'.join(self.HOTKEYS_LIST)
        keyboard.add_hotkey(self.HOTKEYS_STRING, self.activate_sender, suppress=True, trigger_on_release=True)

        # Connect to client
        self.client = pkbc.PKBClient(IP, PORT)
        self.client.connect()

    def get_all_keys_down(self):
        return list(self.keys_down)+list(self.command_keys_down)

    def activate_sender(self):
        if self.is_active == True: return
        self.is_active = True
        self.active_hook = keyboard.hook(self.send_key, suppress=True)
        winsound.PlaySound(SOUND_PATH+'low_swoosh.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        print("ACTIVATED")
    
    def deactivate_sender(self):
        self.is_active = False
        keyboard.unhook(self.active_hook)
        winsound.PlaySound(SOUND_PATH+'high_swoosh.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
        print("DEACTIVATED")

    def send_key(self, event):
        key = event.name.lower()
        if event.event_type == 'down':
            # Return if they key already exists
            if key in self.keys_down or key in self.command_keys_down: return
            # Separate command keys from normal keys
            if key in self.COMMAND_KEY_MAPPING.keys(): self.command_keys_down.add(key)
            else:
                if len(self.keys_down) >= 6: return # Max 6 keys at a time
                self.keys_down.add(key)
        elif event.event_type == 'up':
            # Return if key doesn't exist to prevent errors
            if key not in self.keys_down and key not in self.command_keys_down: return
            # Separate command keys from normal keys
            if key in self.COMMAND_KEY_MAPPING.keys(): self.command_keys_down.remove(key)
            else: self.keys_down.remove(key)
        else: return

        # Check if the only keys that are down are the hotkey keys
        if all(k in self.get_all_keys_down() for k in self.HOTKEYS_LIST) and len(self.get_all_keys_down()) == len(self.HOTKEYS_LIST):
            self.command_keys_down = set()
            self.keys_down = set()
            self.deactivate_sender()
        print(self._generate_key_list())
        self.client.send({'key_press': self._generate_key_list()})

     # Parse the sets and turn them into the List needed to send to the pi
    def _generate_key_list(self):
        key_array = [0,0,0,0,0,0,0,0]
        # Get sum of command keys for first slot
        for k in self.command_keys_down:
            key_array[0] += self.COMMAND_KEY_MAPPING[k]
        # Fill remaining slots with keys
        for i in range(len(self.keys_down)):
            if i >= 6: break # max 6 keys
            key = list(self.keys_down)[i] # Set needs to be converted to list
            if key not in self.KEY_MAPPING.keys():
                print("UNDEFINED KEY: " + key)
                winsound.PlaySound(SOUND_PATH+'bad_key.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
                continue
            digit = self.KEY_MAPPING[key]
            key_array[i+2] = digit

        return key_array

    # Parse Key from raw event input
    def _parse_key(self, key):
        key = str(key).replace("'", "").lower()
        key = key.replace('key.', '')
        return key

pkb_sender = PKBSender()
keyboard.wait()


# TODO: add a sound when switching