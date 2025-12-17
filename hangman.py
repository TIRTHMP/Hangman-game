import tkinter as tk
from tkinter import messagebox
import random
from playsound3 import playsound

# =============================
# THEME CONFIGURATION
# =============================
LIGHT_THEME = {
    "bg": "white",
    "fg": "black"
}

DARK_THEME = {
    "bg": "#1e1e1e",
    "fg": "white"
}

current_theme = DARK_THEME

# =============================
# WORD LISTS BY DIFFICULTY
# =============================
easy_words = ["apple", "grape", "lemon", "mango"]
medium_words = ["banana", "cherry", "orange"]
hard_words = ["pineapple", "watermelon"]

difficulty = "Medium"

word = ""
guesses = 6
guessed_letters = []

# =============================
# ROOT WINDOW
# =============================
root = tk.Tk()
root.title("Hangman Game")
root.config(bg=current_theme["bg"])

# =============================
# LOAD HANGMAN GIFS
# =============================
hangman_images = []
for i in range(7):
    img = tk.PhotoImage(file=f"Hangman-{i}.gif")
    hangman_images.append(img)

# =============================
# HANGMAN IMAGE LABEL
# =============================
image_label = tk.Label(root, image=hangman_images[0],
                       bg=current_theme["bg"])
image_label.grid(row=0, column=0, columnspan=3)

# =============================
# GAME SETUP
# =============================
def setup_game():
    global word, guesses, guessed_letters

    if difficulty == "Easy":
        word = random.choice(easy_words)
        guesses = 8
    elif difficulty == "Medium":
        word = random.choice(medium_words)
        guesses = 6
    else:
        word = random.choice(hard_words)
        guesses = 4

    guessed_letters.clear()

# =============================
# LABELS & ENTRY
# =============================
word_label = tk.Label(root, font=("Arial", 16),
                      bg=current_theme["bg"], fg=current_theme["fg"])
word_label.grid(row=1, column=0, columnspan=3)

guesses_label = tk.Label(root,
                         bg=current_theme["bg"], fg=current_theme["fg"])
guesses_label.grid(row=2, column=0, columnspan=3)

guessed_label = tk.Label(root,
                         bg=current_theme["bg"], fg=current_theme["fg"])
guessed_label.grid(row=3, column=0, columnspan=3)

guess_entry = tk.Entry(root)
guess_entry.grid(row=4, column=0, columnspan=3)

# =============================
# UPDATE GIF BASED ON GUESSES
# =============================
def update_hangman_image():
    stage = 6 - guesses
    stage = min(max(stage, 0), 6)
    image_label.config(image=hangman_images[stage])

# =============================
# GAME LOGIC
# =============================
def check_guess():
    global guesses

    guess = guess_entry.get().lower()
    guess_entry.delete(0, tk.END)

    if len(guess) != 1 or not guess.isalpha():
        return
    if guess in guessed_letters:
        return

    guessed_letters.append(guess)
    guessed_label.config(text="Guessed letters: " + " ".join(guessed_letters))

    if guess in word:
        word_list = list(word_label["text"])
        for i, letter in enumerate(word):
            if letter == guess:
                word_list[2 * i] = guess
        word_label.config(text="".join(word_list))

        if "_" not in word_list:
            playsound("win.wav")
            messagebox.showinfo("Hangman", "🎉 You Win!")
            guess_entry.config(state=tk.DISABLED)
    else:
        guesses -= 1
        guesses_label.config(text=f"Guesses remaining: {guesses}")
        update_hangman_image()

        if guesses == 0:
            playsound("lose.mp3")
            messagebox.showinfo("Hangman", f"❌ You Lose!\nWord was: {word}")
            guess_entry.config(state=tk.DISABLED)

# =============================
# HINT SYSTEM
# =============================
def give_hint():
    available = [c for c in word if c not in guessed_letters]
    if available:
        hint = random.choice(available)
        guess_entry.insert(0, hint)
        check_guess()

# =============================
# RESTART GAME
# =============================
def restart_game():
    setup_game()
    word_label.config(text=" ".join("_" for _ in word))
    guesses_label.config(text=f"Guesses remaining: {guesses}")
    guessed_label.config(text="Guessed letters: ")
    guess_entry.config(state=tk.NORMAL)
    image_label.config(image=hangman_images[0])

# =============================
# THEME TOGGLE
# =============================
def toggle_theme():
    global current_theme
    current_theme = LIGHT_THEME if current_theme == DARK_THEME else DARK_THEME

    root.config(bg=current_theme["bg"])
    image_label.config(bg=current_theme["bg"])

    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=current_theme["bg"], fg=current_theme["fg"])

# =============================
# DIFFICULTY CHANGE
# =============================
def change_difficulty(level):
    global difficulty
    difficulty = level
    restart_game()

# =============================
# BUTTONS
# =============================
tk.Button(root, text="Guess", command=check_guess).grid(row=5, column=0)
tk.Button(root, text="Hint", command=give_hint).grid(row=5, column=1)
tk.Button(root, text="Restart", command=restart_game).grid(row=5, column=2)

tk.Button(root, text="Easy", command=lambda: change_difficulty("Easy")).grid(row=6, column=0)
tk.Button(root, text="Medium", command=lambda: change_difficulty("Medium")).grid(row=6, column=1)
tk.Button(root, text="Hard", command=lambda: change_difficulty("Hard")).grid(row=6, column=2)

tk.Button(root, text="Light / Dark", command=toggle_theme)\
    .grid(row=7, column=0, columnspan=3)

# =============================
# INITIALIZE
# =============================
setup_game()
restart_game()

root.bind("<Return>", lambda event: check_guess())
root.mainloop()
