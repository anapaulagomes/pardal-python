from pardal import templates
from pardal.keyboard import KeyboardConfiguration
from pardal.speaking import say
from pynput import keyboard


class HomeTimeline:
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.data = api.get_home_timeline()
        self.cursor = 0
        self._current_active_modifiers = set()
        self.keyboard = KeyboardConfiguration().set_hotkeys()

    def read(self):
        tweet = self.data[self.cursor]
        formatted_tweet = templates.tweet(tweet)
        print(formatted_tweet, self.cursor)
        say(formatted_tweet)

    def up(self):
        if self.cursor < 0:
            say('End of new tweets in your timeline.')
        else:
            self.cursor = self.cursor - 1
            self.read()

    def down(self):
        if self.cursor == len(self.data) - 1:
            say('End of your timeline.')
        else:
            self.cursor = self.cursor + 1
            self.read()

    def listen(self):
        def pressed_current_modifiers_on(modifiers):
            return all(
                key in self._current_active_modifiers
                for key in modifiers
            )

        def on_press(key):
            if key in self.keyboard.up:
                self._current_active_modifiers.add(key)
                if pressed_current_modifiers_on(self.keyboard.up):
                    self.up()

            if key in self.keyboard.down:
                self._current_active_modifiers.add(key)
                if pressed_current_modifiers_on(self.keyboard.down):
                    self.down()

            if key == keyboard.Key.esc:
                listener.stop()

        def on_release(key):
            try:
                self._current_active_modifiers.remove(key)
            except KeyError:
                pass

        with keyboard.Listener(
                on_press=on_press, on_release=on_release) as listener:
            listener.join()


# FIXME ImportError: You must be root to use this library
