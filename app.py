import os
from datetime import datetime

import cligui as cg


class App(cg.App):
    def __init__(self):
        super().__init__()

        self.display = cg.Text(self, "Testing testing testing...")
        self.display.place(3, 3)

        options = (
            cg.MenuOption("Show time", self.show_time),
            cg.MenuOption("Show weather", self.show_weather),
            cg.MenuOption("Quit", self.end, ("Bye bye!",))
        )
        menu = cg.Menu(self, options, 2)
        menu.symbol = "*"
        menu.place(3, 5)

        self.mode = "instant"
        self.focus = 1

    def show_time(self):
        time = datetime.now().strftime("%I:%M %p")
        self.display.text = f"The time is {time}."

    def show_weather(self):
        self.display.text = "The weather is sunny, 65 degrees. (example)"


if __name__ == "__main__":
    app = App()
    app.run()