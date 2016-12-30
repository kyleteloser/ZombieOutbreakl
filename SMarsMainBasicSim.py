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
        self.day = 0  # starts on day 0 of landing
        self.excessPower = 0
        self.totalSolarPowerInstalled = 0  # kilo watts
        self.solarPanelsInstalled = 0
        self.solarPanelsStock = 0
        self.totalPowerConsumed = 0
        self.roverShiftsPerDay = 0
        self.roverBatteryBank = 0  # kW
        self.powerDelta = 0
        self.reservesCH4 = 0  # kg
        self.reservesO2 = 0  # kg
        self.solarHoursPerDay = 0
        self.solarIrradianceCurve = 0  # irradiance
        self.panelsInstalledPerShift = 0  # see time break down
        self.panelPowerRating = 0.0  # kW Each panel is 260 watts on Earth * 58% efficient on Mars
        self.maxDays = 0  #
        self.powerDeltaCopy = 0  # for record keeping checks
        self.numRovers = 0
        self.numBatteries = 0
        self.batterySize = 0.0  # kW
        self.batteryMinCharge = 0.0  # minimum % charge on the batteries as a floor
        self.maxBatteryBank = self.numBatteries * self.batterySize
        self.batteryBank = 0  # assume that we land with batteries fully charged
        self.fuelCellConsumption = 0.0  # kg per kW

        self.logWindow = None
        self.logTerminal = None
        self.logTerminalScroll = None
        self.header1 = None
        self.header2 = None
        self.logTerm = None
        self.headerFrame = None
        self.resourceManager = None
        self.powerFrame = None
        self.powerUsedBar = None
        self.solarPowerBar = None
        self.batteryBankBar = None
        self.resourcesFrame = None
        self.oxygenResBar = None
        self.methaneResBar = None
        self.waterResBar = None
        self.CO2ResBar = None

        self.createLogWindow(self.mainFrame)

        self.master.focus()
        self.master.bind('<Return>', lambda e: self.doReturn())
        self.master.bind('<space>', lambda e: self.doSpace())

    def doSpace(self):
        self.simLoop()

    def doReturn(self):
        self.simLoop()

    def centerWindow(self):
        w = 1000
        h = 800

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def printTerminal(self, lines):
        for line in lines:
            self.logTerminal.insert('end', line)
            self.logTerminal.select_clear(self.logTerminal.size() - 2)  # Clear the current selected item
            self.logTerminal.select_set(END)  # Select the new item
            self.logTerminal.yview(END)

    def createLogWindow(self, parent):
        self.logWindow = LabelFrame(parent, text="Log Window", borderwidth=2, relief="sunken", width=100, height=100)
        self.logTerm = Frame(self.logWindow, width=800, height=100)
        self.logTerminalScroll = Scrollbar(self.logTerm, orient=VERTICAL)
        self.logTerminalScroll.pack(side=RIGHT, fill=Y)
        self.logTerminal = Listbox(self.logTerm, width=80, height=25, yscrollcommand=self.logTerminalScroll.set)
        self.logTerminal.pack(side=LEFT, fill=BOTH)
        self.logTerminalScroll.config(command=self.logTerminal.yview)
        self.logTerm.pack(side=LEFT)
        self.logWindow.pack(fill=X, expand=1)

    def getInitialConditions(self):
        self.roverShiftsPerDay = 1  # assumes 6 hours of working and 2 hours for recharge / software updates / misc
        self.roverBatteryBank = 10000

        # kW
        self.reservesCH4 = 100  # kg
        self.reservesO2 = 100  # kg
        self.solarHoursPerDay = 7
        self.solarIrradianceCurve = 0.66
        self.panelsInstalledPerShift = 12  # see time break down
        self.panelPowerRating = 0  # kW Each panel is 260 watts on Earth * 58% efficient on Mars
        self.maxDays = 1000  # for now
        self.numRovers = 2
        self.Food = 1
        self.Zombies = 1 * 100

    def updateSim(self):
        # calculate new power installed each day
        powerPerPanel = self.Food = self.powerPerPanel
        powerConsumedEachDay = self.Zombies * self.Zombies
        self.totalPowerConsumed = powerConsumedEachDay

    def printDayStatus(self):
        # Every tenth day draw the column headers
        lines = []
        if self.day % 10 == 0:
            lines.append("Day | Power- | Solar+ ")
        lines.append(str(self.day) + " | " + str(self.totalPowerConsumed) + " | " + str(self.totalSolarPowerInstalled))
        self.printTerminal(lines)

    def simLoop(self):
        self.updateSim()  # update the calculations
        self.printDayStatus()  # do the calculations
        if self.day > self.maxDays:  # check to see if we are at the end of the sim
            self.doSimQuit()
        self.day += 1

    @staticmethod
    def doSimQuit():
        print("End of Simulation")
        sys.exit()


def main():
    root = Tk()
    app = Application(root)
    app.master.title(gGameName)
    app.getInitialConditions()
    app.mainloop()
    root.quit()


gGameName = "Real Mars Simulation"

if __name__ == '__main__':
    main()
