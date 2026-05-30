import streamlit as st
import json
import os

DATA_FILE = "game_data.json"

# Default game data
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
    "next_gender": "Female"
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return default_data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def rerun():
    st.experimental_rerun()

data = load_data()

st.set_page_config(page_title="Softball Dugout Live", page_icon="🥎", layout="wide")

# Custom CSS for a sleek dashboard look
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #08111f 0%, #111827 45%, #020617 100%); }
.block-container { max-width: 1200px; padding-top: 1rem; }

.title { font-size: 64px; font-weight: 900; color: white; margin-bottom: 0px; }
.subtitle { font-size: 20px; color: #cbd5e1; margin-bottom: 1rem; }

.card { background: rgba(255,255,255,0.08); border-radius: 20px; padding: 25px; margin-bottom: 15px; text-align: center; }

.now-batting { font-size: 72px; font-weight: 900; color: white; margin: 15px 0; }
.on-deck { font-size: 40px; font-weight: 800; color: #bfdbfe; margin: 10px 0; }

.metric-card { background: rgba(255,255,255,0.08); border-radius: 20px; padding: 20px; text-align: center; }
.metric-number { font-size: 60px; font-weight: 900; color: white; }
.metric-label { color: #cbd5e1; font-size: 18px; }

.button-wide > button { height: 50px; font-size: 16px; font-weight: 800; border-radius: 12px; }
.lineup-title { font-size: 24px; font-weight: 800; color: #cbd5e1; margin-top: 20px; margin-bottom: 10px; }
.lineup-item { font-size: 18px; color: #e5e7eb; padding: 2px; }
.highlight { background: rgba(34,197,94,0.22); border-radius: 12px; padding: 5px 10px; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# Functions to get current, on-deck, and in-the-hole
def get_batters(data):
    f_idx = data["current_female_index"]
    m_idx = data["current_male_index"]
    next_gender = data["next_gender"]
    female_lineup = data["female_lineup"]
    male_lineup = data["male_lineup"]

    if next_gender == "Female":
        current = female_lineup[f_idx]
        on_deck = male_lineup[m_idx]
        in_hole = female_lineup[(f_idx + 1) % len(female_lineup)]
    else:
        current = male_lineup[m_idx]
        on_deck = female_lineup[f_idx]
        in_hole = male_lineup[(m_idx + 1) % len(male_lineup)]
    return current, on_deck, in_hole

def advance_batter(data):
    if data["next_gender"] == "Female":
        data["current_female_index"] = (data["current_female_index"] + 1) % len(data["female_lineup"])
        data["next_gender"] = "Male"
    else:
        data["current_male_index"] = (data["current_male_index"] + 1) % len(data["male_lineup"])
        data["next_gender"] = "Female"

def add_out(data):
    data["outs"] += 1
    if data["outs"] >= 3:
        data["outs"] = 0
        data["half"] = "Bottom" if data["half"] == "Top" else "Top"
        if data["half"] == "Top":
            data["inning"] += 1

current, on_deck, in_hole = get_batters(data)

# Header
st.markdown(f"<div class='title'>🥎 Softball Dugout Live</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{data['team_name']} dugout control board</div>", unsafe_allow_html=True)

# Batting section with clear separation
bat_col1, bat_col2 = st.columns([2,2])
with bat_col1:
    st.markdown(f"<div class='card'><div class='now-batting'>NOW BATTING<br>{current}</div></div>", unsafe_allow_html=True)
with bat_col2:
    st.markdown(f"<div class='card'><div class='on-deck'>ON DECK<br>{on_deck}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'><div class='on-deck'>IN THE HOLE<br>{in_hole}</div></div>", unsafe_allow_html=True)

# Scoreboard
score_col1, score_col2, info_col = st.columns(3)
with score_col1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>{data['team_name']}</div><div class='metric-number'>{data['home_score']}</div></div>", unsafe_allow_html=True)
    if st.button("+ Run for Us", key="run_us", use_container_width=True):
        data["home_score"] += 1; save_data(data); rerun()
with score_col2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>{data['opponent']}</div><div class='metric-number'>{data['away_score']}</div></div>", unsafe_allow_html=True)
    if st.button("+ Run for Opponent", key="run_opp", use_container_width=True):
        data["away_score"] += 1; save_data(data); rerun()
with info_col:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>GAME INFO</div><div class='metric-number'>{data['half']} {data['inning']}<br>Outs: {data['outs']}</div></div>", unsafe_allow_html=True)

# Action buttons
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.button("➡ Next Batter", key="next", use_container_width=True):
        advance_batter(data); save_data(data); rerun()
with btn_col2:
    if st.button("+ Out", key="out", use_container_width=True):
        add_out(data); save_data(data); rerun()
with btn_col3:
    if st.button("Reset Game", key="reset", use_container_width=True):
        save_data(default_data); rerun()

# Lineups
st.markdown("<div class='lineup-title'>Female Lineup</div>", unsafe_allow_html=True)
for i, p in enumerate(data["female_lineup"]):
    highlight = "highlight" if i == data["current_female_index"] and data["next_gender"] == "Female" else ""
    st.markdown(f"<div class='lineup-item {highlight}'>{i+1}. {p}</div>", unsafe_allow_html=True)

st.markdown("<div class='lineup-title'>Male Lineup</div>", unsafe_allow_html=True)
for i, p in enumerate(data["male_lineup"]):
    highlight = "highlight" if i == data["current_male_index"] and data["next_gender"] == "Male" else ""
    st.markdown(f"<div class='lineup-item {highlight}'>{i+1}. {p}</div>", unsafe_allow_html=True)
