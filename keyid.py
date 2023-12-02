import curses

def main(stdscr):
    curses.curs_set(False)
    stdscr.addstr("Press any key")
    while True:
        key = stdscr.getkey()
        stdscr.clear()
        stdscr.addstr("Pressed key: ")
        stdscr.addstr(key, curses.A_STANDOUT)

if __name__ == "__main__":
    curses.wrapper(main)