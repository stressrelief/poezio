"""
Classes used to replace the input in some tabs or special situations,
but which are not inputs.
"""

import logging
log = logging.getLogger(__name__)


from . import Win, g_lock
from theming import get_theme, to_curses_attr


class HelpText(Win):
    """
    A Window just displaying a read-only message.
    Usually used to replace an Input when the tab is in
    command mode.
    """
    def __init__(self, text=''):
        Win.__init__(self)
        self.txt = text

    def refresh(self, txt=None):
        log.debug('Refresh: %s', self.__class__.__name__)
        if txt:
            self.txt = txt
        with g_lock:
            self._win.erase()
            self.addstr(0, 0, self.txt[:self.width-1], to_curses_attr(get_theme().COLOR_INFORMATION_BAR))
            self.finish_line(get_theme().COLOR_INFORMATION_BAR)
            self._refresh()

    def do_command(self, key, raw=False):
        return False

    def on_delete(self):
        return

class YesNoInput(Win):
    """
    A Window just displaying a Yes/No input
    Used to ask a confirmation
    """
    def __init__(self, text=''):
        Win.__init__(self)
        self.key_func = {
                'y' : self.on_yes,
                'n' : self.on_no,
        }
        self.txt = text
        self.value = None

    def on_yes(self):
        self.value = True

    def on_no(self):
        self.value = False

    def refresh(self, txt=None):
        log.debug('Refresh: %s', self.__class__.__name__)
        if txt:
            self.txt = txt
        with g_lock:
            self._win.erase()
            self.addstr(0, 0, self.txt[:self.width-1], to_curses_attr(get_theme().COLOR_WARNING_PROMPT))
            self.finish_line(get_theme().COLOR_WARNING_PROMPT)
            self._refresh()

    def do_command(self, key, raw=False):
        if key.lower() in self.key_func:
            self.key_func[key]()

    def prompt(self):
        """Monopolizes the input while waiting for a recognized keypress"""
        cl = []
        while self.value is None:
            if len(cl) == 1 and cl[0] in self.key_func:
                self.key_func[cl[0]]()
            cl = self.core.read_keyboard()

    def on_delete(self):
        return

