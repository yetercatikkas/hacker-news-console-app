
# -*- coding: utf-8 -*-
# !/usr/bin/env python
import curses
class Curses(object):

      """def __init__(self):
          self.popup()"""

      def popup(self):
          myscreen = curses.initscr()
          myscreen.border(0)
          myscreen.addstr(1, 1, "0: displays top ten stories!")
          myscreen.addstr(2, 1, "*: displays previous story!")
          myscreen.addstr(3, 1, "-: displays next story!")
          myscreen.addstr(4, 1, "q: quit the terminal!")
          myscreen.addstr(5, 1, "?: help!")
          myscreen.addstr(6, 1, "from 1 to 10: displays list of top ten stories!")
          myscreen.addstr(9,1,  "Press any keyboard characters to exit this window!")
          myscreen.getch()
          myscreen.refresh()
          curses.endwin()




