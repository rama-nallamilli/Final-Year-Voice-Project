import tkinter as tk
from tkinter import ttk
import speech_recognition as sr

# This function is used to record audio from a microphone
# and save it to a file called New Audio File
def recordAudioFunction():
    r = sr.Recognizer()
    # sets the microphone as the source of audio
    with sr.Microphone() as source:
        r.pause_threshold = 1
        # waits for a second to let the recogniser adjust
        # to the surrounding noise
        r.adjust_for_ambient_noise(source, duration=1)
        print('Speak Anything : ')
        audio = r.listen(source)
        try:
            # writes the newly recorded audio to this file
            with open('NewAudioFile.wav', 'wb') as f:
                f.write(audio.get_wav_data())
        # a couple of exception clauses to catch errors if the microphone
        # doesnt quite pick up the audio
        except sr.UnknownValueError:
            print('Sorry, I did not hear that')
        except sr.RequestError:
            print('Sorry my speech service is currently unavailable')


# This function is used to output the contents of the audio file
# to the console window
def readAudioFile():
    r = sr.Recognizer()
    NewAudioFile = sr.AudioFile('NewAudioFile.wav')
    with NewAudioFile as source:
        audio_text = r.record(source)
    print(type(audio_text))
    print(r.recognize_google(audio_text))

# For the use of GUI i used the Tkinter module which is the standard
# python interface to the Tk GUI  toolkit

LARGE_FONT = ("Calibri", 30)

# The class below is essentially as the name of the class
# is described a blue print for the two pages needed I found it easier
# to create the pages this way in case I needed to make multiple pages
# which i found myself doing

class PageBlueprint(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Voice Recognition Project")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, SaveAudio):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Voice Recognition", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Save New Audio",
                            command=lambda: controller.show_frame(SaveAudio))
        button.place(x=260,y=150)


# The main class which is used to bring the components together
# it has three buttons one which takes you back to the main page
# and the other two which are attached to their respective functions
# recordAudioFunction and readAudioFile

class SaveAudio(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Save Audio to File", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Main Page",
                             command=lambda: controller.show_frame(MainPage))
        button1.place(x=20,y=10)

        button2 = ttk.Button(self, text="Record New Audio",
                             command=recordAudioFunction)
        button2.place(x=260,y=130)

        button3 = ttk.Button(self, text="Print Text From Audio File",
                             command=readAudioFile)
        button3.place(x=240,y=180)


app = PageBlueprint()
app.geometry("600x400")
app.mainloop()