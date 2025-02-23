import streamlit as st
import pandas as pd

# Fungsi untuk menghasilkan jadwal pertandingan dengan sesi yang tidak bentrok
def generate_fixtures(teams, home_away=True):
    sessions = []
    base_fixtures = []
    num_teams = len(teams)
    
    for i in range(num_teams - 1):
        round_matches = []
        for j in range(num_teams // 2):
            home = teams[j]
            away = teams[num_teams - 1 - j]
            round_matches.append((home, away))
        sessions.append(round_matches)
        teams.insert(1, teams.pop())  # Rotasi tim
    
    if home_away:  # Jika Home & Away, tambahkan putaran kedua
        for fixtures in sessions:
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
if "champion" not in st.session_state:
    st.session_state.champion = None

if page == "Input & Jadwal":
    st.title("⚽ Input Tim & Jadwal")
    team_input = st.text_area("Masukkan tim (pisahkan dengan koma)", "")

    if st.button("Buat Jadwal Grup"):
        teams = [t.strip() for t in team_input.split(",") if t.strip()]
        if len(teams) < 4:
            st.error("Minimal harus memasukkan 4 tim!")
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
        winner = standings_df.index[0]
        st.success(f"🎉 Selamat tim {winner} memenangkan liga! Selamat berjuang di babak championship! 🎉")

if page == "Riwayat":
    st.title("📜 Riwayat Pertandingan")
    if not st.session_state.match_history:
        st.warning("Belum ada pertandingan yang dikonfirmasi.")
    else:
        for history in st.session_state.match_history:
            st.write(history)

if page == "Babak Championship":
    st.title("🏆 Babak Championship")

    standings_df = pd.DataFrame.from_dict(st.session_state.standings, orient='index')
    standings_df['GD'] = standings_df['GF'] - standings_df['GA']
    standings_df = standings_df.sort_values(by=['Pts', 'GD', 'GF'], ascending=[False, False, False])

    if len(standings_df) < 4:
        st.warning("Jumlah tim tidak cukup untuk babak championship!")
    else:
        teams = standings_df.index[:4].tolist()
        
        # Babak penyisihan awal
        st.subheader("🏅 Babak Penyisihan")
        st.write(f"{teams[0]} vs {teams[1]} (Perebutan tiket ke final)")
        st.write(f"{teams[2]} vs {teams[3]} (Perebutan tiket ke semi final)")
        
        score1 = st.number_input(f"Skor {teams[0]}", min_value=0, step=1, key="match1_team1")
        score2 = st.number_input(f"Skor {teams[1]}", min_value=0, step=1, key="match1_team2")
        score3 = st.number_input(f"Skor {teams[2]}", min_value=0, step=1, key="match2_team3")
        score4 = st.number_input(f"Skor {teams[3]}", min_value=0, step=1, key="match2_team4")

        if st.button("Konfirmasi Babak Penyisihan"):
            finalist = teams[0] if score1 > score2 else teams[1]
            semi_finalist = teams[3] if score3 > score4 else teams[2]
            loser_of_top_match = teams[1] if score1 > score2 else teams[0]
            st.session_state.semi_final_match = (semi_finalist, loser_of_top_match)
            st.session_state.finalist = finalist
            st.success(f"{finalist} melaju ke final!")
            st.success(f"{semi_finalist} melaju ke semi final melawan {loser_of_top_match}!")
        
        # Semi Final
        if "semi_final_match" in st.session_state:
            st.subheader("🏅 Semi Final")
            teamA, teamB = st.session_state.semi_final_match
            scoreA = st.number_input(f"Skor {teamA}", min_value=0, step=1, key="semi_teamA")
            scoreB = st.number_input(f"Skor {teamB}", min_value=0, step=1, key="semi_teamB")

            if st.button("Konfirmasi Semi Final"):
                semi_winner = teamA if scoreA > scoreB else teamB
                st.session_state.finalist2 = semi_winner
                st.success(f"{semi_winner} melaju ke Final melawan {st.session_state.finalist}!")

        # Final
        if "finalist2" in st.session_state:
            st.subheader("🏆 Final")
            score_final1 = st.number_input(f"Skor {st.session_state.finalist}", min_value=0, step=1, key="final1")
            score_final2 = st.number_input(f"Skor {st.session_state.finalist2}", min_value=0, step=1, key="final2")

            if st.button("Konfirmasi Final"):
                champion = st.session_state.finalist if score_final1 > score_final2 else st.session_state.finalist2
                st.session_state.champion = champion
                st.success(f"🎉 Selamat! {champion} adalah juara Babak Championship! 🎉")
                st.balloons()

                st.markdown("""
                    <iframe width="560" height="315" 
                    src="https://www.youtube.com/embed/04854XqcfCY?autoplay=1" 
                    frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
                    encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
                    </iframe>
                """, unsafe_allow_html=True)
                # st.audio("we_are_the_champions.mp3")  # Putar lagu We Are The Champions
