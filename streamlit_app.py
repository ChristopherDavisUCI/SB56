import streamlit as st
import numpy as np
import pandas as pd
import nfl_data_py as nfl

st.title("Super Bowl 56")

df_schedule = nfl.import_schedules([2021])
df_players = nfl.import_rosters([2021])
df_pbp = nfl.import_pbp_data([2021]) #play-by-play

st.write(df_pbp.head())

teams = ["LA", "CIN"] + [team for team in df_schedule.home_team.unique() if team not in ["LA","CIN"]]

team = st.selectbox("Team", teams)

df_wr = df_players[["player_name", "player_id"]][(df_players.position=="WR") & (df_players.team==team)]

wrs = df_wr.set_index("player_name")["player_id"]

wr = st.selectbox("Receiver", wrs)
