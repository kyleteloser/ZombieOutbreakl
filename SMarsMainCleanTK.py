from Tkinter import *

try:
    import Image
    import ImageDraw
    import ImageFont
    import ImageTk
except ImportError:
    from PIL import Image, ImageDraw, ImageFont, ImageTk


class Application(Frame):
    def __init__(self, master=None):
        self.mainFrame = Frame.__init__(self, master)


def main():
    root = Tk()
    app = Application(root)
    app.master.title(gGameName)
    app.mainloop()
    root.quit()


gGameName = "Real Mars Simulation"

if __name__ == '__main__':
    main()

