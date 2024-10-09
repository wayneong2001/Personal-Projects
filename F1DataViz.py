# creating a plot that compares data from max verstappen and lewis hamilton (top 2 finishers in Abu Dhabi Grand Prix 2021)
# using fastf1 module and pyplot to compare their laptimes in correlation with their tire data
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import fastf1 as ff1
import fastf1.plotting
from fastf1.core import Laps

# load session from qualifying session from 1st race in 2024
race = ff1.get_session(2021, 22, "R")
race.load()

# use fastf1 color palette for graph
ff1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False,
                          color_scheme='fastf1')

# get the laptimes from top 2 finishers (VER and HAM)
top2 = race.drivers[:2]
# print(top2)
driver_laps = race.laps.pick_drivers(top2).pick_quicklaps()
driver_laps = driver_laps.reset_index()

# plot drivers by finishing order using driver abbreviation
finishing_order = [race.get_driver(i)["Abbreviation"] for i in top2]
print(finishing_order)

# create the figure
fig, ax = plt.subplots(figsize=(10, 5))

# Seaborn doesn't have proper timedelta support,
# so we have to convert timedelta to float (in seconds)
driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

sns.violinplot(data=driver_laps,
               x="Driver",
               y="LapTime(s)",
               hue="Driver",
               inner=None,
               density_norm="area",
               order=finishing_order,
               palette=fastf1.plotting.get_driver_color_mapping(session=race)
               )

sns.swarmplot(data=driver_laps,
              x="Driver",
              y="LapTime(s)",
              order=finishing_order,
              hue="Compound",
              palette=fastf1.plotting.get_compound_mapping(session=race),
              hue_order=["SOFT", "MEDIUM", "HARD"],
              linewidth=0,
              size=4,)

# adding labels to make chart more aesthetic
ax.set_xlabel("Driver")
ax.set_ylabel("Lap Time (s)")
plt.suptitle("2021 Abu Dhabi Grand Prix Lap Time Distributions")
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()

# creating dataframes from fastf1 module to extract telemetry data from 2021 Abu Dhabi qualifying from max verstappen
# and lewis hamilton which will be extracted as csvs and used for visualization of lap time in tableau

# loading qualifying data from 2021 abu dhabi gp
session = ff1.get_session(2021, 22, "Q")
session.load()

# loading lap from ver and ham
VerQLap = session.laps.pick_driver("VER").pick_fastest()
HamQLap = session.laps.pick_driver("HAM").pick_fastest()

# get telemetry for each driver on their qualifying lap
VER = VerQLap.get_telemetry()
HAM = HamQLap.get_telemetry()

# making throttle 100 and brake -100 to make it easier to visualize in tableau later
HAM["Brake"] = HAM["Brake"].replace({True: 100, False: 0})
HAM["Pedal"] = HAM["Throttle"] - HAM["Brake"]
VER["Brake"] = VER["Brake"].replace({True: 100, False: 0})
VER["Pedal"] = VER["Throttle"] - VER["Brake"]

# export telemetry data from qualifying to current working directory
# VER.to_csv("ver_tel_q_ad.csv")
# HAM.to_csv("ham_tel_q_ad.csv")

