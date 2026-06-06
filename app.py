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
    "female_lineup": ["Player One", "Player Two", "Player Three", "Player Four", "Player Five"],
    "male_lineup": ["Player Six", "Player Seven", "Player Eight", "Player Nine", "Player Ten"],
    "current_female_index": 0,
    "current_male_index": 0,
    "next_gender": "Female",
    "theme": "Dodger"
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            saved = json.load(file)
        for key, value in default_data.items():
            if key not in saved:
                saved[key] = value
        return saved
    return default_data.copy()

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def rerun_app():
    st.rerun()

def first_name(name):
    return name.split()[0] if name.split() else name

def clean_lineup(text):
    return [line.strip() for line in text.splitlines() if line.strip()]

def lineup_to_text(lineup):
    return "\n".join(lineup)

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

def undo_out(data):
    if data["outs"] > 0:
        data["outs"] -= 1

data = load_data()

st.set_page_config(
    page_title="Dugout Live",
    page_icon="🥎",
    layout="wide"
)

themes = {
    "Dodger": {
        "bg": "linear-gradient(135deg, #003B73 0%, #005A9C 45%, #001F3F 100%)",
        "now": "#FFFFFF",
        "deck": "#EF3E42",
        "hole": "#A7C7E7",
        "card": "rgba(255,255,255,0.13)"
    },
    "Night Game": {
        "bg": "linear-gradient(135deg, #08111f 0%, #111827 50%, #020617 100%)",
        "now": "#84cc16",
        "deck": "#38bdf8",
        "hole": "#c084fc",
        "card": "rgba(255,255,255,0.09)"
    }
}

theme = themes.get(data.get("theme", "Dodger"), themes["Dodger"])

st.markdown(f"""
<style>
.stApp {{
    background: {theme["bg"]};
}}

header {{
    height: 0px;
}}

.block-container {{
    padding-top: 1.2rem;
    padding-left: 2.3rem;
    padding-right: 2.3rem;
    padding-bottom: 1rem;
    max-width: 1450px;
}}

.main-title {{
    font-size: clamp(38px, 4.4vw, 64px);
    font-weight: 900;
    color: white;
    line-height: 1;
    margin-bottom: 6px;
}}

.subtitle {{
    color: #EAF4FF;
    font-size: 18px;
    margin-bottom: 18px;
}}

.batter-grid {{
    display: grid;
    grid-template-columns: 1.45fr 1fr 1fr;
    gap: 16px;
    margin-bottom: 8px;
}}

.batter-card {{
    background: {theme["card"]};
    border-radius: 22px;
    padding: 22px;
    min-height: 185px;
}}

.now-card {{
    border: 3px solid {theme["now"]};
}}

.deck-card {{
    border: 3px solid {theme["deck"]};
}}

.hole-card {{
    border: 3px solid {theme["hole"]};
}}

.card-label {{
    color: #EAF4FF;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 3px;
    font-weight: 900;
    margin-bottom: 16px;
}}

.now-name {{
    color: white;
    font-size: clamp(64px, 7vw, 104px);
    font-weight: 900;
    line-height: 0.95;
}}

.secondary-name {{
    color: white;
    font-size: clamp(46px, 5vw, 74px);
    font-weight: 900;
    line-height: 0.98;
}}

.score-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr 1.15fr;
    gap: 16px;
    margin-top: 18px;
    margin-bottom: 8px;
}}

.score-card {{
    background: {theme["card"]};
    border: 2px solid rgba(255,255,255,0.30);
    border-radius: 20px;
    padding: 18px;
    min-height: 120px;
}}

.score-name {{
    color: #EAF4FF;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 14px;
    font-weight: 900;
}}

.score-number {{
    color: white;
    font-size: 58px;
    font-weight: 900;
    line-height: 1;
    margin-top: 8px;
}}

.game-info {{
    color: white;
    font-size: 44px;
    font-weight: 900;
    line-height: 1.08;
}}

.stButton > button {{
    border-radius: 12px;
    height: 44px;
    font-weight: 900;
    font-size: 14px;
}}

div[data-testid="stButton"] button[kind="primary"] {{
    height: 66px !important;
    font-size: 24px !important;
    border-radius: 16px !important;
    font-weight: 900 !important;
}}

.lineup-title {{
    color: white;
    font-size: 24px;
    font-weight: 900;
    margin-top: 14px;
}}

.lineup-subtitle {{
    color: white;
    font-size: 18px;
    font-weight: 900;
    margin-bottom: 6px;
}}

.lineup-text {{
    color: #EAF4FF;
    font-size: 16px;
    line-height: 1.4;
}}

.highlight {{
    background: rgba(239,62,66,0.32);
    border-radius: 12px;
    padding: 6px 10px;
    color: white;
    font-weight: 900;
    font-size: 16px;
    margin: 3px 0;
}}

.setup-note {{
    color: #EAF4FF;
    font-size: 14px;
}}

.reset-note {{
    color: #FFD6D6;
    font-size: 13px;
    font-weight: 800;
    text-align: right;
}}

div[data-testid="stCheckbox"] label {{
    color: #FFD6D6 !important;
    font-weight: 900;
}}

@media screen and (max-width: 900px) {{
    .block-container {{
        padding-left: 1rem;
        padding-right: 1rem;
    }}

    .batter-grid {{
        grid-template-columns: 1fr;
    }}

    .score-grid {{
        grid-template-columns: 1fr;
    }}

    .batter-card {{
        min-height: 120px;
    }}
}}
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

bat_next_col, bat_middle_col, bat_prev_col = st.columns([1.45, 1, 1])

with bat_next_col:
    if st.button("NEXT BATTER", type="primary", use_container_width=True):
        next_batter(data)
        save_data(data)
        rerun_app()

with bat_middle_col:
    st.empty()

with bat_prev_col:
    if st.button("Previous Batter", use_container_width=True):
        previous_batter(data)
        save_data(data)
        rerun_app()

score_html = f"""
<div class='score-grid'>
<div class='score-card'>
<div class='score-name'>{data['team_name']} Score</div>
<div class='score-number'>{data['home_score']}</div>
</div>
<div class='score-card'>
<div class='score-name'>{data['opponent']} Score</div>
<div class='score-number'>{data['away_score']}</div>
</div>
<div class='score-card'>
<div class='score-name'>Outs / Inning</div>
<div class='game-info'>{data['outs']} Outs • {data['half']} {data['inning']}</div>
</div>
</div>
"""
st.markdown(score_html, unsafe_allow_html=True)

score_col1, score_col2, score_col3 = st.columns([1, 1, 1.15])

with score_col1:
    if st.button("+ Run Us", use_container_width=True):
        data["home_score"] += 1
        save_data(data)
        rerun_app()

with score_col2:
    if st.button("+ Run Opp", use_container_width=True):
        data["away_score"] += 1
        save_data(data)
        rerun_app()

with score_col3:
    out_col1, out_col2 = st.columns(2)
    with out_col1:
        if st.button("Out", use_container_width=True):
            add_out(data)
            save_data(data)
            rerun_app()
    with out_col2:
        if st.button("Undo Out", use_container_width=True):
            undo_out(data)
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

st.markdown("---")

with st.expander("⚙️ Game Setup / Edit Players"):
    st.markdown("<div class='setup-note'>Use Quick Paste if you already have a lineup. Use Guided Entry if you want to type one player at a time.</div>", unsafe_allow_html=True)

    setup_tab1, setup_tab2 = st.tabs(["Quick Paste", "Guided Entry"])

    with setup_tab1:
        quick_col1, quick_col2 = st.columns(2)

        with quick_col1:
            new_team_name = st.text_input("Team Name", value=data["team_name"], key="quick_team")
            new_female_text = st.text_area(
                "Female Lineup — one player per line",
                value=lineup_to_text(data["female_lineup"]),
                height=170,
                key="quick_female"
            )

        with quick_col2:
            new_opponent = st.text_input("Opponent", value=data["opponent"], key="quick_opp")
            new_male_text = st.text_area(
                "Male Lineup — one player per line",
                value=lineup_to_text(data["male_lineup"]),
                height=170,
                key="quick_male"
            )

        theme_choice = st.selectbox(
            "Theme",
            list(themes.keys()),
            index=list(themes.keys()).index(data.get("theme", "Dodger")),
            key="quick_theme"
        )

        if st.button("Save Quick Setup", use_container_width=True):
            new_female_lineup = clean_lineup(new_female_text)
            new_male_lineup = clean_lineup(new_male_text)

            if not new_female_lineup or not new_male_lineup:
                st.warning("Please add at least one female player and one male player.")
            else:
                data["team_name"] = new_team_name.strip() or "Your Team"
                data["opponent"] = new_opponent.strip() or "Opponent"
                data["female_lineup"] = new_female_lineup
                data["male_lineup"] = new_male_lineup
                data["theme"] = theme_choice
                data["home_score"] = 0
                data["away_score"] = 0
                data["inning"] = 1
                data["half"] = "Top"
                data["outs"] = 0
                data["current_female_index"] = 0
                data["current_male_index"] = 0
                data["next_gender"] = "Female"
                save_data(data)
                rerun_app()

    with setup_tab2:
        guide_col1, guide_col2 = st.columns(2)

        with guide_col1:
            guided_team_name = st.text_input("Team Name", value=data["team_name"], key="guided_team")
            female_count = st.number_input("Number of female players", min_value=1, max_value=20, value=len(data["female_lineup"]), step=1)

            guided_female = []
            for i in range(female_count):
                existing = data["female_lineup"][i] if i < len(data["female_lineup"]) else ""
                guided_female.append(st.text_input(f"Female Player {i + 1}", value=existing, key=f"female_{i}"))

        with guide_col2:
            guided_opponent = st.text_input("Opponent", value=data["opponent"], key="guided_opp")
            male_count = st.number_input("Number of male players", min_value=1, max_value=20, value=len(data["male_lineup"]), step=1)

            guided_male = []
            for i in range(male_count):
                existing = data["male_lineup"][i] if i < len(data["male_lineup"]) else ""
                guided_male.append(st.text_input(f"Male Player {i + 1}", value=existing, key=f"male_{i}"))

        guided_theme = st.selectbox(
            "Theme",
            list(themes.keys()),
            index=list(themes.keys()).index(data.get("theme", "Dodger")),
            key="guided_theme"
        )

        if st.button("Save Guided Setup", use_container_width=True):
            guided_female_clean = [p.strip() for p in guided_female if p.strip()]
            guided_male_clean = [p.strip() for p in guided_male if p.strip()]

            if not guided_female_clean or not guided_male_clean:
                st.warning("Please add at least one female player and one male player.")
            else:
                data["team_name"] = guided_team_name.strip() or "Your Team"
                data["opponent"] = guided_opponent.strip() or "Opponent"
                data["female_lineup"] = guided_female_clean
                data["male_lineup"] = guided_male_clean
                data["theme"] = guided_theme
                data["home_score"] = 0
                data["away_score"] = 0
                data["inning"] = 1
                data["half"] = "Top"
                data["outs"] = 0
                data["current_female_index"] = 0
                data["current_male_index"] = 0
                data["next_gender"] = "Female"
                save_data(data)
                rerun_app()

reset_left, reset_right = st.columns([4, 1])

with reset_right:
    st.markdown("<div class='reset-note'>Reset area</div>", unsafe_allow_html=True)
    confirm_reset = st.checkbox("Confirm Reset")
    if st.button("RESET GAME", use_container_width=True):
        if confirm_reset:
            save_data(default_data.copy())
            rerun_app()
        else:
            st.warning("Check Confirm Reset first.")
