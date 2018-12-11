import sys
import pytest
from pardal.speaking import say
from unittest.mock import patch


@pytest.mark.skipif(sys.platform == 'darwin', reason='not valid on MacOS')
@patch('pardal.speaking.engine.say')
def test_say(mock_engine):
    say('Hello world')

    assert mock_engine.called
