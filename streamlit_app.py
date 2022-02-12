import streamlit as st
import numpy as np
import pandas as pd
import nfl_data_py as nfl

st.title("Longest Receptions")

df_schedule = nfl.import_schedules([2021])
df_players = nfl.import_rosters([2021])
df_pbp = nfl.import_pbp_data([2021]) #play-by-play

def get_games(team):
    return df_schedule.game_id[(df_schedule.home_team == team)|(df_schedule.away_team == team)]

# Example: get_player_id("Chase","CIN")
def get_player_id(player,team):
    return df_players[(df_players.last_name==player) &(df_players.team == team)].player_id.item()

def get_longest_reception(player_id, team):
    games = get_games(team)
    rec_dict = {}
    for game in games:
        df_temp = df_pbp[df_pbp.game_id==game]
        df_temp2 = df_temp[df_temp.receiver_player_id == player_id].sort_values("receiving_yards",ascending=False).copy()
        if len(df_temp2) > 0:
            ser = df_temp2.iloc[0]
            try:
                rec_dict[f"Week {ser['week']}"] = int(ser['receiving_yards'])
            except ValueError:
                # ignore nan values
                pass
    rec_series = pd.Series(rec_dict, name="Yards")
    return pd.Series(rec_dict)

teams = ["LA", "CIN"] + sorted([team for team in df_schedule.home_team.unique() if team not in ["LA","CIN"]])

team = st.selectbox("Team", teams, index=0)

df_wr = df_players[["player_name", "player_id"]][(df_players.position=="WR") & (df_players.team==team)]

wrs = df_wr.set_index("player_name")["player_id"]

wr = st.selectbox("Receiver", wrs.index)

rec_series = get_longest_reception(wrs[wr], team)

st.write(f"The median longest reception for {wr} is {rec_series.median()} yards.")

col1, col2 = st.columns(2)

with col1:
    st.header(f"Longest reception by week for {wr}:")
    st.table(rec_series)

with col2:
    st.header("Sorted list of longest receptions:")
    st.table(rec_series.sort_values(ascending=False))