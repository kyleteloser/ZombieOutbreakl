# library imports
import sys
import tkinter as tk

# SMars imports
import SMarsResourceBar
import SMarsResource
import LogWindow
import MapWindow
import RoverWindow


class Application(tk.Frame):
    def __init__(self, master=None):
        self.mainFrame = tk.Frame.__init__(self, master)

        self.day = 0  # starts on day 0 of landing
        self.excessPower = 0
        self.totalSolarPowerInstalled = 0  # kilo watts
        self.solarPanelsInstalled = 0
        self.solarPanelsStock = 0
        self.totalPowerConsumed = 0
        self.roverShiftsPerDay = 0
        self.roverBatteryBank = 0  # kW
        self.powerDelta = 0
        self.Food = 0  # kg
        self.Water = 0  # kg
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
        self.mapWindow = None

        self.roverWindow = None

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

        self.getInitialConditions()
        self.resourceManager = SMarsResource.ResourceManager()
        self.setupUX()

    def setupUX(self):
        self.setupPowerBars(self.mainFrame)
        self.powerFrame.grid(row=0, column=0)

        self.roverWindow = RoverWindow.RoverWindow(self.mainFrame, self.numRovers)
        self.roverWindow.roverWindow.grid(row=0, column=1)

        self.mapWindow = MapWindow.MapWindow(self.mainFrame)
        self.mapWindow.mapWindow.grid(row=1, column=0)

        self.logWindow = LogWindow.LogWindow(self.mainFrame)
        self.logWindow.logWindow.grid(row=1, column=1, sticky=tk.N)

        self.setupResourceBars(self.mainFrame)
        self.resourcesFrame.grid(row=1, column=2, sticky=tk.N)

        self.master.focus()
        self.master.bind('<Return>', lambda e: self.doReturn())
        self.master.bind('<space>', lambda e: self.doSpace())

    def setupPowerBars(self, parent):
        mW = 1000.0  # 1000 kW
        # solarPower Stock
        self.powerFrame = tk.LabelFrame(parent, text="Power", borderwidth=2, relief="sunken", padx=10, pady=5)
        self.powerUsedBar = SMarsResourceBar.ResourceBar(self.powerFrame,
                                                         self.resourceManager.sResources['Survivors Left'], 120, mW,
                                                         self.totalPowerConsumed, True)
        self.solarPowerBar = SMarsResourceBar.ResourceBar(self.powerFrame,
                                                          self.resourceManager.sResources['Dead Humans'],
                                                          120, mW, self.totalSolarPowerInstalled, True)
        self.batteryBankBar = SMarsResourceBar.ResourceBar(self.powerFrame,
                                                           self.resourceManager.sResources['ZombieDead'], 120, 5 * mW,
                                                           self.batteryBank, True)

    def setupResourceBars(self, parent):
        mT = 1000.0  # 1000 kgs
        self.resourcesFrame = tk.LabelFrame(parent, text="Resources", borderwidth=2, relief="sunken", padx=10,
                                            pady=5)
        self.oxygenResBar = SMarsResourceBar.ResourceBar(self.resourcesFrame,
                                                         self.resourceManager.sResources['Food'],
                                                         100, self.Water, self.Water, False)
        self.methaneResBar = SMarsResourceBar.ResourceBar(self.resourcesFrame,
                                                          self.resourceManager.sResources['Water'],
                                                          100, self.Food, self.Food, False)
        self.waterResBar = SMarsResourceBar.ResourceBar(self.resourcesFrame, self.resourceManager.sResources['Water'],
                                                        100, mT, 1, False)
        self.CO2ResBar = SMarsResourceBar.ResourceBar(self.resourcesFrame, self.resourceManager.sResources['ZombieDead'], 100,
                                                      mT, 1, False)

    def doSpace(self):
        self.simLoop()

    def doReturn(self):
        self.simLoop()

    def getInitialConditions(self):
        self.day = 0  # starts on day 0 of landing
        self.excessPower = 10000
        self.totalSolarPowerInstalled = 0  # kilo watts
        self.solarPanelsInstalled = 0
        self.solarPanelsStock = 0
        self.totalPowerConsumed = 1
        self.roverShiftsPerDay = 3  # assumes 6 hours of working and 2 hours for recharge / software updates / misc
        self.roverBatteryBank = 1000    # kW
        self.Food = 133  # kg
        self.Water = 133  # kg
        self.solarHoursPerDay = 7
        self.solarIrradianceCurve = 0.66
        self.panelsInstalledPerShift = 12  # see time break down
        self.panelPowerRating = 0.150  # kW Each panel is 260 watts on Earth * 58% efficient on Mars
        self.maxDays = 100  # for now
        self.powerDeltaCopy = 0  # for record keeping checks
        self.numRovers = 1
        self.numBatteries = 0
        self.batterySize = 13.5


        # kW
        self.batteryMinCharge = 0.5  # minimum % charge on the batteries as a floor
        self.maxBatteryBank = self.numBatteries * self.batterySize
        self.batteryBank = self.maxBatteryBank  # assume that we land with batteries fully charged
        self.fuelCellConsumption = 0.01  # kg per kW

    def updateSim(self):
        # Check for fail condition
        if (self.Food < 0) or (self.Water < 0):
            self.doSimQuit()

        # calculate new power installed each day
        powerPerPanel = self.panelPowerRating * self.solarHoursPerDay * self.solarIrradianceCurve
        powerInstalledPerDay = self.numRovers * self.roverShiftsPerDay * self.panelsInstalledPerShift * powerPerPanel
        self.totalSolarPowerInstalled += powerInstalledPerDay

        # calculate power consumed each day
        powerConsumedEachDay = self.numRovers * self.roverBatteryBank * self.roverShiftsPerDay
        self.totalPowerConsumed = powerConsumedEachDay

        # do the power accounting
        self.powerDelta = self.totalSolarPowerInstalled - self.totalPowerConsumed
        self.powerDeltaCopy = self.powerDelta

        self.excessPower = 0

        # if powerDelta is positive, we have extra energy, if it is negative we need from storage
        if self.powerDelta >= 0:
            print("Extra Power!")
            # add the extra power to the battery bank
            self.batteryBank += self.powerDelta
            # We cannot charge over the max size of the battery bank
            if self.batteryBank > self.maxBatteryBank:
                # find out what the excess power is after charging the batteries to full
                self.powerDelta = self.batteryBank - self.maxBatteryBank
                # find out what the excess power is after charging the batteries to full
                self.batteryBank = self.maxBatteryBank  # set the current bank to max bank
                # self.powerDelta now contains excess power available for other systems
                self.excessPower = self.powerDelta

        else:
            # take power from batteries first, second from fuel cells
            batteryAvailable = self.batteryBank - self.maxBatteryBank * self.batteryMinCharge

            if batteryAvailable > abs(self.powerDelta):  # Do we have more available than we need?
                self.batteryBank += self.powerDelta  # great take it
                self.powerDelta = 0  # set the gap to 0
            else:
                self.powerDelta += batteryAvailable  # take what is available
                # now we should be at the floor of the reserves
                self.batteryBank = self.maxBatteryBank * self.batteryMinCharge

                # the remaining energy is needed from the CH4/O2 fuel cell
                fuelUsed = self.fuelCellConsumption * abs(self.powerDeltaCopy)  # determine the kg of fuel consumed

                # Burns CH4 + 2O2  = > CO2 + 2H2O
                # O2 is approx 2x as heavy as CH4, and we need to burn 2x O2 for every CH4, so 4kg of O2
                self.Food -= fuelUsed
                self.Water-= fuelUsed
                self.powerDelta = 0  # and now we are done paying for our power


                if self.Food < 0:
                    self.logWindow.printTerminal(["Ran out of Food!"])
                if self.Water < 0:
                    self.logWindow.printTerminal(["Ran out of Water!"])

    def getUserInputs(self):
        # Text Entries
        self.numRovers = int(self.roverWindow.numRoverEntryVar.get())

    def updateUX(self):
        # Power Bars
        self.solarPowerBar.updateValue(self.totalSolarPowerInstalled)
        self.powerUsedBar.updateValue(self.totalPowerConsumed)
        self.batteryBankBar.updateValue(self.batteryBank)

        # Resource Bars
        self.oxygenResBar.updateValue(self.Water)
        self.methaneResBar.updateValue(self.Food)
        self.waterResBar.updateValue(0)
        self.CO2ResBar.updateValue(0)

    def printDayStatus(self):
        status = [[self.day, self.totalPowerConsumed, self.totalSolarPowerInstalled,
                   self.powerDeltaCopy, self.batteryBank, self.Food, self.Water]]
        statusLine = []
        for s in status:
            statusLine = "{:4d} {:8.1f} {:8.1f} {:8.1f} {:8.1f} {:8.1f} {:8.1f}".format(*s)

        if len(statusLine) > 0:
            self.logWindow.printTerminal([statusLine])

    def simLoop(self):
        self.getUserInputs()
        self.updateSim()  # update the calculations

        self.updateUX()
        self.printDayStatus()  # print the daily status

        if self.day > self.maxDays:  # check to see if we are at the end of the sim
            self.doSimQuit()
        self.day += 1

    @staticmethod
    def doSimQuit():
        print("End of Simulation")
        sys.exit()


def main():
    root = tk.Tk()
    app = Application(root)
    app.master.title(gGameName)
    app.updateUX()
    app.mainloop()
    root.quit()


gGameName = "Real Mars Simulation"

if __name__ == '__main__':
    main()
