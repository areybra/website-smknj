# Project Documentation: SMK Nurul Jadid Web Portal 2026

## Overview
Portal website resmi untuk SMK Nurul Jadid (versi 2026) yang dibangun menggunakan framework Django dan basis data MySQL. Website ini berfungsi sebagai CMS untuk mengelola profil sekolah, berita, pengumuman, daftar jurusan (program keahlian), fasilitas laboratorium, informasi ekstrakurikuler, serta dashboard statistik sekolah.

## Tech Stack
- **Backend**: Python 3.x, Django 4.2+
- **Database**: MySQL
- **Frontend**: HTML5, Tailwind CSS (CDN), Material Symbols (Icons)
- **Editor**: CKEditor (Rich Text Editor)
- **Caching**: Django Local Memory Cache
- **Admin Panel**: Django Jazzmin

## Project Structure
```
website-smknj/
├── .git/                 # Git repository
├── .gitignore
├── manage.py             # Django management script
├── media/                # User uploaded files (news images, teacher photos, etc.)
├── otak_aplikasi/        # Main application logic (models, views, templates)
├── README.md
├── requirements.txt      # Python dependencies
├── static/               # Static assets (custom CSS, JS, logo images)
├── templates/            # Main HTML templates and base layouts
├── venv/                 # Virtual environment
└── web_smknj/            # Django project core configuration
```

## Key Features
1. **Pusat Informasi Berita & Pengumuman** - CMS untuk publikasi berita sekolah dan pengumuman penting dengan kategori
2. **Profil Sekolah & Struktur Organisasi** - Sejarah, visi-misi, daftar tenaga pendidik dan kependidikan
3. **Program Keahlian (Jurusan)** - Katalog lengkap jurusan dengan kompetensi, prospek karir, testimoni alumni
4. **Fasilitas & Lab** - Dokumentasi laboratorium dan peralatan penunjang pembelajaran
5. **Ekstrakurikuler** - Jadwal dan kegiatan pengembangan diri siswa
6. **Statistik Sekolah Dinamis** - Dashboard statistik siswa, instruktur, mitra industri
7. **Pencarian Global** - Pencarian informasi di seluruh modul website
8. **Admin Panel Premium** - Django Jazzmin untuk manajemen data modern

## Installation & Setup
1. Clone repository
2. Create virtual environment: `python -m venv env`
3. Activate: `env\Scripts\activate` (Windows) / `source env/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure MySQL database named `web_smknj_db` in `web_smknj/settings.py`
6. Run migrations: `python manage.py makemigrations && python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

## Main Application Modules (otak_aplikasi)
Berisi logika utama aplikasi termasuk models, views, dan templates untuk:
- Manajemen berita dan pengumuman
- Profil sekolah dan struktur organisasi
- Program keahlian/jurusan
- Fasilitas dan laboratorium
- Ekstrakurikuler
- Statistik sekolah
- Pencarian global

## Configuration Files
- `web_smknj/settings.py` - Django settings, database config, installed apps
- `web_smknj/urls.py` - URL routing utama
- `requirements.txt` - Python package dependencies

## Development Commands
```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

## Access URLs
- Website: `http://127.0.0.1:8000/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

## Notes for Future Development
- Uses Django 4.2+ with modern class-based views
- Frontend uses Tailwind CSS via CDN (no build step required)
- Rich text editing via CKEditor
- Admin interface customized with Jazzmin
- Static files served via Django staticfiles
- Media files stored in `media/` directory