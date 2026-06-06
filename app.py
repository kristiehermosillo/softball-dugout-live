import streamlit as st
import json
import os

DATA_FILE = "game_data.json"

# Default generic data
default_data = {
    "team_name": "Your Team",
    "opponent": "Opponent",
    "home_score": 0,
    "away_score": 0,
    "inning": 1,
    "half": "Top",
    "outs": 0,
    "female_lineup": ["Player One","Player Two","Player Three","Player Four","Player Five"],
    "male_lineup": ["Player Six","Player Seven","Player Eight","Player Nine","Player Ten"],
    "current_female_index": 0,
    "current_male_index": 0,
    "next_gender": "Female",
    "theme": "Dodger"
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    return default_data

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)

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
        return data["female_lineup"][f], data["male_lineup"][m], data["female_lineup"][(f+1)%len(data["female_lineup"])]
    else:
        return data["male_lineup"][m], data["female_lineup"][f], data["male_lineup"][(m+1)%len(data["male_lineup"])]

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
        if data["half"]=="Top": data["half"]="Bottom"
        else: data["half"]="Top"; data["inning"]+=1

# Load saved data
data = load_data()

st.set_page_config(page_title="Dugout Live", page_icon="🥎", layout="wide")

# Theme colors
theme_colors = {
    "Dodger": {
        "bg":"linear-gradient(135deg,#003B73 0%,#005A9C 45%,#001F3F 100%)",
        "primary":"#1E90FF",
        "secondary":"#EF3E42",
        "accent":"#A7C7E7"
    },
    "Classic": {
        "bg":"linear-gradient(135deg,#111827 0%,#181C28 50%,#020617 100%)",
        "primary":"#84cc16",
        "secondary":"#38bdf8",
        "accent":"#c084fc"
    }
}

colors = theme_colors.get(data.get("theme","Dodger"))

# CSS
st.markdown(f"""
<style>
.stApp {{ background: {colors['bg']}; }}
.block-container {{ padding-top:2.6rem; padding-left:2rem; padding-right:2rem; padding-bottom:1rem; max-width:1350px; }}
.main-title {{ font-size: clamp(34px,4.1vw,56px); font-weight:900; color:white; margin-bottom:4px; }}
.subtitle {{ color:#EAF4FF; font-size:18px; margin-bottom:14px; }}
.batter-grid {{ display:grid; grid-template-columns:1.4fr 1fr 1fr; gap:14px; margin-bottom:8px; }}
.batter-card {{ background: rgba(255,255,255,0.12); border-radius:20px; padding:18px; min-height:150px; }}
.now-card {{ border:2px solid {colors['primary']}; box-shadow:0 0 22px rgba(255,255,255,0.22); }}
.deck-card {{ border:2px solid {colors['secondary']}; box-shadow:0 0 20px rgba(239,62,66,0.22); }}
.hole-card {{ border:2px solid {colors['accent']}; box-shadow:0 0 20px rgba(167,199,231,0.22); }}
.card-label {{ color:#EAF4FF; text-transform:uppercase; font-size:13px; letter-spacing:2px; font-weight:900; margin-bottom:12px; }}
.now-name {{ color:white; font-size:clamp(48px,6vw,78px); font-weight:900; line-height:1.03; }}
.secondary-name {{ color:white; font-size:clamp(34px,4vw,54px); font-weight:900; line-height:1.05; }}
.next-batter-wrap button {{ height:64px!important; font-size:23px!important; font-weight:900!important; border-radius:16px!important; background:{colors['primary']}!important; border:1px solid {colors['primary']}!important; color:white!important; }}
.previous-wrap button {{ height:40px!important; font-size:13px!important; border-radius:999px!important; background:rgba(255,255,255,0.08)!important; border:1px solid rgba(255,255,255,0.35)!important; color:#EAF4FF!important; }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-title'>🥎 Dugout Live</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{data['team_name']} game board</div>", unsafe_allow_html=True)

# Manual setup
with st.expander("Game Setup / Enter Players"):
    theme_choice = st.selectbox("Theme", list(theme_colors.keys()), index=list(theme_colors.keys()).index(data.get("theme","Dodger")))
    new_team = st.text_input("Team Name", value=data["team_name"])
    new_opp = st.text_input("Opponent", value=data["opponent"])
    new_female = st.text_area("Female Lineup (one per line)", value=lineup_to_text(data["female_lineup"]))
    new_male = st.text_area("Male Lineup (one per line)", value=lineup_to_text(data["male_lineup"]))
    if st.button("Save Setup", use_container_width=True):
        f_lineup = clean_lineup(new_female)
        m_lineup = clean_lineup(new_male)
        if f_lineup and m_lineup:
            data["team_name"]=new_team.strip() or "Your Team"
            data["opponent"]=new_opp.strip() or "Opponent"
            data["female_lineup"]=f_lineup
            data["male_lineup"]=m_lineup
            data["current_female_index"]=0
            data["current_male_index"]=0
            data["next_gender"]="Female"
            data["home_score"]=0
            data["away_score"]=0
            data["inning"]=1
            data["half"]="Top"
            data["outs"]=0
            data["theme"]=theme_choice
            save_data(data)
            st.success("Setup saved.")
            rerun_app()
        else:
            st.warning("Enter at least one player in each lineup.")

# Batting cards
current_batter, on_deck, in_the_hole = get_batters(data)
current_batter_display = first_name(current_batter)
on_deck_display = first_name(on_deck)
in_the_hole_display = first_name(in_the_hole)

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

# Batting buttons
bat_next_col, bat_empty_col, bat_prev_col = st.columns([2.2,1,0.8])
with bat_next_col:
    if st.button("NEXT BATTER", use_container_width=True):
        next_batter(data)
        save_data(data)
        rerun_app()
with bat_empty_col: st.empty()
with bat_prev_col:
    if st.button("Previous Batter", use_container_width=True):
        previous_batter(data)
        save_data(data)
        rerun_app()

# Score
score_html = f"""
<div class='batter-grid'>
<div class='batter-card now-card'>
<div class='card-label'>{data['team_name']} Score</div>
<div class='now-name'>{data['home_score']}</div>
</div>
<div class='batter-card deck-card'>
<div class='card-label'>{data['opponent']} Score</div>
<div class='now-name'>{data['away_score']}</div>
</div>
<div class='batter-card hole-card'>
<div class='card-label'>Outs / Inning</div>
<div class='secondary-name'>{data['outs']} Outs • {data['half']} {data['inning']}</div>
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

    out_col1, out_col2 = st.columns(2)

    with out_col1:
        if st.button("Out", use_container_width=True):
            add_out(data)
            save_data(data)
            rerun_app()

    with out_col2:
        if st.button("Undo Out", use_container_width=True):

            if data["outs"] > 0:
                data["outs"] -= 1

            save_data(data)
            rerun_app()

# Lineup display
st.markdown("<div class='lineup-title'>Lineup</div>", unsafe_allow_html=True)
lineup_col1, lineup_col2 = st.columns(2)
with lineup_col1:
    st.markdown("<div class='lineup-subtitle'>Female Lineup</div>", unsafe_allow_html=True)
    for i,p in enumerate(data["female_lineup"]):
        if i==data["current_female_index"] and data["next_gender"]=="Female":
            st.markdown(f"<div class='highlight'>🥎 {i+1}. {p}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='lineup-text'>{i+1}. {p}</div>", unsafe_allow_html=True)
with lineup_col2:
    st.markdown("<div class='lineup-subtitle'>Male Lineup</div>", unsafe_allow_html=True)
    for i,p in enumerate(data["male_lineup"]):
        if i==data["current_male_index"] and data["next_gender"]=="Male":
            st.markdown(f"<div class='highlight'>🥎 {i+1}. {p}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='lineup-text'>{i+1}. {p}</div>", unsafe_allow_html=True)

# Reset button bottom-right
reset_left, reset_right = st.columns([4,1])
with reset_right:
    confirm_reset = st.checkbox("Confirm Reset")
    if st.button("RESET GAME", use_container_width=True):
        if confirm_reset:
            save_data(default_data)
            rerun_app()
        else:
            st.warning("Check Confirm Reset first.")
