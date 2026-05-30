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

def get_batters(data):
    female_lineup = data["female_lineup"]
    male_lineup = data["male_lineup"]
    female_idx = data["current_female_index"]
    male_idx = data["current_male_index"]

    if data["next_gender"] == "Female":
        current = female_lineup[female_idx]
        on_deck = male_lineup[male_idx]
        in_the_hole = female_lineup[(female_idx + 1) % len(female_lineup)]
    else:
        current = male_lineup[male_idx]
        on_deck = female_lineup[female_idx]
        in_the_hole = male_lineup[(male_idx + 1) % len(male_lineup)]

    return current, on_deck, in_the_hole

def next_batter(data):
    if data["next_gender"] == "Female":
        data["current_female_index"] = (data["current_female_index"] + 1) % len(data["female_lineup"])
        data["next_gender"] = "Male"
    else:
        data["current_male_index"] = (data["current_male_index"] + 1) % len(data["male_lineup"])
        data["next_gender"] = "Female"

def previous_batter(data):
    if data["next_gender"] == "Female":
        data["current_male_index"] = (data["current_male_index"] - 1) % len(data["male_lineup"])
        data["next_gender"] = "Male"
    else:
        data["current_female_index"] = (data["current_female_index"] - 1) % len(data["female_lineup"])
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

data = load_data()

st.set_page_config(
    page_title="Softball Dugout Live",
    page_icon="🥎",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #08111f 0%, #111827 50%, #020617 100%);
}

.block-container {
    padding-top: 0.75rem;
    padding-bottom: 1rem;
    max-width: 1180px;
}

.main-title {
    font-size: clamp(34px, 5vw, 56px);
    font-weight: 900;
    color: white;
    line-height: 1.05;
    margin-bottom: 6px;
}

.subtitle {
    color: #cbd5e1;
    font-size: clamp(16px, 2vw, 20px);
    margin-bottom: 16px;
}

.batter-grid {
    display: grid;
    grid-template-columns: 1.4fr 1fr 1fr;
    gap: 14px;
    margin-bottom: 16px;
}

.batter-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 22px;
    padding: 18px;
    min-height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.now-card {
    border: 2px solid rgba(132,204,22,0.85);
    box-shadow: 0 0 22px rgba(132,204,22,0.18);
}

.deck-card {
    border: 2px solid rgba(59,130,246,0.75);
    box-shadow: 0 0 22px rgba(59,130,246,0.14);
}

.hole-card {
    border: 2px solid rgba(168,85,247,0.75);
    box-shadow: 0 0 22px rgba(168,85,247,0.14);
}

.card-label {
    color: #cbd5e1;
    text-transform: uppercase;
    font-size: 15px;
    letter-spacing: 2px;
    font-weight: 900;
    margin-bottom: 12px;
}

.now-name {
    color: white;
    font-size: clamp(36px, 5.2vw, 64px);
    font-weight: 900;
    line-height: 1.02;
}

.secondary-name {
    color: white;
    font-size: clamp(26px, 3.6vw, 42px);
    font-weight: 900;
    line-height: 1.05;
}

.score-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1.25fr;
    gap: 14px;
    margin-bottom: 12px;
}

.score-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 20px;
    padding: 18px;
}

.score-name {
    color: #cbd5e1;
    font-size: 17px;
    font-weight: 800;
}

.score-number {
    color: white;
    font-size: clamp(42px, 5vw, 58px);
    font-weight: 900;
    line-height: 1;
    margin-top: 8px;
}

.game-info {
    color: white;
    font-size: clamp(30px, 4vw, 44px);
    font-weight: 900;
    line-height: 1.15;
}

.button-row {
    margin-bottom: 12px;
}

.stButton > button {
    border-radius: 12px;
    height: 46px;
    font-weight: 900;
    font-size: 15px;
}

.lineup-title {
    color: white;
    font-size: 26px;
    font-weight: 900;
    margin-top: 10px;
    margin-bottom: 8px;
}

.lineup-subtitle {
    color: white;
    font-size: 21px;
    font-weight: 900;
    margin-bottom: 8px;
}

.lineup-text {
    color: #e5e7eb;
    font-size: 18px;
    line-height: 1.55;
}

.highlight {
    background: rgba(34,197,94,0.25);
    border-radius: 12px;
    padding: 7px 10px;
    color: white;
    font-weight: 900;
    font-size: 18px;
    margin: 3px 0;
}

@media screen and (max-width: 850px) {
    .batter-grid {
        grid-template-columns: 1fr;
    }

    .score-grid {
        grid-template-columns: 1fr;
    }

    .batter-card {
        min-height: 110px;
    }
}
</style>
""", unsafe_allow_html=True)

current_batter, on_deck, in_the_hole = get_batters(data)

st.markdown("<div class='main-title'>🥎 Softball Dugout Live</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{data['team_name']} dugout control board</div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class='batter-grid'>
        <div class='batter-card now-card'>
            <div class='card-label'>Now Batting</div>
            <div class='now-name'>{current_batter}</div>
        </div>

        <div class='batter-card deck-card'>
            <div class='card-label'>On Deck</div>
            <div class='secondary-name'>{on_deck}</div>
        </div>

        <div class='batter-card hole-card'>
            <div class='card-label'>In The Hole</div>
            <div class='secondary-name'>{in_the_hole}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class='score-grid'>
        <div class='score-card'>
            <div class='score-name'>{data['team_name']}</div>
            <div class='score-number'>{data['home_score']}</div>
        </div>

        <div class='score-card'>
            <div class='score-name'>{data['opponent']}</div>
            <div class='score-number'>{data['away_score']}</div>
        </div>

        <div class='score-card'>
            <div class='card-label'>Game Info</div>
            <div class='game-info'>{data['half']} {data['inning']}</div>
            <div class='game-info'>Outs: {data['outs']}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

button_col1, button_col2, button_col3, button_col4, button_col5 = st.columns(5)

with button_col1:
    if st.button("+ Run Us", use_container_width=True):
        data["home_score"] += 1
        save_data(data)
        rerun_app()

with button_col2:
    if st.button("+ Run Opp", use_container_width=True):
        data["away_score"] += 1
        save_data(data)
        rerun_app()

with button_col3:
    if st.button("Previous Batter", use_container_width=True):
        previous_batter(data)
        save_data(data)
        rerun_app()

with button_col4:
    if st.button("Next Batter", use_container_width=True):
        next_batter(data)
        save_data(data)
        rerun_app()

with button_col5:
    if st.button("+ Out", use_container_width=True):
        add_out(data)
        save_data(data)
        rerun_app()

reset_col1, reset_col2, reset_col3 = st.columns([1, 1, 1])

with reset_col2:
    if st.button("Reset Game", use_container_width=True):
        save_data(default_data)
        rerun_app()

st.markdown("<div class='lineup-title'>Lineup</div>", unsafe_allow_html=True)

lineup_col1, lineup_col2 = st.columns(2)

with lineup_col1:
    st.markdown("<div class='lineup-subtitle'>Female Lineup</div>", unsafe_allow_html=True)
    for i, player in enumerate(data["female_lineup"]):
        if i == data["current_female_index"] and data["next_gender"] == "Female":
            st.markdown(f"<div class='highlight'>🥎 {i + 1}. {player}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='lineup-text'>{i + 1}. {player}</div>", unsafe_allow_html=True)

with lineup_col2:
    st.markdown("<div class='lineup-subtitle'>Male Lineup</div>", unsafe_allow_html=True)
    for i, player in enumerate(data["male_lineup"]):
        if i == data["current_male_index"] and data["next_gender"] == "Male":
            st.markdown(f"<div class='highlight'>🥎 {i + 1}. {player}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='lineup-text'>{i + 1}. {player}</div>", unsafe_allow_html=True)
