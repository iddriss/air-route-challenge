'''
Author
---------
Iddriss Raaj (2022)

Summary
--------
Functions for finding the shortes route
'''
import argparse
import functions as fn
import math

# prepare to read from terminal

parser = argparse.ArgumentParser()
parser.add_argument("inputfile", action="store", help="Input file location")
arg = parser.parse_args().inputfile

inputfilename = arg
# inputfilename = "abc.txt"
outputfilename = inputfilename[:-4]+"_output.txt"
radiusOfEarth = 6378.137  # in km

source = []
destination = []

# open input file for parameters
with open(inputfilename, newline="") as file:
    lines = file.readlines()
    if len(lines) < 2:
        raise ValueError(f"Your input file is not valid")
    else:
        source = lines[0].rstrip().split(",")
        destination = lines[1].rstrip().split(",")

    if len(source) < 2 or len(destination) < 2:
        raise ValueError(f"Your input file is not valid")


optimalRoute = fn.optimalRoute(source, destination)

totalDistance = fn.totalDistance(radiusOfEarth, optimalRoute)

showTotalDistance = True if totalDistance > 0 else False
showOptimalityCriteria = True

# open outputfile for writing
with open(outputfilename, "w") as outfile:
    counter = 0
    stops = 0

    print("=> writing data to output")
    if len(optimalRoute) > 0:
        for i in optimalRoute:
            counter += 1
            stops += int(i[7])
            outfile.write(
                f"{counter}. {i[0]} from {i[2]} to {i[4]} {i[7]} stops\n")

        outfile.write(f"Total flights: {len(optimalRoute)}\n")
        outfile.write(f"Total additional stops: {stops}\n")
        if showTotalDistance:
            outfile.write(f"Total distance: {math.ceil(totalDistance)} km\n")

        outfile.write(f"Optimality criteria: flights\n")
    else:
        outfile.write("Unsupported request")
