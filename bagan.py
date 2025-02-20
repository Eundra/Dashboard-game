import streamlit as st
import pandas as pd

# Fungsi untuk menghasilkan jadwal pertandingan dengan sesi yang tidak bentrok
def generate_fixtures(teams, home_away=True):
    sessions = []
    base_fixtures = [
        [(teams[0], teams[3]), (teams[2], teams[1])],  # Pertandingan 1
        [(teams[0], teams[1]), (teams[2], teams[3])],  # Pertandingan 2
        [(teams[0], teams[2]), (teams[1], teams[3])]   # Pertandingan 3
    ]
    
    for fixtures in base_fixtures:
        sessions.append(fixtures)

    if home_away:  # Jika Home & Away, tambahkan putaran kedua
        for fixtures in base_fixtures:
            reversed_fixtures = [(away, home) for home, away in fixtures]
            sessions.append(reversed_fixtures)
    
    return sessions

# Fungsi untuk memperbarui klasemen berdasarkan hasil pertandingan
def update_standings(standings, team, goals_for, goals_against):
    if team not in standings:
        standings[team] = {'MP': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'Pts': 0}

    standings[team]['MP'] += 1
    standings[team]['GF'] += goals_for
    standings[team]['GA'] += goals_against

    if goals_for > goals_against:
        standings[team]['W'] += 1
        standings[team]['Pts'] += 3
    elif goals_for < goals_against:
        standings[team]['L'] += 1
    else:
        standings[team]['D'] += 1
        standings[team]['Pts'] += 1

st.set_page_config(page_title="Turnamen Sepak Bola", layout="wide")
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Input & Jadwal", "Klasemen", "Riwayat", "Babak Championship"])

# Inisialisasi session state
if "teams" not in st.session_state:
    st.session_state.teams = []
if "fixtures" not in st.session_state:
    st.session_state.fixtures = []
if "standings" not in st.session_state:
    st.session_state.standings = {}
if "confirmed_matches" not in st.session_state:
    st.session_state.confirmed_matches = set()
if "match_history" not in st.session_state:
    st.session_state.match_history = []

if page == "Input & Jadwal":
    st.title("⚽ Input Tim & Jadwal")
    team_input = st.text_area("Masukkan 4 tim (pisahkan dengan koma)", "")

    if st.button("Buat Jadwal Grup"):
        teams = [t.strip() for t in team_input.split(",") if t.strip()]
        if len(teams) != 4:
            st.error("Harus memasukkan tepat 4 tim!")
        else:
            home_away = st.radio("Pilih sistem pertandingan:", ("Home & Away", "Sekali Bertemu"))
            st.session_state.teams = teams
            st.session_state.fixtures = generate_fixtures(teams, home_away == "Home & Away")
            st.session_state.standings = {team: {'MP': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'Pts': 0} for team in teams}
            st.session_state.confirmed_matches = set()
            st.session_state.match_history = []
            st.success("Jadwal berhasil dibuat!")

    st.title("📅 Jadwal Pertandingan")
    if not st.session_state.fixtures:
        st.warning("Belum ada jadwal pertandingan.")
    else:
        for i, session in enumerate(st.session_state.fixtures):
            st.subheader(f"🕑 Sesi {i+1}")
            for match in session:
                match_key = f"{match[0]}_{match[1]}"
                if match_key not in st.session_state.confirmed_matches:
                    col1, col2 = st.columns(2)
                    with col1:
                        score1 = st.number_input(f"Skor {match[0]}", min_value=0, step=1, key=f"score_{match_key}_1")
                    with col2:
                        score2 = st.number_input(f"Skor {match[1]}", min_value=0, step=1, key=f"score_{match_key}_2")

                    if st.button(f"Konfirmasi {match[0]} vs {match[1]}"):
                        update_standings(st.session_state.standings, match[0], score1, score2)
                        update_standings(st.session_state.standings, match[1], score2, score1)
                        st.session_state.confirmed_matches.add(match_key)
                        st.session_state.match_history.append(f"{match[0]} {score1} - {score2} {match[1]}")
                        st.rerun()

if page == "Klasemen":
    st.title("📊 Klasemen")
    if not st.session_state.standings:
        st.warning("Belum ada data klasemen.")
    else:
        standings_df = pd.DataFrame.from_dict(st.session_state.standings, orient='index')
        standings_df = standings_df.sort_values(by=['Pts', 'GF', 'GA'], ascending=[False, False, True])
        st.dataframe(standings_df)

if page == "Riwayat":
    st.title("📜 Riwayat Pertandingan")
    if not st.session_state.match_history:
        st.warning("Belum ada pertandingan yang dikonfirmasi.")
    else:
        for history in st.session_state.match_history:
            st.write(history)
