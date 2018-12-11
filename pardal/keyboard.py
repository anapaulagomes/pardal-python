import configparser
from pynput import keyboard


keyboard_mapping = {
    'command': keyboard.Key.cmd,
    'windows': keyboard.Key.cmd,
    'up': keyboard.Key.up,
    'down': keyboard.Key.down,
    'ctrl': keyboard.Key.ctrl,
    'esc': keyboard.Key.esc,
}


def string_to_hotkeys(string):
    """Convert a hotkey string to a tuple of Key objects."""
    combination = []
    string_keys = string.replace(' ', '').split('+')
    for string_key in string_keys:
        key = keyboard_mapping.get(string_key)
        if key:
            combination.append(key)
        else:
            raise KeyNotFound

    return set(combination)


class KeyNotFound(Exception):
    pass


class KeyboardConfiguration:
    def __init__(self):
        self._config = self.read_config()

    def read_config(self):
        config = configparser.ConfigParser(
            {
                'up': 'alt+up+windows',
                'down': 'alt+down+windows',
                'exit': 'esc',
            }
        )
        config.read('keyboard.ini.sample')
        return config

    def set_hotkeys(self):
        for option in self._config.options('general'):
            string_hotkey = self._config.get('general', option)
            setattr(self, option, string_to_hotkeys(string_hotkey))
            print(option, string_to_hotkeys(string_hotkey))
        return self
