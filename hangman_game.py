import tkinter as tk
from tkinter import ttk
import random
import sqlite3
import os

class Hangman:
    def __init__(self, word_list):
        self.word_list = word_list
        self.new_game()

    def new_game(self):
        self.word = random.choice(self.word_list).upper()
        self.guessed_letters = set()
        self.remaining_attempts = 6
        self.game_over = False

    def display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def guess_letter(self, letter):
        if self.game_over:
            return "Game is over. Please start a new game."
        letter = letter.upper()
        if not letter.isalpha() or len(letter) != 1:
            return "Please enter a single alphabetical letter."
        if letter in self.guessed_letters:
            return f"You already guessed '{letter}'."
        self.guessed_letters.add(letter)
        if letter not in self.word:
            self.remaining_attempts -= 1

        status = self.check_game_status()
        if status is not None:
            self.game_over = True
            save_game_result(self.word, self.guessed_letters, self.remaining_attempts)
        return status

    def check_game_status(self):
        if all(letter in self.guessed_letters for letter in self.word):
            return "win"
        if self.remaining_attempts <= 0:
            return "lose"
        return None

    def get_remaining_attempts(self):
        return self.remaining_attempts

    def get_guessed_letters(self):
        return sorted(self.guessed_letters)

def save_game_result(word, guessed_letters, attempts_left):
    conn = sqlite3.connect('hangman_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS game_history
                 (word TEXT, guessed_letters TEXT, attempts_left INTEGER)''')
    c.execute("INSERT INTO game_history (word, guessed_letters, attempts_left) VALUES (?, ?, ?)",
              (word, ','.join(sorted(guessed_letters)), attempts_left))
    conn.commit()
    conn.close()

def fetch_history():
    if not os.path.exists('hangman_history.db'):
        return []
    conn = sqlite3.connect('hangman_history.db')
    c = conn.cursor()
    c.execute("SELECT rowid, word, guessed_letters, attempts_left FROM game_history ORDER BY rowid DESC")
    rows = c.fetchall()
    conn.close()
    return rows

class HangmanApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hangman Game")
        self.configure(bg="#121212")
        self.state('zoomed')
        self.bind("<Escape>", lambda e: self.destroy())

        self.word_list = [
            'PYTHON', 'HANGMAN', 'DEVELOPER', 'PROGRAMMING', 'CHALLENGE',
            'OPENAI', 'COMPUTER', 'ALGORITHM', 'SOFTWARE', 'FUNCTION',
            'VARIABLE', 'DATABASE', 'JAVASCRIPT', 'DEBUGGING', 'COMPILER',
            'NETWORK', 'SCRIPT', 'OPERATING', 'SYSTEM', 'INTERNET',
            'FRAMEWORK', 'LIBRARY', 'BOOLEAN', 'INTEGER', 'FLOAT',
            'STRING', 'ARRAY', 'DICTIONARY', 'LOOP', 'CONDITION',
            'BINARY', 'HEXADECIMAL', 'PYRAMID', 'PIXEL', 'DISPLAY',
            'GRAPHICS', 'CODE', 'VERSION', 'CONTROL', 'GITHUB',
            'APPLICATION', 'USER', 'INTERFACE', 'PROTOCOL', 'SECURITY',
            'ENCRYPTION', 'DECRYPTION', 'SERVER', 'CLIENT', 'DATABASE',
            'QUERY', 'INDEX', 'FUNCTIONALITY', 'SYNCHRONIZATION', 'MULTITHREADING',
            'DEBUG', 'ERROR', 'EXCEPTION', 'LIBRARY', 'MODULE',
            'PACKAGE', 'REPOSITORY', 'VERSIONING', 'COMMIT', 'BRANCH',
            'MERGE', 'DEPLOYMENT', 'CONTAINER', 'VIRTUALIZATION', 'CLOUD',
            'API', 'ENDPOINT', 'REQUEST', 'RESPONSE', 'AUTHENTICATION',
            'AUTHORIZATION', 'SESSION', 'COOKIE', 'CACHE', 'LOADBALANCING',
            'SCALABILITY', 'PERFORMANCE', 'OPTIMIZATION', 'TESTING', 'DEBUGGING',
            'INTEGRATION', 'CONTINUOUS', 'DELIVERY', 'DEPLOY', 'MONITORING',
            'ANALYTICS', 'METRICS', 'LOGGING', 'TRACING', 'PROFILING',
            'SIMULATION', 'ANIMATION', 'RENDERING', 'COMPOSITION', 'TRANSFORMATION'
        ]
        self.game = Hangman(self.word_list)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = tk.Frame(self, bg="#121212")
        self.container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        for i in range(8):
            self.container.grid_rowconfigure(i, weight=1, pad=5)
        self.container.grid_columnconfigure(0, weight=1)

        self.create_widgets()

        # Force canvas size update before first draw to show hangman stand
        self.update()
        self.update_ui()

    def create_widgets(self):
        self.title_label = tk.Label(self.container, text="HANGMAN GAME",
                                    font=("Segoe UI Black", 36, "bold"),
                                    fg="#ffd600", bg="#121212")
        self.title_label.grid(row=0, column=0, sticky="ew", pady=(0,10))

        self.word_var = tk.StringVar()
        self.word_label = tk.Label(self.container, textvariable=self.word_var,
                                   font=("Consolas", 44),
                                   fg="#ffffff", bg="#121212", pady=10)
        self.word_label.grid(row=1, column=0, sticky="ew")

        attempts_canvas_frame = tk.Frame(self.container, bg="#121212")
        attempts_canvas_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        attempts_canvas_frame.grid_columnconfigure(0, weight=0, minsize=250)
        attempts_canvas_frame.grid_columnconfigure(1, weight=1, minsize=100)
        attempts_canvas_frame.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(attempts_canvas_frame, width=250, height=250,
                                bg="#121212", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="n")

        self.attempts_var = tk.StringVar()
        self.attempts_label = tk.Label(attempts_canvas_frame, textvariable=self.attempts_var,
                                       font=("Segoe UI", 20), fg="#ff4444",
                                       bg="#121212", anchor="nw", justify="left")
        self.attempts_label.grid(row=0, column=1, sticky="nw")

        self.guessed_var = tk.StringVar()
        self.guessed_label = tk.Label(self.container, textvariable=self.guessed_var,
                                     font=("Segoe UI", 20),
                                     fg="#aaaaaa", bg="#121212", anchor="w", justify="left")
        self.guessed_label.grid(row=3, column=0, sticky="ew", pady=10, padx=5)

        input_frame = tk.Frame(self.container, bg="#121212")
        input_frame.grid(row=4, column=0, sticky="w", pady=10, padx=5)

        guess_label = tk.Label(input_frame, text="Enter a letter:",
                               font=("Segoe UI", 20), fg="#ffffff", bg="#121212")
        guess_label.pack(side='left', padx=(0, 10))

        self.guess_entry = tk.Entry(input_frame, font=("Segoe UI", 24),
                                    width=3, justify='center',
                                    bg="#292929", fg="white",
                                    insertbackground='white')
        self.guess_entry.pack(side='left')
        self.guess_entry.bind('<Return>', self.handle_guess)

        guess_button = tk.Button(input_frame, text="Guess", command=self.handle_guess,
                                 font=("Segoe UI", 20), bg="#388e3c", fg="white",
                                 activebackground="#66bb6a", activeforeground="#000000",
                                 relief="flat", padx=15, pady=8)
        guess_button.pack(side='left', padx=15)

        self.message_label = tk.Label(self.container, text="",
                                      font=("Segoe UI", 16),
                                      fg="#ffb74d", bg="#121212")
        self.message_label.grid(row=5, column=0, sticky="ew", pady=5)

        btn_frame = tk.Frame(self.container, bg="#121212")
        btn_frame.grid(row=6, column=0, sticky="ew", pady=10)

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        new_game_btn = tk.Button(btn_frame, text="New Game", command=self.new_game,
                                 font=("Segoe UI", 18), bg="#1976d2", fg="white",
                                 activebackground="#63a4ff", activeforeground="#000000",
                                 relief="flat", padx=20, pady=8)
        new_game_btn.grid(row=0, column=0, sticky='ew', padx=20)

        history_btn = tk.Button(btn_frame, text="Show History", command=self.show_history,
                                font=("Segoe UI", 18), bg="#7b1fa2", fg="white",
                                activebackground="#af52bf", activeforeground="#000000",
                                relief="flat", padx=20, pady=8)
        history_btn.grid(row=0, column=1, sticky='ew', padx=20)

        quit_btn = tk.Button(btn_frame, text="Quit", command=self.destroy,
                             font=("Segoe UI", 18), bg="#d32f2f", fg="white",
                             activebackground="#ff6659", activeforeground="#000000",
                             relief="flat", padx=20, pady=8)
        quit_btn.grid(row=0, column=2, sticky='ew', padx=20)

        self.popup_frame = tk.Frame(self, bg='#212121', bd=4, relief="ridge")
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_frame.lower()
        self.popup_frame.configure(width=600, height=300)

        self.popup_label = tk.Label(self.popup_frame, text="", font=("Segoe UI Black", 28, "bold"),
                                    fg="#ffd600", bg='#212121')
        self.popup_label.pack(pady=30)

        popup_btn_frame = tk.Frame(self.popup_frame, bg='#212121')
        popup_btn_frame.pack(pady=15)

        self.play_again_btn = tk.Button(popup_btn_frame, text="Play Again",
                                        font=("Segoe UI", 20), bg="#388e3c", fg="white",
                                        relief="flat", padx=30, pady=10,
                                        command=self.hide_popup_and_new_game)
        self.play_again_btn.grid(row=0, column=0, padx=25)

        self.exit_btn = tk.Button(popup_btn_frame, text="Exit",
                                  font=("Segoe UI", 20), bg="#d32f2f", fg="white",
                                  relief="flat", padx=30, pady=10,
                                  command=self.destroy)
        self.exit_btn.grid(row=0, column=1, padx=25)

    def handle_guess(self, event=None):
        if self.game.game_over:
            return
        letter = self.guess_entry.get().strip().upper()
        self.guess_entry.delete(0, tk.END)

        self.message_label.config(text="")

        if len(letter) != 1 or not letter.isalpha():
            self.message_label.config(text="Please enter a single letter.")
            self.guess_entry.focus_set()
            return

        result = self.game.guess_letter(letter)

        if result == "win":
            self.update_ui()
            self.show_game_over_popup(win=True)
            self.message_label.config(text="")
        elif result == "lose":
            self.update_ui()
            self.show_game_over_popup(win=False)
            self.message_label.config(text="")
        elif isinstance(result, str):
            self.message_label.config(text=result)
        else:
            self.message_label.config(text="")

        self.update_ui()

        if not self.game.game_over:
            self.guess_entry.focus_set()

    def update_ui(self):
        display_word = self.game.display_word()
        self.word_var.set(display_word)

        width = self.winfo_width()
        height = self.winfo_height()
        if width < 800:
            width = 800
        if height < 600:
            height = 600

        max_width = width - 150
        approx_char_count = max(len(display_word), 10)
        approx_char_width = max_width / approx_char_count
        font_size = max(min(int(approx_char_width * 0.7), 50), 26)
        self.word_label.config(font=("Consolas", font_size))

        self.attempts_var.set(f"Remaining Attempts: {self.game.get_remaining_attempts()}")
        guessed = ', '.join(self.game.get_guessed_letters())
        self.guessed_var.set(f"Guessed Letters: {guessed if guessed else '-'}")

        self.draw_hangman_figure(self.game.get_remaining_attempts())

    def new_game(self):
        self.game.new_game()
        self.message_label.config(text="")
        self.guess_entry.config(state='normal')
        self.guess_entry.focus_set()
        self.popup_frame.lower()
        self.update_ui()

    def hide_popup_and_new_game(self):
        self.popup_frame.lower()
        self.new_game()

    def show_game_over_popup(self, win):
        if win:
            text = f"YOU WIN!\n\nThe word was:\n{self.game.word}"
            self.popup_label.config(fg="#4caf50")
        else:
            text = f"GAME OVER!\n\nThe word was:\n{self.game.word}"
            self.popup_label.config(fg="#ff5252")
        self.popup_label.config(text=text)
        self.popup_frame.lift()
        self.guess_entry.config(state='disabled')

    def show_history(self):
        rows = fetch_history()
        if not rows:
            self.show_info_popup("No game history available.")
            return
        win = tk.Toplevel(self)
        win.title("Game History")
        win.geometry("900x400")
        win.configure(bg="#121212")
        win.focus_set()
        win.grab_set()

        lbl = tk.Label(win, text="Hangman Game History", font=("Segoe UI Black", 24, "bold"),
                       fg="#ffd600", bg="#121212")
        lbl.pack(pady=(10, 10))

        columns = ('ID', 'Word', 'Guessed Letters', 'Attempts Left')
        tree = ttk.Treeview(win, columns=columns, show='headings', style='History.Treeview')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')
        tree.pack(expand=True, fill='both', padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('History.Treeview', background='#212121', foreground='white', fieldbackground='#212121',
                        font=("Segoe UI", 12))
        style.map('History.Treeview', background=[('selected', '#ffca28')])

        for row in rows:
            tree.insert('', 'end', values=row)

        close_btn = tk.Button(win, text="Close", command=win.destroy,
                              font=("Segoe UI", 16), bg="#1976d2", fg="white", relief="flat",
                              padx=20, pady=10)
        close_btn.pack(pady=(0, 20))

    def show_info_popup(self, message):
        popup = tk.Toplevel(self)
        popup.title("Info")
        popup.geometry("400x150")
        popup.configure(bg="#121212")
        popup.transient(self)
        popup.grab_set()
        lbl = tk.Label(popup, text=message, font=("Segoe UI", 18), fg="#ffd600", bg="#121212")
        lbl.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        btn = tk.Button(popup, text="OK", command=popup.destroy,
                        font=("Segoe UI", 14), bg="#1976d2", fg="white", relief="flat", padx=20, pady=10)
        btn.pack(pady=(0, 20))

    def draw_hangman_figure(self, attempts_left):
        self.canvas.delete("all")

        # Get current canvas width and height; fallback to default if too small
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            w = int(self.canvas['width'])
        if h < 10:
            h = int(self.canvas['height'])

        base_color = "#bbbbbb"
        hangman_color = "#ff5252"

        base_y = h * 0.95
        base_x1 = w * 0.15
        base_x2 = w * 0.85
        pole_top = h * 0.15
        crossbeam_x = w * 0.7
        crossbeam_y = pole_top
        rope_x = crossbeam_x
        rope_y1 = pole_top
        rope_y2 = pole_top + h * 0.12

        # Draw hangman stand parts (base, pole, cross beam, rope)
        self.canvas.create_line(base_x1, base_y, base_x2, base_y, width=6, fill=base_color)  # base
        self.canvas.create_line(base_x1 + 20, base_y, base_x1 + 20, pole_top, width=6, fill=base_color)  # pole
        self.canvas.create_line(base_x1 + 20, pole_top, crossbeam_x, crossbeam_y, width=6, fill=base_color)  # cross beam
        self.canvas.create_line(rope_x, rope_y1, rope_x, rope_y2, width=6, fill=base_color)  # rope

        head_radius_w = w * 0.07
        head_radius_h = h * 0.10
        body_length = h * 0.25
        arm_length_w = w * 0.15
        arm_height = h * 0.12
        leg_length_w = w * 0.10
        leg_length_h = h * 0.20

        parts = [
            lambda: self.canvas.create_oval(rope_x - head_radius_w, rope_y2,
                                           rope_x + head_radius_w, rope_y2 + head_radius_h,
                                           width=4, outline=hangman_color),  # head
            lambda: self.canvas.create_line(rope_x, rope_y2 + head_radius_h, rope_x, rope_y2 + head_radius_h + body_length,
                                           width=4, fill=hangman_color),  # body
            lambda: self.canvas.create_line(rope_x, rope_y2 + head_radius_h + arm_height / 2,
                                           rope_x - arm_length_w, rope_y2 + head_radius_h + arm_height,
                                           width=4, fill=hangman_color),  # left arm
            lambda: self.canvas.create_line(rope_x, rope_y2 + head_radius_h + arm_height / 2,
                                           rope_x + arm_length_w, rope_y2 + head_radius_h + arm_height,
                                           width=4, fill=hangman_color),  # right arm
            lambda: self.canvas.create_line(rope_x, rope_y2 + head_radius_h + body_length,
                                           rope_x - leg_length_w, rope_y2 + head_radius_h + body_length + leg_length_h,
                                           width=4, fill=hangman_color),  # left leg
            lambda: self.canvas.create_line(rope_x, rope_y2 + head_radius_h + body_length,
                                           rope_x + leg_length_w, rope_y2 + head_radius_h + body_length + leg_length_h,
                                           width=4, fill=hangman_color),  # right leg
        ]

        parts_to_draw = 6 - attempts_left
        for i in range(parts_to_draw):
            parts[i]()

if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()

