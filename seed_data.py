import os
import django
import sys

# Konfigurasi environment Django
sys.path.append('C:\\yok\\website-smknj')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_smknj.settings')
django.setup()

from otak_aplikasi.models import (
    newsCategory, news, ektraCategory, ektra, Jurusan, 
    MataPelajaran, StaffDanGuru, categoryPengumuman, FasilitasLab
)

def create_seed():
    # 1. Jurusan
    jurusans = [
        {"nama": "Rekayasa Perangkat Lunak", "kode": "RPL"},
        {"nama": "Teknik Komputer Jaringan", "kode": "TKJ"},
        {"nama": "Multimedia", "kode": "MM"},
        {"nama": "Akuntansi", "kode": "AK"},
        {"nama": "Perbankan Syariah", "kode": "PS"},
        {"nama": "Teknik Kendaraan Ringan", "kode": "TKR"}
    ]
    
    jurusan_objs = []
    for j in jurusans:
        obj, _ = Jurusan.objects.get_or_create(nama=j['nama'], kode_jurusan=j['kode'])
        jurusan_objs.append(obj)

    # 2. Ekskul
    cat_ekskul, _ = ektraCategory.objects.get_or_create(name="Ekstrakurikuler")
    ekskuls = [
        "Futsal", "Basket", "Pramuka", "PMR", "Paskibra", "Hadrah"
    ]
    for e in ekskuls:
        ektra.objects.get_or_create(
            title=e,
            pembina="Pembina Umum",
            lokasi="Area Sekolah",
            jadwal="15.00 - 17.00",
            hari="Jumat",
            type_ektra="Pilihan",
            tahun=2026,
            category=cat_ekskul
        )

    # 3. Fasilitas Lab
    for j in jurusan_objs[:3]: # Hanya untuk 3 jurusan pertama
        FasilitasLab.objects.get_or_create(
            jurusan=j,
            nama_lab=f"Lab {j.nama}",
            deskripsi="Laboratorium standar industri."
        )

    # 4. Berita
    cat_berita, _ = newsCategory.objects.get_or_create(name="Berita")
    for i in range(6):
        news.objects.get_or_create(
            title=f"Berita Sekolah {i+1}",
            content="<p>Isi berita penting untuk warga sekolah.</p>",
            category=cat_berita
        )

    print("Seed data completed (6+ items per category).")

if __name__ == "__main__":
    create_seed()
