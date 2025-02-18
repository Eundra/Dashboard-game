
import streamlit as st
import random
import pandas as pd

# Fungsi untuk menghasilkan jadwal pertandingan dengan home & away atau sekali bertemu
def generate_fixtures(teams, home_away=True):
    fixtures = [(team1, team2) for i, team1 in enumerate(teams) for team2 in teams[i+1:]]
    if home_away:
        fixtures += [(team2, team1) for team1, team2 in fixtures]
    random.shuffle(fixtures)
    return fixtures

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

if "teams" not in st.session_state:
    st.session_state.teams = []
if "fixtures" not in st.session_state:
    st.session_state.fixtures = []
if "standings" not in st.session_state:
    st.session_state.standings = {}
if "final_teams" not in st.session_state:
    st.session_state.final_teams = []
if "champion" not in st.session_state:
    st.session_state.champion = None
if "confirmed_matches" not in st.session_state:
    st.session_state.confirmed_matches = set()
if "match_history" not in st.session_state:
    st.session_state.match_history = []

if page == "Input & Jadwal":
    st.title("⚽ Input Tim & Jadwal")
    team_input = st.text_area("Masukkan nama tim (pisahkan dengan koma)", "")
    if st.button("Buat Jadwal Grup"):
        teams = [t.strip() for t in team_input.split(",") if t.strip()]
        if len(teams) < 4:
            st.error("Minimal 4 tim diperlukan!")
        else:
            st.session_state.teams = teams
            home_away = st.radio("Pilih sistem pertandingan:", ("Home & Away", "Sekali Bertemu"))
            st.session_state.fixtures = generate_fixtures(teams, home_away == "Home & Away")
            st.session_state.standings = {team: {'MP': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'Pts': 0} for team in teams}
            st.session_state.final_teams = []
            st.session_state.champion = None
            st.session_state.confirmed_matches = set()
            st.session_state.match_history = []
            st.success("Jadwal berhasil dibuat!")

    st.title("📅 Jadwal Pertandingan")
    if not st.session_state.fixtures:
        st.warning("Belum ada jadwal pertandingan. Silakan masukkan tim terlebih dahulu.")
    else:
        for match in st.session_state.fixtures:
            match_key = f"{match[0]}_{match[1]}"
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
                st.session_state.fixtures.remove(match)
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

if page == "Babak Championship":
    st.subheader("Riwayat Pertandingan")
    if st.session_state.match_history:
        for history in st.session_state.match_history:
            st.write(history)
    else:
        st.write("Belum ada pertandingan yang dikonfirmasi.")

    if st.session_state.standings and not st.session_state.final_teams and not st.session_state.fixtures:
        if len(st.session_state.standings) >= 4:
            standings_df = pd.DataFrame.from_dict(st.session_state.standings, orient='index')
            standings_df = standings_df.sort_values(by=['Pts', 'GF', 'GA'], ascending=[False, False, True])
            st.session_state.final_teams = standings_df.index[:4].tolist()

    if len(st.session_state.final_teams) == 4:
        st.subheader("Pertandingan Champions")
        semi_final_1 = (st.session_state.final_teams[0], st.session_state.final_teams[3])
        semi_final_2 = (st.session_state.final_teams[1], st.session_state.final_teams[2])

        st.write(f"🔹 Semi Final 1: {semi_final_1[0]} vs {semi_final_1[1]}")
        st.write(f"🔹 Semi Final 2: {semi_final_2[0]} vs {semi_final_2[1]}")

        sf1_score1 = st.number_input(f"Skor {semi_final_1[0]}", min_value=0, step=1, key="sf1_1")
        sf1_score2 = st.number_input(f"Skor {semi_final_1[1]}", min_value=0, step=1, key="sf1_2")

        sf2_score1 = st.number_input(f"Skor {semi_final_2[0]}", min_value=0, step=1, key="sf2_1")
        sf2_score2 = st.number_input(f"Skor {semi_final_2[1]}", min_value=0, step=1, key="sf2_2")

        if st.button("Konfirmasi Semi Final"):
            finalists = []
            finalists.append(semi_final_1[0] if sf1_score1 > sf1_score2 else semi_final_1[1])
            finalists.append(semi_final_2[0] if sf2_score1 > sf2_score2 else semi_final_2[1])
            st.session_state.final_teams = finalists

    if len(st.session_state.final_teams) == 2:
        st.subheader(f"🏆 Final: {st.session_state.final_teams[0]} vs {st.session_state.final_teams[1]}")
        final_score1 = st.number_input(f"Skor {st.session_state.final_teams[0]}", min_value=0, step=1, key="final1")
        final_score2 = st.number_input(f"Skor {st.session_state.final_teams[1]}", min_value=0, step=1, key="final2")

        if st.button("Konfirmasi Final"):
            if final_score1 > final_score2:
                st.session_state.champion = st.session_state.final_teams[0]
            elif final_score2 > final_score1:
                st.session_state.champion = st.session_state.final_teams[1]
            else:
                st.warning("Final harus memiliki pemenang!")

    if st.session_state.champion:
        st.subheader("🏆 Pemenang Turnamen 🏆")
        st.success(f"Selamat kepada {st.session_state.champion} sebagai juara kompetisi! 🎉")
        st.balloons()
