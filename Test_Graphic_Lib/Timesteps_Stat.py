import os
import sys
import pylab
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
from PIL import Image

#%%%%%%%%%%%%%%%%%%%%%%%%%
# SAVE GRAPHIC LIKE IMAGE#
#%%%%%%%%%%%%%%%%%%%%%%%%%
def saveFigure(descr):
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, sys.argv[1]+"/")
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    pyplot.savefig(results_dir + sys.argv[1]+descr, format="jpg")


# Graphic's different design
pyplot.style.use('ggplot')

# Reading the dataset about the current input for each year from 2005 to 2016
series2 = pd.read_csv("TOTAL_timesteps_dataset.csv", usecols=["time", "Conf", sys.argv[1]])
# Initialize the graphic's figure
fig2 = pyplot.figure()
ax = fig2.add_subplot(111)

# Set the x axis tick
series2_origin = series2[:]

configurations = ["BT1_A3", "BT1_A6", "BT1_A9", "BT1_A12", "BT3_A3", "BT3_A6", "BT3_A9", "BT3_A12"]

for conf in configurations:
    series_temp = series2[series2["Conf"] == conf]
    print()
    pyplot.plot(series_temp["time"], series_temp[sys.argv[1]], linewidth=2, alpha=0.8, label = series_temp["Conf"].iloc[0])

ax.legend(loc=4, ncol=1, fancybox=True, shadow=True)
pyplot.title(sys.argv[1]+ ": Stats over timesteps between different configurations")
pyplot.show()
#saveFigure("_Years.jpg")