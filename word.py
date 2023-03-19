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
        self.master.geometry("1920x1080")
        self.master.attributes('-fullscreen', True)  # Fullscreen modu
        self.pack(fill="both", expand=True)

        # Add icon to taskbar
        self.master.iconbitmap("assets/brain.ico")



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
            button = tk.Button(self.answer_frame, text="", width=50, height=10, command=lambda i=i: self.check_answer(i), wraplength=200, highlightbackground=None, highlightcolor=None, bg="#bbae9f")
            self.answer_buttons.append(button)
            self.answer_buttons[i].grid(row=i//2, column=i%2, padx=0, pady=0)

        self.next_button = tk.Button(self, text="Next", width=40, height=2, command=self.next_question, state=tk.DISABLED, bg="#bbae9f")
        self.next_button.pack(pady=20)

        self.choose_file_button = tk.Button(self, text="Choose File   📂", width=40, height=2, command=self.choose_file, fg="black", bg="#bbae9f")
        self.choose_file_button.pack(pady=20)
                # settings button
        self.settings_button = tk.Button(self, text="Guide", width=20, height=2, command=self.show_settings, bg="#bbae9f")
        self.settings_button.pack(pady=20)

        self.exit_button = tk.Button(self, text="Çık", width=20, height=2, command=self.master.destroy, bg="#bbae9f")
        self.exit_button.pack(pady=20)

                # Bind F11 key to toggle fullscreen
        self.master.bind("<F11>", self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        """Toggle between fullscreen and normal mode."""
        self.master.attributes("-fullscreen", not self.master.attributes("-fullscreen"))


    def show_settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Guide")

        # Get screen width and height
        screen_width = settings_window.winfo_screenwidth()
        screen_height = settings_window.winfo_screenheight()

        # Calculate coordinates for centering the settings window
        settings_width = 600
        settings_height = 400
        x = (screen_width/2) - (settings_width/2)
        y = (screen_height/2) - (settings_height/2)

        # Set the geometry of the settings window to the center of the screen
        settings_window.geometry("%dx%d+%d+%d" % (settings_width, settings_height, x, y))

        settings_window.transient(self.master)
        settings_window.grab_set()

        tk.Label(settings_window, text="\n\n\nWhat Is This App ?").pack()
        tk.Label(settings_window, text="This app developed to improve users foreign language word and setence knowledge. \n                                     ").pack()
        tk.Label(settings_window, text="How It Works ?").pack()
        tk.Label(settings_window, text="Import your google translete favorite words or google translate history as an exel file \nthen use choose file button and choose this exel file thused this program will ask \nyou meaning of words which coming from your file and which you have to learn. \n🙂").pack()
        tk.Label(settings_window, text="Who Am I ?").pack()
        tk.Label(settings_window, text="Hi I'm Yasin and Studying Computer Engineering at Recep Tayyip Erdogan University. \nI developed this program to improve my english word knowledge. \nThused I could improve my programming skils with english.").pack()
        tk.Label(settings_window, text="Contact With Me").pack()
        tk.Label(settings_window, text="LinkedIN :  - - -").pack()


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


        self.word_label.config(text=english_sentence)

        for i in range(4):
            wrapped_text = "\n".join(textwrap.wrap(choices[i], width=25))
            self.answer_buttons[i].config(text=wrapped_text, bg="SystemButtonFace")

        self.current_sentence = english_sentence
        self.current_answer = turkish_sentence
        self.current_answer_index = choices.index(turkish_sentence)


root = tk.Tk()

root.iconbitmap("assets/brain.ico") # Burada, ikonun yolunu belirtin

# Center the window on the screen
window_width = 1920
window_height = 1080
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

app = WordMemorizationApp(master=root)
app.mainloop()


