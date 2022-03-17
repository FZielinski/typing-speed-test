from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
BG = "#ffffff"
FG = "#000000"


class Word():
    def __init__(self, row, column, content):
        self.row = row
        self.column = column
        self.content = content
        self.label = Label(text=content, fg=FG, bg=BG, font=('Arial', 25))
        self.label.grid(column=column, row=row, padx=(10, 10))

    def typed_word_ok(self):
        self.label.config(fg="blue", bg=BG)

    def typed_word_wrong(self):
        self.label.config(fg="red", bg=BG)

    def current_word(self):
        self.label.config(bg="green")