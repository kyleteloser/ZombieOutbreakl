from PIL import Image, ImageTk
import tkinter as tk


class MapWindow:
    def __init__(self, parent):
        self.mapWindow = tk.LabelFrame(parent, text="Map", borderwidth=2, relief="sunken")

        # load the image of mars for the moment
        self.mapImageLabel = tk.Label(self.mapWindow, width=512, height=512)
        image = Image.open("./assets/city.png").convert("RGB")
        image = image.resize((512, 512), Image.ANTIALIAS)
        self.mapImage = ImageTk.PhotoImage(image)
        self.mapImageLabel.configure(image=self.mapImage)
        self.mapImageLabel.image = self.mapImage
        self.mapImageLabel.pack(side=tk.LEFT)
