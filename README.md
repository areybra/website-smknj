# SMK Nurul Jadid Web Portal 2026

Selamat datang di repositori resmi Web Portal SMK Nurul Jadid versi 2026. Proyek ini dibangun menggunakan Django Framework untuk memberikan informasi lengkap mengenai profil sekolah, berita, pengumuman, dan fasilitas bagi siswa maupun masyarakat umum.

## 🚀 Fitur Utama

*   **Pusat Informasi Berita & Pengumuman**: Sistem manajemen konten (CMS) untuk publikasi berita sekolah dan pengumuman penting dengan kategori pendukung.
*   **Profil Sekolah & Struktur Organisasi**: Informasi detail mengenai sejarah, visi-misi, serta daftar tenaga pendidik dan kependidikan.
*   **Program Keahlian (Jurusan)**: Katalog lengkap jurusan dengan informasi kompetensi, prospek karir, dan testimoni alumni.
*   **Fasilitas & Lab**: Dokumentasi laboratorium dan peralatan penunjang pembelajaran di setiap jurusan.
*   **Ekstrakurikuler**: Informasi jadwal dan kegiatan pengembangan diri siswa di luar jam pelajaran.
*   **Statistik Sekolah Dinamis**: Dashboard statistik siswa, instruktur, dan mitra industri yang terintegrasi.
*   **Pencarian Global**: Memudahkan pengguna menemukan informasi di seluruh modul website.
*   **Admin Panel Premium**: Menggunakan Django Jazzmin untuk antarmuka manajemen data yang modern dan user-friendly.

## 🛠️ Tech Stack

*   **Backend**: Python 3.x, Django 4.2+
*   **Database**: MySQL
*   **Frontend**: HTML5, Tailwind CSS (CDN), Material Symbols (Icons)
*   **Editor**: CKEditor (Rich Text Editor)
*   **Cashing**: Django Local Memory Cache

## 📋 Prasyarat

Sebelum memulai, pastikan Anda telah menginstal:
*   Python 3.8 atau versi di atasnya
*   MySQL Server
*   Virtualenv (disarankan)

## ⚙️ Instalasi

Ikuti langkah-langkah di bawah ini untuk menjalankan project di lingkungan lokal:

1.  **Clone Repositori**
    ```bash
    git clone https://github.com/username/web-smknj-2026.git
    cd web-smknj-2026
    ```

2.  **Buat Virtual Environment**
    ```bash
    python -m venv env
    ```

3.  **Aktifkan Virtual Environment**
    *   Windows: `env\Scripts\activate`
    *   Linux/Mac: `source env/bin/activate`

4.  **Instal Dependensi**
    Gunakan file `requirements.txt` untuk menginstal semua library yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Konfigurasi Database**
    Buat database di MySQL dengan nama `web_smknj_db`. Sesuaikan username dan password database Anda di file `web_smknj/settings.py` pada bagian `DATABASES`.

6.  **Migrasi Database**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7.  **Buat Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

## 🏃 Menjalankan Aplikasi

Jalankan server pengembangan dengan perintah:
```bash
python manage.py runserver
```
Buka browser dan akses `http://127.0.0.1:8000/`. Untuk masuk ke dashboard admin, akses `http://127.0.0.1:8000/admin/`.

## 📁 Struktur Folder Utama

*   `otak_aplikasi/`: Berisi logika utama aplikasi (models, views, templates).
*   `web_smknj/`: Konfigurasi inti project Django.
*   `static/`: File aset statis (CSS custom, JS, Gambar logo).
*   `media/`: File yang diunggah oleh pengguna (Gambar berita, foto guru, dll).
*   `templates/`: File HTML utama dan layout dasar.

## 🤝 Kontribusi

Jika Anda ingin berkontribusi, silakan lakukan fork pada repositori ini dan buat pull request, atau buka issue untuk melaporkan bug atau saran fitur baru.

---
© 2026 SMK Nurul Jadid - Membangun Masa Depan dengan Teknologi.
