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

def get_batters(data):
    female_lineup = data["female_lineup"]
    male_lineup = data["male_lineup"]
    female_idx = data["current_female_index"]
    male_idx = data["current_male_index"]
    next_gender = data["next_gender"]

    if next_gender == "Female":
        current_batter = female_lineup[female_idx]
        on_deck = male_lineup[male_idx]
        in_the_hole = female_lineup[(female_idx + 1) % len(female_lineup)]
    else:
        current_batter = male_lineup[male_idx]
        on_deck = female_lineup[female_idx]
        in_the_hole = male_lineup[(male_idx + 1) % len(male_lineup)]

    return current_batter, on_deck, in_the_hole

def next_batter(data):
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

        if data["half"] == "Top":
            data["half"] = "Bottom"
        else:
            data["half"] = "Top"
            data["inning"] += 1

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
    padding-top: 1.5rem;
    max-width: 1150px;
}

.main-title {
    font-size: 68px;
    font-weight: 900;
    color: white;
    line-height: 1;
    margin-bottom: 12px;
}

.subtitle {
    color: #cbd5e1;
    font-size: 22px;
    margin-bottom: 30px;
}

.card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 22px;
}

.batter-card {
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 28px;
    padding: 34px;
    margin-bottom: 26px;
    text-align: center;
}

.small-label {
    color: #94a3b8;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 2px;
    font-weight: 800;
}

.now-batting {
    font-size: 72px;
    font-weight: 900;
    color: white;
    line-height: 1.05;
    margin-bottom: 28px;
}

.on-deck {
    font-size: 40px;
    color: #bfdbfe;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 24px;
}

.score-name {
    color: #cbd5e1;
    font-size: 18px;
    font-weight: 700;
}

.score-number {
    font-size: 64px;
    font-weight: 900;
    color: white;
    line-height: 1;
    margin-top: 12px;
}

.game-info {
    color: white;
    font-size: 40px;
    font-weight: 900;
    line-height: 1.2;
}

.lineup-text {
    color: #e5e7eb;
    font-size: 20px;
    line-height: 1.8;
}

.highlight {
    background: rgba(34,197,94,0.22);
    border-radius: 14px;
    padding: 10px 14px;
    color: white;
    font-weight: 900;
    font-size: 20px;
    margin: 4px 0;
}

h3, h4 {
    color: white !important;
}

.stButton > button {
    border-radius: 12px;
    height: 48px;
    font-weight: 800;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

current_batter, on_deck, in_the_hole = get_batters(data)

st.markdown("<div class='main-title'>🥎 Softball Dugout Live</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{data['team_name']} dugout control board</div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class='batter-card'>
        <div class='small-label'>NOW BATTING</div>
        <div class='now-batting'>{current_batter}</div>

        <div class='small-label'>ON DECK</div>
        <div class='on-deck'>{on_deck}</div>

        <div class='small-label'>IN THE HOLE</div>
        <div class='on-deck'>{in_the_hole}</div>
    </div>
    """,
    unsafe_allow_html=True
)

score_col1, score_col2, info_col = st.columns(3)

with score_col1:
    st.markdown(
        f"""
        <div class='card'>
            <div class='score-name'>{data['team_name']}</div>
            <div class='score-number'>{data['home_score']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("+ Run for Us", use_container_width=True):
        data["home_score"] += 1
        save_data(data)
        rerun_app()

with score_col2:
    st.markdown(
        f"""
        <div class='card'>
            <div class='score-name'>{data['opponent']}</div>
            <div class='score-number'>{data['away_score']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("+ Run for Opponent", use_container_width=True):
        data["away_score"] += 1
        save_data(data)
        rerun_app()

with info_col:
    st.markdown(
        f"""
        <div class='card'>
            <div class='small-label'>GAME INFO</div>
            <div class='game-info'>{data['half']} {data['inning']}</div>
            <div class='game-info'>Outs: {data['outs']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

button_col1, button_col2, button_col3 = st.columns(3)

with button_col1:
    if st.button("➡ Next Batter", use_container_width=True):
        next_batter(data)
        save_data(data)
        rerun_app()

with button_col2:
    if st.button("+ Out", use_container_width=True):
        add_out(data)
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
    for i, player in enumerate(data["female_lineup"]):
        if i == data["current_female_index"] and data["next_gender"] == "Female":
            st.markdown(f"<div class='highlight'>🥎 {i + 1}. {player}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='lineup-text'>{i + 1}. {player}</div>", unsafe_allow_html=True)

with lineup_col2:
    st.markdown("#### Male Lineup")
    for i, player in enumerate(data["male_lineup"]):
        if i == data["current_male_index"] and data["next_gender"] == "Male":
            st.markdown(f"<div class='highlight'>🥎 {i + 1}. {player}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='lineup-text'>{i + 1}. {player}</div>", unsafe_allow_html=True)
