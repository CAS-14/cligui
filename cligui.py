import curses
import time


class App:
    MODES = ("input", "instant", "sleep", "stop")
    CTLMODES = ("widget", "function")

    def __init__(self):
        self.widgets = []
        self.focus = 0
        self.mode = "input"
        self.ctlmode = "widget"
        self.cfunc = None

    def _main(self, stdscr):
        curses.curs_set(False)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

        self.style = curses.color_pair(1)
        self.style_active = self.style | curses.A_REVERSE

        for widget in self.widgets:
            widget._init_style()

        self.mode = "input"

        # main application loop
        while True:
            stdscr.clear()

            for widget in self.widgets:
                widget._render(stdscr)

            if self.focus:
                self.widgets[self.focus]._focus(stdscr)

            if self.mode == "input":
                key = stdscr.getkey()
                if self.ctlmode == "widget":
                    self.widgets[self.focus]._dispatch(key)
            
            elif self.mode == "sleep":
                time.sleep(1)

            elif self.mode == "stop":
                break

        if self.endmsg:
            return self.endmsg

    def run(self):
        result = curses.wrapper(self._main)
        if result: print(result)

    def end(self, message: str = None):
        self.endmsg = message
        self.mode = "stop"
        

class Widget:
    EX_ONLY = "This class should be used for example purposes only."

    def __init__(self, root: App):
        self.root = root
        self.x = None
        self.y = None
        self.w = None
        self.h = None

        self.root.widgets.append(self)

    def place(self, x: int, y: int, *, w: int = None, h: int = None):
        self.x = x
        self.y = y
        if w: self.w = w
        if h: self.h = h

    def _init_style(self):
        self.style = self.root.style
        self.style_active = self.root.style_active

    def _dispatch(self, key: str):
        print(f"Default Widget received key {key}. {self.EX_ONLY}")

    def _render(self, stdscr):
        print(f"Default Widget received Screen {stdscr} for render. {self.EX_ONLY}")

    def _focus(self, stdscr):
        print(f"Default Widget received Screen {stdscr} for focus render. {self.EX_ONLY}")


class MenuOption:
    def __init__(self, name: str, func: callable, args: tuple = None):
        self.name = name
        self.func = func
        self.args = args

    def do(self):
        if self.args:
            self.func(*self.args)
        else:
            self.func()


class Menu(Widget):
    def __init__(self, root: App, options: tuple[MenuOption], default: int = 0, *, horizontal: bool = False, on_change: callable = None):
        super().__init__(root)
        self.options = options
        self.active = default
        
        self.horiz = horizontal
        self.on_change = on_change

        self.symbol = None
        self.symbol_active = False

    def _dispatch(self, key: str):
        if key in ("KEY_DOWN", "KEY_RIGHT"):
            self.active += 1
            self._change()

        elif key in ("KEY_UP", "KEY_LEFT"):
            self.active -= 1
            self._change()

        elif key == "\n":
            self._select()

    def _change(self):
        if self.on_change:
            self.on_change()
        self._check_overflow()

    def _check_overflow(self):
        if self.active >= len(self.options):
            self.active = 0
        elif self.active < 0:
            self.active = len(self.options) - 1

    def _select(self):
        self.options[self.active].do()

    def _render(self, stdscr):
        if self.horiz:
            hx_offset = 0

        for i in range(len(self.options)):
            option = self.options[i]

            if self.active == i:
                active = True
                style = self.style_active
            else:
                active = False
                style = self.style

            if self.symbol:
                if self.symbol_active:
                    ss = self.style_active
                else:
                    ss = self.style

            if self.horiz:
                opt = option.name
                if hx_offset != 0:
                    opt = " " + opt

                opt_x = self.x + hx_offset
                hx_offset += len(opt)
                stdscr.addstr(self.y, opt_x, opt, style)

                if active and self.symbol:
                    if len(self.symbol) == 1:
                        self.symbol *= 2

                    stdscr.addstr(self.y, opt_x, self.symbol[0], ss)
                    stdscr.addstr(self.y, opt_x, self.symbol[1], ss)

            else:
                opt_y = self.y + i
                stdscr.addstr(opt_y, self.x, option.name, style)

                if self.symbol:
                    if active:
                        stdscr.addstr(opt_y, self.x-1, self.symbol, ss)
                    else:
                        stdscr.addstr(opt_y, self.x-1, " ", self.style)
    
    def _focus(self, stdscr):
        pass
    

class Text(Widget):
    def __init__(self, root: App, text: str):
        super().__init__(root)
        self.text = text

    def _render(self, stdscr):
        stdscr.addstr(self.y, self.x, self.text, self.style)