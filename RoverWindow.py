
from PIL import Image, ImageTk
import tkinter as tk


class RoverWindow:
    def __init__(self, parent, initialValue):
        self.roverWindow = tk.LabelFrame(parent, text="Zombie (In hundred-millions)", borderwidth=2, relief="sunken", padx=20, pady=10)
        self.numRoverEntryVar = tk.StringVar()

        self.roverImageLabel = tk.Label(self.roverWindow, width=32, height=32)
        image = Image.open("./assets/ZombiePic.jpeg").convert("RGB")
        image = image.resize((32, 32), Image.ANTIALIAS)
        self.roverImage = ImageTk.PhotoImage(image)
        self.roverImageLabel.configure(image=self.roverImage)
        self.roverImageLabel.image = self.roverImage
        self.roverImageLabel.pack(side=tk.LEFT)

        self.numRoverEntry = tk.Entry(self.roverWindow, textvariable=self.numRoverEntryVar)
        self.numRoverEntryVar.set(str(initialValue))
        self.numRoverEntry.pack()
