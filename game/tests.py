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
(...)
FileNotFoundError: [WinError 2] Het systeem kan het opgegeven bestand niet
vinden
"""
