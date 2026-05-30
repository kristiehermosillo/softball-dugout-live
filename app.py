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
    "next_gender": "Female"
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return default_data

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def rerun_app():
    st.rerun()

data = load_data()

st.set_page_config(
    page_title="Softball Dugout Live",
    page_icon="🥎",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #08111f 0%, #111827 45%, #020617 100%);
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

.big-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 22px;
}

.title {
    font-size: 64px;
    font-weight: 900;
    color: white;
    margin-bottom: 0px;
}

.subtitle {
    color: #cbd5e1;
    font-size: 22px;
    margin-top: 0px;
}

.now-batting {
    font-size: 52px;
    font-weight: 900;
    color: white;
    text-align: center;
}

.on-deck {
    font-size: 30px;
    color: #bfdbfe;
    text-align: center;
}

.small-label {
    color: #94a3b8;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 2px;
    font-weight: 700;
}

.score-number {
    font-size: 58px;
    font-weight: 900;
    color: white;
}

.score-name {
    color: #cbd5e1;
    font-size: 18px;
}

.highlight {
    background: rgba(34,197,94,0.18);
    border-radius: 14px;
    padding: 10px 14px;
    color: white;
    font-weight: 800;
}

.lineup-text {
    color: #e5e7eb;
    font-size: 18px;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

female_lineup = data["female_lineup"]
male_lineup = data["male_lineup"]
female_idx = data["current_female_index"]
male_idx = data["current_male_index"]
next_gender = data["next_gender"]

if next_gender == "Female":
    current_batter = female_lineup[female_idx]
    on_deck = male_lineup[male_idx]
    on_deck_gender = "Male"
else:
    current_batter = male_lineup[male_idx]
    on_deck = female_lineup[female_idx]
    on_deck_gender = "Female"

st.markdown("<div class='title'>🥎 Softball Dugout Live</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{data['team_name']} dugout control board</div>", unsafe_allow_html=True)

st.markdown("<div class='big-card'>", unsafe_allow_html=True)
st.markdown("<div class='small-label'>Now Batting</div>", unsafe_allow_html=True)
st.markdown(f"<div class='now-batting'>{current_batter}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='on-deck'>On deck: {on_deck} ({on_deck_gender})</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

score_col1, score_col2, info_col = st.columns(3)

with score_col1:
    st.markdown("<div class='big-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-name'>{data['team_name']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-number'>{data['home_score']}</div>", unsafe_allow_html=True)
    if st.button("Add Run for Us", use_container_width=True):
        data["home_score"] += 1
        save_data(data)
        rerun_app()
    st.markdown("</div>", unsafe_allow_html=True)

with score_col2:
    st.markdown("<div class='big-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-name'>{data['opponent']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-number'>{data['away_score']}</div>", unsafe_allow_html=True)
    if st.button("Add Run for Opponent", use_container_width=True):
        data["away_score"] += 1
        save_data(data)
        rerun_app()
    st.markdown("</div>", unsafe_allow_html=True)

with info_col:
    st.markdown("<div class='big-card'>", unsafe_allow_html=True)
    st.markdown("<div class='small-label'>Game Info</div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:white;'> {data['half']} {data['inning']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:white;'>Outs: {data['outs']}</h2>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

button_col1, button_col2, button_col3 = st.columns(3)

with button_col1:
    if st.button("Next Batter", use_container_width=True):
        if next_gender == "Female":
            data["current_female_index"] = (female_idx + 1) % len(female_lineup)
            data["next_gender"] = "Male"
        else:
            data["current_male_index"] = (male_idx + 1) % len(male_lineup)
            data["next_gender"] = "Female"
        save_data(data)
        rerun_app()

with button_col2:
    if st.button("Add Out", use_container_width=True):
        data["outs"] += 1
        if data["outs"] >= 3:
            data["outs"] = 0
            if data["half"] == "Top":
                data["half"] = "Bottom"
            else:
                data["half"] = "Top"
                data["inning"] += 1
        save_data(data)
        rerun_app()

with button_col3:
    if st.button("Reset Game", use_container_width=True):
        save_data(default_data)
        rerun_app()

st.markdown("### Lineup")

lineup_col1, lineup_col2 = st.columns(2)

with lineup_col1:
    st.markdown("#### Female Lineup")
    for i, player in enumerate(female_lineup):
        if i == female_idx and next_gender == "Female":
            st.markdown(f"<div class='highlight'>🥎 {i + 1}. {player}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='lineup-text'>{i + 1}. {player}</div>", unsafe_allow_html=True)

with lineup_col2:
    st.markdown("#### Male Lineup")
    for i, player in enumerate(male_lineup):
        if i == male_idx and next_gender == "Male":
            st.markdown(f"<div class='highlight'>🥎 {i + 1}. {player}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='lineup-text'>{i + 1}. {player}</div>", unsafe_allow_html=True)
