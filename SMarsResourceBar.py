# Resource Bar
# Progress Bar with min, max, current values
# Length
# Text Label
# Current value
# Color (TODO: or full, medium, low)
# Image label

from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk


class ResourceBar:
    def __init__(self, parent, resource, barLength, maxValue, initialValue, horiz):
        # rid is the resource id
        # barColor is text 'red', 'blue' etc

        name = resource.name
        units = resource.units
        fullText = name + " (" + units + ")"
        iconPath = resource.icon
        barColor = resource.barColor

        # Create a LabelFrame to hold this resource bar
        self.resourceFrame = tk.LabelFrame(parent, text=fullText, borderwidth=1, relief="sunken")

        # Create the Label to hold the icon
        self.resourceIconLabel = tk.Label(self.resourceFrame, width=32, height=32)

        # Load the icon and pop it into the Label
        image = Image.open(iconPath).convert("RGB")
        image = image.resize((38

                                   , 38), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(image)
        self.resourceIconLabel.configure(image=self.icon)
        self.resourceIconLabel.image = self.icon
        self.resourceIconLabel.pack(side=tk.LEFT, padx=5)

        # Setup the progress bar
        self.value = tk.DoubleVar()
        self.value.set(initialValue)
        self.valuetext = tk.StringVar()
        self.valuetext.set(str(initialValue))

        # self.pbcanvas = tk.Canvas(self.resourceFrame, relief=tk.FLAT, background="#D2D2D2", width=barLength, height=5)
        self.pbcanvas = tk.Canvas(self.resourceFrame, relief=tk.FLAT,  width=barLength, height=5)
        s = ttk.Style()
        s.theme_use('alt')
        s.configure(barColor+".resource.Horizontal.TProgressbar", foreground=barColor, background=barColor)
        print(barColor)
        self.pb = ttk.Progressbar(self.pbcanvas, variable=self.value,
                                  style=barColor+".resource.Horizontal.TProgressbar",
                                  orient="horizontal", max=maxValue, length=barLength,
                                  value=initialValue, mode="determinate")
        self.pb.pack(padx=10)

        self.pbcanvas.create_window(1, 1, anchor=tk.NW, window=self.pb)
        self.pbcanvas.pack(pady=1)

        self.resourceTextLabel = tk.Label(self.resourceFrame, textvariable=self.valuetext)
        self.resourceTextLabel.pack()

        self.resourceIconLabel.pack()

        if horiz:
            self.resourceFrame.pack(side=tk.LEFT)
        else:
            self.resourceFrame.pack()

    def updateValue(self, value):
        self.value.set(value)
        self.valuetext.set(str("{0:.1f}".format(round(value, 1))))


# NOTES
# ProgressBar Styles: classic, clam, alt, xpnative (the default on my system), and winnative Alt looks the best
