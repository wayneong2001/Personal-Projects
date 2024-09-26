import pandas as pd
import fastf1 as ff1
from fastf1.core import Laps

# load session from qualifying session from 1st race in 2024
session = ff1.get_session(2024, 1, "Q")
session.load()