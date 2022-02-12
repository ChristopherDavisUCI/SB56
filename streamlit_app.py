import streamlit as st
import numpy as np
import pandas as pd
import nfl_data_py as nfl

st.title("Super Bowl 56")

df_schedule = nfl.import_schedules([2021])
df_players = nfl.import_rosters([2021])
df_pbp = nfl.import_pbp_data([2021]) #play-by-play

st.write(df_pbp.head())
