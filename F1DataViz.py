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