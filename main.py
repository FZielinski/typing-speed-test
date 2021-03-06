from tkinter import *
import requests
import random
from time import time
import math
from word import Word


r = requests.get('https://random-word-api.herokuapp.com/word?number=50')

# ---------------------------- CONSTANTS -------------------------------------- #
BG = "#ffffff"
FG = "#000000"
words_list = []
words_instances_list = []
reps = 0
count_sec = 59
word_pos = 0
score = 0
end_of_time = False


# ---------------------------- WORDS LIST FROM API ---------------------------- #
def get_words_from_api():
    while len(words_list) < 300:
        r = requests.get('https://random-word-api.herokuapp.com/word?number=1000')
        for word in r.json():
            if len(word) <= 6:
                words_list.append(word)
            elif len(words_list) >= 300:
                break
    random.shuffle(words_list)


# ---------------------------- LABELS FOR WORDS ------------------------------- #
def create_words_labels(index):
    for y in range(0, 3):
        for x in range(0, 7):
            word_instance = Word(y, x, words_list[index])
            words_instances_list.append(word_instance)
            index += 1


# ---------------------------- SCOREBOARD --------------------------------------- #
def scoreboard():
    time_from_start = 60 - count_sec
    words_per_second = math.floor((score*60)/time_from_start)
    score_label.config(text=f"{words_per_second}/min")


# ---------------------------- COMPARE WORD FROM ENTRY WITH LIST -------------- #
def compare_word(event):
    global word_pos, score
    user_input = (entry.get()).rstrip()
    if user_input == words_list[word_pos]:
        words_instances_list[word_pos].typed_word_ok()
        entry.delete(0, 'end')
        word_pos += 1
        score += 1
    elif user_input != words_list[word_pos]:
        words_instances_list[word_pos].typed_word_wrong()
        entry.delete(0, 'end')
        word_pos += 1
    if word_pos == len(words_instances_list):
        for word in words_instances_list:
            word.clear_label()
        create_words_labels(word_pos)
    words_instances_list[word_pos].current_word()
    scoreboard()


# ---------------------------- COUNTDOWN MECHANISM ----------------------------- #
def count_down():
    global reps, count_sec, end_of_time
    reps += 1
    if reps == 10:
        reps = 0
        count_sec -= 1
    count_msec = 9 - reps
    if count_sec > 0 or count_msec > 0:
        timer_label.config(text=f"{count_sec}.{count_msec}s")
        window.after(100, count_down)
    else:
        timer_label.config(text=f"0.0s")
        end_of_time = True
        window.unbind("<space>")


# ---------------------------- UI SETUP --------------------------------------- #
window = Tk()
window.title("Typing speed test app")
window.config(padx=100, pady=50, bg=BG)
get_words_from_api()
create_words_labels(0)
words_instances_list[word_pos].current_word()

if not end_of_time:
    window.bind("<space>", compare_word)


entry = Entry(font=('Arial', 15), highlightthickness=2)
entry.grid(column=3, row=4, pady=(30, 30))
entry.focus()

score_label = Label(text="Score: words/s", fg=FG, bg=BG, font=('Arial', 25))
score_label.grid(column=4, row=3, pady=(30, 30))

timer_label = Label(text="Timer: 60.00", fg=FG, bg=BG, font=('Arial', 25))
timer_label.grid(column=2, row=3, pady=(30, 30))


window.after(100, count_down)

window.mainloop()