import streamlit as st
import json
import os

DATA_FILE = "game_data.json"

default_data = {
    "team_name": "Your Team",
    "opponent": "Opponent",
    "home_score": 0,
    "away_score": 0,
    "inning": 1,
    "half": "Top",
    "outs": 0,
    "female_lineup": [
        "Player One",
        "Player Two",
        "Player Three",
        "Player Four",
        "Player Five"
    ],
    "male_lineup": [
        "Player Six",
        "Player Seven",
        "Player Eight",
        "Player Nine",
        "Player Ten"
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

def first_name(name):
    return name.split()[0]

def get_batters(data):
    f = data["current_female_index"]
    m = data["current_male_index"]

    if data["next_gender"] == "Female":
        return (
            data["female_lineup"][f],
            data["male_lineup"][m],
            data["female_lineup"][(f + 1) % len(data["female_lineup"])]
        )
    else:
        return (
            data["male_lineup"][m],
            data["female_lineup"][f],
            data["male_lineup"][(m + 1) % len(data["male_lineup"])]
        )

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
    page_title="Dugout Live",
    page_icon="🥎",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #003B73 0%, #005A9C 45%, #001F3F 100%);
}

header {
    height: 0px;
}

.block-container {
    padding-top: 2.6rem;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-bottom: 1rem;
    max-width: 1350px;
}

.main-title {
    font-size: clamp(34px, 4.1vw, 56px);
    font-weight: 900;
    color: white;
    line-height: 1.08;
    margin-bottom: 4px;
}

.subtitle {
    color: #EAF4FF;
    font-size: 18px;
    margin-bottom: 14px;
}

.batter-grid {
    display: grid;
    grid-template-columns: 1.4fr 1fr 1fr;
    gap: 14px;
    margin-bottom: 8px;
}

.batter-card {
    background: rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 18px;
    min-height: 150px;
}

.now-card {
    border: 2px solid #FFFFFF;
    box-shadow: 0 0 22px rgba(255,255,255,0.22);
}

.deck-card {
    border: 2px solid #EF3E42;
    box-shadow: 0 0 20px rgba(239,62,66,0.22);
}

.hole-card {
    border: 2px solid #A7C7E7;
    box-shadow: 0 0 20px rgba(167,199,231,0.22);
}

.card-label {
    color: #EAF4FF;
    text-transform: uppercase;
    font-size: 13px;
    letter-spacing: 2px;
    font-weight: 900;
    margin-bottom: 12px;
}

.now-name {
    color: white;
    font-size: clamp(48px, 6vw, 78px);
    font-weight: 900;
    line-height: 1.03;
}

.secondary-name {
    color: white;
    font-size: clamp(34px, 4vw, 54px);
    font-weight: 900;
    line-height: 1.05;
}

.next-batter-wrap button {
    height: 64px !important;
    font-size: 23px !important;
    font-weight: 900 !important;
    border-radius: 16px !important;
    background: #EF3E42 !important;
    border: 1px solid #EF3E42 !important;
    color: white !important;
}

.previous-wrap button {
    height: 40px !important;
    font-size: 13px !important;
    border-radius: 999px !important;
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.35) !important;
    color: #EAF4FF !important;
}

.score-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1.25fr;
    gap: 14px;
    margin-top: 14px;
    margin-bottom: 8px;
}

.score-card {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 18px;
    padding: 16px;
    min-height: 115px;
}

.score-name {
    color: #EAF4FF;
    font-size: 16px;
    font-weight: 800;
}

.score-number {
    color: white;
    font-size: 50px;
    font-weight: 900;
    line-height: 1;
    margin-top: 8px;
}

.game-info {
    color: white;
    font-size: 34px;
    font-weight: 900;
    line-height: 1.15;
}

.stButton > button {
    border-radius: 12px;
    height: 42px;
    font-weight: 900;
    font-size: 14px;
}

div[data-testid="stCheckbox"] label {
    color: #FFD6D6 !important;
    font-weight: 900;
}

.lineup-title {
    color: white;
    font-size: 24px;
    font-weight: 900;
    margin-top: 12px;
}

.lineup-subtitle {
    color: white;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 8px;
}

.lineup-text {
    color: #EAF4FF;
    font-size: 16px;
    line-height: 1.45;
}

.highlight {
    background: rgba(239,62,66,0.28);
    border-radius: 12px;
    padding: 6px 10px;
    color: white;
    font-weight: 900;
    font-size: 16px;
    margin: 3px 0;
}

.reset-note {
    color: #FFD6D6;
    font-size: 13px;
    font-weight: 800;
    text-align: right;
}

@media screen and (max-width: 900px) {
    .block-container {
        padding-top: 2.4rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

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

current_batter_display = first_name(current_batter)
on_deck_display = first_name(on_deck)
in_the_hole_display = first_name(in_the_hole)

st.markdown("<div class='main-title'>🥎 Dugout Live</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{data['team_name']} game board</div>", unsafe_allow_html=True)

batting_html = f"""
<div class='batter-grid'>
<div class='batter-card now-card'>
<div class='card-label'>Now Batting</div>
<div class='now-name'>{current_batter_display}</div>
</div>
<div class='batter-card deck-card'>
<div class='card-label'>On Deck</div>
<div class='secondary-name'>{on_deck_display}</div>
</div>
<div class='batter-card hole-card'>
<div class='card-label'>In The Hole</div>
<div class='secondary-name'>{in_the_hole_display}</div>
</div>
</div>
"""
st.markdown(batting_html, unsafe_allow_html=True)

bat_next_col, bat_empty_col, bat_prev_col = st.columns([2.2, 1, 0.8])

with bat_next_col:
    st.markdown("<div class='next-batter-wrap'>", unsafe_allow_html=True)
    if st.button("NEXT BATTER", use_container_width=True):
        next_batter(data)
        save_data(data)
        rerun_app()
    st.markdown("</div>", unsafe_allow_html=True)

with bat_empty_col:
    st.empty()

with bat_prev_col:
    st.markdown("<div class='previous-wrap'>", unsafe_allow_html=True)
    if st.button("Previous Batter", use_container_width=True):
        previous_batter(data)
        save_data(data)
        rerun_app()
    st.markdown("</div>", unsafe_allow_html=True)

score_html = f"""
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
"""
st.markdown(score_html, unsafe_allow_html=True)

score_button_col1, score_button_col2, score_button_col3 = st.columns([1, 1, 1.25])

with score_button_col1:
    if st.button("+ Run Us", use_container_width=True):
        data["home_score"] += 1
        save_data(data)
        rerun_app()

with score_button_col2:
    if st.button("+ Run Opp", use_container_width=True):
        data["away_score"] += 1
        save_data(data)
        rerun_app()

with score_button_col3:
    if st.button("+ Out", use_container_width=True):
        add_out(data)
        save_data(data)
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

st.markdown("<br>", unsafe_allow_html=True)

reset_left, reset_right = st.columns([4, 1])

with reset_right:
    st.markdown("<div class='reset-note'>Reset area</div>", unsafe_allow_html=True)
    confirm_reset = st.checkbox("Confirm")
    if st.button("Reset Game", use_container_width=True):
        if confirm_reset:
            save_data(default_data)
            rerun_app()
        else:
            st.warning("Check Confirm first.")
