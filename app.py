import streamlit as st
import json
import os

DATA_FILE = "game_data.json"

default_data = {
    "team_name": "Breaking Bat",
    "opponent": "Opponent",
    "home_score": 0,
    "away_score": 0,
    "inning": 1,
    "half": "Top",
    "outs": 0,
    "current_batter_index": 0,
    "lineup": [
        "Veronica Valencia",
        "Mari Ahern",
        "Kristie Hermosillo",
        "Kaitlyn Garza",
        "Natalie Elias",
        "Raymond Fierro",
        "Benjamin Almendarez",
        "Christian Downs",
        "Miguel Rodriguez",
        "Brandon Diggs",
        "Aaron Quinn"
    ]
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return default_data

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

data = load_data()

st.set_page_config(
    page_title="Softball Dugout Live",
    layout="centered"
)

st.title("🥎 Softball Dugout Live")

page = st.sidebar.radio(
    "Choose View",
    ["Dugout View", "Scorekeeper"]
)

lineup = data["lineup"]
current_index = data["current_batter_index"]

current_batter = lineup[current_index]

next_index = current_index + 1
if next_index >= len(lineup):
    next_index = 0

on_deck = lineup[next_index]

if page == "Dugout View":
    st.header(data["team_name"])

    st.subheader("Score")
    col1, col2 = st.columns(2)
    col1.metric(data["team_name"], data["home_score"])
    col2.metric(data["opponent"], data["away_score"])

    st.subheader("Game Info")
    st.write(f"Inning: {data['half']} {data['inning']}")
    st.write(f"Outs: {data['outs']}")

    st.subheader("Now Batting")
    st.success(current_batter)

    st.subheader("On Deck")
    st.info(on_deck)

    st.subheader("Lineup")
    for number, player in enumerate(lineup, start=1):
        if number == current_index + 1:
            st.write(f"🥎 {number}. {player}")
        else:
            st.write(f"{number}. {player}")

if page == "Scorekeeper":
    st.header("Scorekeeper Controls")

    st.subheader("Score")
    col1, col2 = st.columns(2)

    if col1.button("Add Run for Us"):
        data["home_score"] = data["home_score"] + 1
        save_data(data)
        st.rerun()

    if col2.button("Add Run for Opponent"):
        data["away_score"] = data["away_score"] + 1
        save_data(data)
        st.rerun()

    st.subheader("Batting")
    st.write(f"Current batter: {current_batter}")
    st.write(f"On deck: {on_deck}")

    if st.button("Next Batter"):
        data["current_batter_index"] = next_index
        save_data(data)
        st.rerun()

    st.subheader("Outs")
    st.write(f"Current outs: {data['outs']}")

    if st.button("Add Out"):
        data["outs"] = data["outs"] + 1
        if data["outs"] >= 3:
            data["outs"] = 0
            if data["half"] == "Top":
                data["half"] = "Bottom"
            else:
                data["half"] = "Top"
                data["inning"] = data["inning"] + 1
        save_data(data)
        st.rerun()

    st.subheader("Reset")
    if st.button("Reset Game"):
        data = default_data
        save_data(data)
        st.rerun()
