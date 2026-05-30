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
    "female_lineup": [
        "Veronica Valencia",
        "Mari Ahern",
        "Kristie Hermosillo",
        "Kaitlyn Garza",
        "Natalie Elias"
    ],
    "male_lineup": [
        "Raymond Fierro",
        "Benjamin Almendarez",
        "Christian Downs",
        "Miguel Rodriguez",
        "Brandon Diggs",
        "Aaron Quinn"
    ],
    "current_female_index": 0,
    "current_male_index": 0,
    "next_gender": "Female"  # start with Female
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

# Determine current batter and on-deck
female_lineup = data["female_lineup"]
male_lineup = data["male_lineup"]
female_idx = data["current_female_index"]
male_idx = data["current_male_index"]
next_gender = data["next_gender"]

if next_gender == "Female":
    current_batter = female_lineup[female_idx]
    next_gender_for_deck = "Male"
    on_deck_idx = male_idx
    on_deck = male_lineup[on_deck_idx] if male_lineup else None
else:
    current_batter = male_lineup[male_idx]
    next_gender_for_deck = "Female"
    on_deck_idx = female_idx
    on_deck = female_lineup[on_deck_idx] if female_lineup else None

# Dugout View
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
    st.success(f"{current_batter} ({next_gender})")

    st.subheader("On Deck")
    if on_deck:
        st.info(f"{on_deck} ({next_gender_for_deck})")
    else:
        st.info("None")

    st.subheader("Lineup")
    st.write("Female Lineup:")
    for i, player in enumerate(female_lineup, start=1):
        prefix = "🥎" if i-1 == female_idx and next_gender=="Female" else ""
        st.write(f"{prefix}{i}. {player}")
    st.write("Male Lineup:")
    for i, player in enumerate(male_lineup, start=1):
        prefix = "🥎" if i-1 == male_idx and next_gender=="Male" else ""
        st.write(f"{prefix}{i}. {player}")

# Scorekeeper View
if page == "Scorekeeper":
    st.header("Scorekeeper Controls")

    st.subheader("Score")
    col1, col2 = st.columns(2)
    if col1.button("Add Run for Us"):
        data["home_score"] += 1
        save_data(data)
        st.experimental_rerun()
    if col2.button("Add Run for Opponent"):
        data["away_score"] += 1
        save_data(data)
        st.experimental_rerun()

    st.subheader("Batting")
    st.write(f"Current batter: {current_batter} ({next_gender})")
    st.write(f"On deck: {on_deck} ({next_gender_for_deck})")

    if st.button("Next Batter"):
        # Advance the proper index and switch gender
        if next_gender == "Female":
            data["current_female_index"] = (female_idx + 1) % len(female_lineup)
            data["next_gender"] = "Male"
        else:
            data["current_male_index"] = (male_idx + 1) % len(male_lineup)
            data["next_gender"] = "Female"
        save_data(data)
        st.experimental_rerun()

    st.subheader("Outs")
    st.write(f"Current outs: {data['outs']}")
    if st.button("Add Out"):
        data["outs"] += 1
        if data["outs"] >= 3:
            data["outs"] = 0
            if data["half"] == "Top":
                data["half"] = "Bottom"
            else:
                data["half"] = "Top"
                data["inning"] += 1
        save_data(data)
        st.experimental_rerun()

    st.subheader("Reset")
    if st.button("Reset Game"):
        data = default_data
        save_data(data)
        st.experimental_rerun()
