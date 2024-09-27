import pandas as pd
# import seaborn as sns
from matplotlib import pyplot as plt
import fastf1 as ff1
import fastf1.plotting
from fastf1.core import Laps

# load session from qualifying session from 1st race in 2024
race = ff1.get_session(2021, 22, "R")
race.load()

# get the laptimes from top 2 finishers (VER and HAM)
top2 = race.drivers[:2]
# print(top2)
driver_laps = race.laps.pick_drivers(top2).pick_quicklaps()
driver_laps = driver_laps.reset_index()

# plot drivers by finishing order using driver abbreviation
finishing_order = [race.get_driver(i)["Abbreviation"] for i in top2]
print(finishing_order)