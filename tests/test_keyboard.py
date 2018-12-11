from pynput import keyboard
import pytest
from pardal.keyboard import (
    string_to_hotkeys, KeyNotFound, KeyboardConfiguration
)


@pytest.mark.parametrize('string,expected_object', [
    ('command+up', {keyboard.Key.cmd, keyboard.Key.up}),
    ('windows+up', {keyboard.Key.cmd, keyboard.Key.up}),
    ('command + up + ctrl', {
        keyboard.Key.cmd, keyboard.Key.up, keyboard.Key.ctrl}),
    ('ctrl', {keyboard.Key.ctrl})
])
def test_returns_key_objects_from_string(string, expected_object):
    assert string_to_hotkeys(string) == expected_object


def test_throw_exception_if_key_not_found():
    with pytest.raises(KeyNotFound):
        string_to_hotkeys('random')


class TestKeyboardConfiguration:
    def test_convert_config_into_key_objects(self):
        keyboard_config = KeyboardConfiguration()

        assert keyboard_config._config

        keyboard_config.set_hotkeys()

        expected_up = {
            keyboard.Key.ctrl, keyboard.Key.cmd, keyboard.Key.up}
        expected_down = {
            keyboard.Key.ctrl, keyboard.Key.cmd, keyboard.Key.down}
        expected_exit = {keyboard.Key.esc}

        assert getattr(keyboard_config, 'up') == expected_up
        assert getattr(keyboard_config, 'down') == expected_down
        assert getattr(keyboard_config, 'exit') == expected_exit
