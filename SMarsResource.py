# Resource

# ID
# Name
# Units
# Icon

# Assume icons are 32x32

# Need to load this data from a csv file

import csv


class Resource:
    def __init__(self, rid):
        # Look up name, Units, and Icon from CSV file to populate the resource
        self.rid = rid


class ResourceManager:
    sResources = {}

    def __init__(self):
        self.resourcePath = './assets/Resources.csv'
        with open(self.resourcePath, 'r') as csvfile:
            resourceReader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            rowNumber = 0
            for row in resourceReader:
                if rowNumber > 0:  # skip the header row
                    print(rowNumber)
                    print(row)
                    r = Resource(int(row[0]))
                    r.name = row[1]
                    r.units = row[2]
                    r.icon = './assets/' + row[3]
                    r.barColor = row[4]
                    self.sResources[r.name] = r
                rowNumber += 1

        print(" Check Resources")
        for r in self.sResources:
            print(r)
