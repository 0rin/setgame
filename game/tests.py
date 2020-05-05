from django.test import LiveServerTestCase
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

class GameTestCase(LiveServerTestCase):
    """docstring for GameTestCase"""

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(GameTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(GameTestCase, self).tearDown()

    def test_new_game():
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        first_card = selenium.find_element_by_class_name('card_outline')
        print(first_card)

"""
$ python manage.py test game/
Creating test database for alias 'default'...
E
======================================================================
ERROR: test_new_game (game.tests.GameTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\Orin\Documents\SoftwareDevelopment\LearningPython\virtualenvs\env_setgame\lib\site-packages\selenium\webdriver\common\service.py", line 72, in start
    self.process = subprocess.Popen(cmd, env=self.env,
  File "c:\users\orin\appdata\local\programs\python\python38-32\lib\subprocess.py", line 854, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "c:\users\orin\appdata\local\programs\python\python38-32\lib\subprocess.py", line 1307, in _execute_child
    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,
FileNotFoundError: [WinError 2] Het systeem kan het opgegeven bestand niet vinden

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\Orin\Documents\SoftwareDevelopment\LearningPython\setgame\game\tests.py", line 11, in setUp
    self.selenium = webdriver.Firefox()
  File "C:\Users\Orin\Documents\SoftwareDevelopment\LearningPython\virtualenvs\env_setgame\lib\site-packages\selenium\webdriver\firefox\webdriver.py", line 164, in __init__
    self.service.start()
  File "C:\Users\Orin\Documents\SoftwareDevelopment\LearningPython\virtualenvs\env_setgame\lib\site-packages\selenium\webdriver\common\service.py", line 81, in start
    raise WebDriverException(
selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH.
"""

