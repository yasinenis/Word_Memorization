import tkinter as tk 
import random
import tkinter.filedialog as fd
import openpyxl as xl
import tkinter.messagebox as mb
import textwrap
import winsound

class WordMemorizationApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Word Memorization App")
        self.master.geometry("800x800")
        self.pack(fill="both", expand=True)

        # Add background image
        self.background_image = tk.PhotoImage(file="assets/gate3.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Add other widgets
        self.word_label = tk.Label(self, text="", font=("Helvetica", 24), wraplength=500)
        self.word_label.pack(pady=20)

        self.answer_frame = tk.Frame(self)
        self.answer_frame.pack(expand=True)

        self.answer_buttons = []
        for i in range(4):
            button = tk.Button(self.answer_frame, text="", width=50, height=10, command=lambda i=i: self.check_answer(i), wraplength=200, highlightbackground=None, highlightcolor=None)
            self.answer_buttons.append(button)
            self.answer_buttons[i].grid(row=i//2, column=i%2, padx=0, pady=0)

        self.next_button = tk.Button(self, text="Next", width=40, height=2, command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=20)

        self.choose_file_button = tk.Button(self, text="Choose File", width=40, height=2, command=self.choose_file)
        self.choose_file_button.pack(pady=20)
                # settings button
        self.settings_button = tk.Button(self, text="Guide", width=20, height=2, command=self.show_settings)
        self.settings_button.pack(pady=20)

    def show_settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Guide")
        settings_window.geometry("400x400")
        settings_window.transient(self.master)
        settings_window.grab_set()

        # Add widgets to the settings window
        # ...

        settings_window.wait_window()
                #------------
        self.workbook = None  # Eklendi: Dosya seçilmediği durumda hata vermemesi için
        self.sheet = None  # Eklendi: Dosya seçilmediği durumda hata vermemesi için   

    def choose_file(self):
        file_path = fd.askopenfilename()
        if file_path:
            self.workbook = xl.load_workbook(filename=file_path)
            self.sheet = self.workbook.active
            self.next_question()

    def check_answer(self, answer):
        selected_text = self.answer_buttons[answer]["text"]
        if selected_text == self.current_answer:
            self.answer_buttons[answer].config(bg="green")
            winsound.PlaySound("assets/cor2.wav", winsound.SND_ASYNC)
        else:
            self.answer_buttons[answer].config(bg="red")
            self.answer_buttons[self.current_answer_index].config(bg="green")
            winsound.PlaySound("assets/wrong.wav", winsound.SND_ASYNC)

        for i in range(4):
            self.answer_buttons[i].config(state=tk.DISABLED)

        self.next_button.config(state=tk.NORMAL)

        # Bind <Return> key to Next button when it's enabled
        if self.next_button['state'] == tk.NORMAL:
            self.master.bind('<Return>', lambda event: self.next_button.invoke())


    def next_question(self):
        for i in range(4):
            self.answer_buttons[i].config(state=tk.NORMAL, text="", bg="SystemButtonFace")
        self.current_sentence = ""
        self.current_answer = ""
        self.current_answer_index = -1  # Eklendi: doğru cevabın index'i sıfırlanır
        self.next_button.config(state=tk.DISABLED)

            # Call choose_file only if workbook is not already loaded
        if not self.workbook:
            self.choose_file()
        else:
            max_row = self.sheet.max_row
            random_row = random.randint(1, max_row)

            english_sentence = self.sheet[f"A{random_row}"].value
            turkish_sentence = self.sheet[f"B{random_row}"].value

            choices = [turkish_sentence]
            while len(choices) < 4:
                random_row = random.randint(1, max_row)
                random_choice = self.sheet[f"B{random_row}"].value
                if random_choice and random_choice not in choices:
                    choices.append(random_choice)
                elif not random_choice:
                    continue

            random.shuffle(choices)

        print(f"English Sentence: {english_sentence}")
        print(f"Turkish Sentence: {turkish_sentence}")
        print(f"Choices: {choices}")

        self.word_label.config(text=english_sentence)

        for i in range(4):
            wrapped_text = "\n".join(textwrap.wrap(choices[i], width=25))
            self.answer_buttons[i].config(text=wrapped_text, bg="SystemButtonFace")

        self.current_sentence = english_sentence
        self.current_answer = turkish_sentence
        self.current_answer_index = choices.index(turkish_sentence)


root = tk.Tk()

# Center the window on the screen
window_width = 800
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

app = WordMemorizationApp(master=root)
app.mainloop()


