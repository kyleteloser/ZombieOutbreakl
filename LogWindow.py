import tkinter as tk


class LogWindow:
    def __init__(self, parent):
        self.logWindow = tk.LabelFrame(parent, text="Log Window", borderwidth=2, relief="sunken")

        self.headerFrame = tk.Frame(self.logWindow)

        headers = [["Day", "Survivors", "Buildings Own", "Delta", "Defense  ", "food", "water"]]
        headerLine1 = ""
        for h in headers:
            headerLine1 = "{: ^4} {: ^8} {: ^8} {: ^8} {: ^8} {: ^8} {: ^8}".format(*h)

        # headers2 = [["24h", "kW    ", "kW    ", "kW   ", "kW          ", "Lb (Billions)     ", "Lb (Trillions)     "]]
        headers2 = [["24h", "How Many", "How many", "", "Defense points", "Lb (Billions)", "Lb (Trillions)"]]
        headerLine2 = ""
        for h in headers2:
            headerLine2 = "{: ^4} {: ^8} {: ^8} {: ^8} {: ^8} {: ^8} {: ^8}".format(*h)

        self.header1 = tk.Label(self.headerFrame, text=headerLine1, font=("Courier", 12))
        self.header2 = tk.Label(self.headerFrame, text=headerLine2, font=("Courier", 12))

        self.header1.pack()
        self.header2.pack()
        self.headerFrame.pack()

        self.logTerm = tk.Frame(self.headerFrame)
        self.logTerminalScroll = tk.Scrollbar(self.logTerm, orient=tk.VERTICAL)
        self.logTerminalScroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.logTerminal = tk.Listbox(self.logTerm, width=60, height=20, yscrollcommand=self.logTerminalScroll.set,
                                      font=("Courier", 12))
        self.logTerminal.pack(fill=tk.BOTH)
        self.logTerminalScroll.config(command=self.logTerminal.yview)
        self.logTerm.pack()
        self.logWindow.pack(side=tk.LEFT, fill=tk.X, expand=1)

    def printTerminal(self, lines):
        for line in lines:
            self.logTerminal.insert(0, line)  # pops it at the top of the list box
            self.logTerminal.select_clear(self.logTerminal.size() - 2)  # Clear the current selected item
            self.logTerminal.select_set(tk.END)  # Select the new item
            self.logTerminal.yview(tk.END)
