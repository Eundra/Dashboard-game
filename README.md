# 📖 README: Aplikasi Turnamen Sepak Bola ⚽

Proyek ini adalah aplikasi berbasis web yang dibuat dengan Streamlit untuk mengelola turnamen sepak bola, termasuk fitur pembuatan jadwal pertandingan, pencatatan hasil pertandingan, klasemen, dan babak championship.

## 🛠️ Fitur Utama
1. **Input Tim & Jadwal:**
   - Input daftar tim dan pembuatan jadwal otomatis dengan opsi Home & Away atau Sekali Bertemu.
2. **Klasemen:**
   - Menampilkan tabel klasemen dengan perhitungan poin otomatis.
3. **Riwayat Pertandingan:**
   - Menampilkan hasil pertandingan yang telah dikonfirmasi.
4. **Babak Championship:**
   - Memilih 4 tim terbaik untuk bertanding di babak semifinal dan final hingga menemukan juara.

---

## ⚙️ Instalasi

1. **Kloning Repositori:**
   ```bash
   git clone https://github.com/username/bagan-turnamen.git
   cd bagan-turnamen
   ```

2. **Buat Virtual Environment (Opsional):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   .\venv\Scripts\activate   # Untuk Windows
   ```

3. **Install Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi:**
   ```bash
   streamlit run bagan.py
   ```

---

## 🖥️ Penggunaan

1. **Input Tim:** Masukkan nama tim dengan dipisahkan koma (,) dan klik "Buat Jadwal Grup".
2. **Input Hasil Pertandingan:** Masukkan skor pada setiap pertandingan dan klik tombol "Konfirmasi".
3. **Pantau Klasemen:** Lihat perkembangan klasemen di tab "Klasemen".
4. **Cek Riwayat:** Lihat hasil pertandingan di tab "Riwayat".
5. **Championship:** Babak semifinal dan final akan otomatis muncul setelah semua pertandingan grup selesai.

---

## 🛠️ Teknologi yang Digunakan
- Python
- Streamlit
- Pandas
- Random

Selamat menggunakan aplikasi turnamen sepak bola ini! 🎉⚽