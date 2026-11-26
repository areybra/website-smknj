"""
Seed data dummy lengkap untuk SMK Nurul Jadid.

Idempoten: aman dijalankan berulang. Semua baris dicari lewat kunci alami
(slug / nama) lalu dibuat atau diperbarui, tidak pernah diduplikasi.

Jalankan:
    python manage.py seed_dummy
"""
from datetime import timedelta

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.utils import timezone

from otak_aplikasi.models import (
    Kompetensi,
    FasilitasJurusan,
    FasilitasLab,
    Jurusan,
    MataPelajaran,
    MitraIndustri,
    Pengumuman,
    PeralatanLab,
    ProspekKarir,
    SchoolStatistics,
    Sertifikasi,
    StaffDanGuru,
    TestimoniAlumni,
    categoryPengumuman,
    ektra,
    ektraCategory,
    news,
    newsCategory,
)


JURUSAN_DATA = {
    "rekayasa-perangkat-lunak": {
        "kode": "RPL",
        "siswa": 216,
        "guru": 9,
        "lab": 3,
        "serapan": "94%",
        "gedung": "A Lt. 2",
        "kaprodi": "Ahmad Fauzi, S.Kom.",
        "email": "rpl@smknuruljadid.sch.id",
        "kontak": "(0335) 881-201",
        "deskripsi": "Mempelajari rekayasa perangkat lunak mulai dari pemrograman, basis data, "
        "pengembangan web dan mobile, hingga pengujian perangkat lunak.",
        "hard": ["Pemrograman Dasar", "Basis Data MySQL", "Pemrograman Web", "Pemrograman Mobile", "Pengujian Perangkat Lunak"],
        "soft": ["Kerja Tim", "Berpikir Kritis", "Manajemen Waktu"],
        "fasilitas": [
            ("Lab Pemrograman", "24 workstation untuk praktik pemrograman dan pengujian kode.", "code"),
            ("Lab Basis Data", "Ruang praktik perancangan dan administrasi basis data.", "dns"),
            ("Studio Proyek", "Ruang kolaborasi pengerjaan proyek perangkat lunak.", "groups"),
        ],
        "karir": [
            ("Web Developer", "Membangun dan memelihara aplikasi berbasis web.", "Rp 5-9 juta"),
            ("Mobile Developer", "Mengembangkan aplikasi Android dan iOS.", "Rp 6-10 juta"),
            ("Quality Assurance", "Menguji kualitas perangkat lunak sebelum rilis.", "Rp 5-8 juta"),
        ],
        "sertifikasi": [("Junior Web Developer", "BNSP"), ("Oracle Database Foundation", "Oracle Academy")],
        "mitra": ["PT Telkom Indonesia", "Bank Jatim", "PT Sido Muncul"],
        "alumni": [
            ("Dina Maulida", "Software Engineer", "Tokopedia", 2021, "Bekal praktik di RPL sangat membantu saya masuk industri teknologi."),
            ("Rizky Ramadhan", "Backend Developer", "PT Telkom Indonesia", 2020, "Guru-guru membimbing sampai saya siap kerja."),
        ],
    },
    "teknik-komputer-jaringan": {
        "kode": "TKJ",
        "siswa": 198,
        "guru": 8,
        "lab": 3,
        "serapan": "92%",
        "gedung": "B Lt. 1",
        "kaprodi": "Siti Nurhaliza, S.T.",
        "email": "tkj@smknuruljadid.sch.id",
        "kontak": "(0335) 881-202",
        "deskripsi": "Fokus pada instalasi jaringan, administrasi server, keamanan siber, "
        "dan teknologi cloud yang dibutuhkan industri.",
        "hard": ["Instalasi Jaringan", "Administrasi Server", "Keamanan Jaringan", "Konfigurasi Router", "Cloud Dasar"],
        "soft": ["Disiplin", "Komunikasi Teknis", "Problem Solving"],
        "fasilitas": [
            ("Lab Jaringan", "Praktik pengkabelan, konfigurasi router dan switch.", "router"),
            ("Server Room", "Ruang server untuk praktik administrasi sistem.", "storage"),
            ("Lab Fiber Optik", "Praktik splicing dan pengukuran fiber optik.", "cable"),
        ],
        "karir": [
            ("Network Administrator", "Mengelola infrastruktur jaringan perusahaan.", "Rp 5-9 juta"),
            ("Teknisi Fiber Optik", "Instalasi dan pemeliharaan jaringan fiber optik.", "Rp 4-7 juta"),
            ("Cloud Support", "Mendukung layanan cloud dan server virtual.", "Rp 6-10 juta"),
        ],
        "sertifikasi": [("MTCNA", "MikroTik"), ("CCNA", "Cisco Networking Academy")],
        "mitra": ["PT Telkom Akses", "Indosat Ooredoo", "PT Petrokimia Gresik"],
        "alumni": [
            ("Fajar Hidayat", "Network Engineer", "Indosat Ooredoo", 2019, "Lab jaringan sekolah sangat mirip dengan perangkat di tempat kerja."),
            ("Nur Aini", "NOC Analyst", "PT Telkom Akses", 2022, "Praktik langsung membuat saya cepat beradaptasi."),
        ],
    },
    "multimedia": {
        "kode": "MM",
        "siswa": 184,
        "guru": 7,
        "lab": 3,
        "serapan": "90%",
        "gedung": "A Lt. 3",
        "kaprodi": "Bayu Prakoso, S.Ds.",
        "email": "multimedia@smknuruljadid.sch.id",
        "kontak": "(0335) 881-203",
        "deskripsi": "Mengasah desain grafis, fotografi, videografi, animasi, dan produksi konten digital.",
        "hard": ["Desain Grafis", "Fotografi", "Videografi", "Animasi 2D", "Editing Video"],
        "soft": ["Kreativitas", "Kolaborasi", "Presentasi"],
        "fasilitas": [
            ("Studio Foto", "Studio dengan lighting dan backdrop untuk praktik fotografi.", "photo_camera"),
            ("Studio Video", "Ruang produksi dan editing video dengan green screen.", "videocam"),
            ("Lab Desain", "Workstation grafis dengan perangkat lunak desain industri.", "palette"),
        ],
        "karir": [
            ("Graphic Designer", "Merancang identitas visual dan materi promosi.", "Rp 4-8 juta"),
            ("Video Editor", "Mengedit konten video untuk media digital.", "Rp 4-7 juta"),
            ("Content Creator", "Memproduksi konten untuk kanal digital brand.", "Rp 4-9 juta"),
        ],
        "sertifikasi": [("Adobe Certified Professional", "Adobe"), ("Desainer Grafis Muda", "BNSP")],
        "mitra": ["Net TV", "Jawa Pos", "Studio Kreatif Malang"],
        "alumni": [
            ("Ayu Lestari", "Art Director", "Studio Kreatif Malang", 2020, "Portofolio dari kelas multimedia jadi modal utama saya."),
            ("Bagus Setiawan", "Video Editor", "Jawa Pos", 2021, "Studio sekolah lengkap, jadi terbiasa produksi nyata."),
        ],
    },
    "akuntansi": {
        "kode": "AKL",
        "siswa": 172,
        "guru": 7,
        "lab": 2,
        "serapan": "93%",
        "gedung": "C Lt. 1",
        "kaprodi": "Dewi Kartika, S.E.",
        "email": "akuntansi@smknuruljadid.sch.id",
        "kontak": "(0335) 881-204",
        "deskripsi": "Membekali siswa dengan akuntansi keuangan, perpajakan, komputer akuntansi, "
        "dan administrasi perkantoran.",
        "hard": ["Akuntansi Dasar", "Komputer Akuntansi", "Perpajakan", "Laporan Keuangan", "Administrasi Transaksi"],
        "soft": ["Teliti", "Integritas", "Etika Profesi"],
        "fasilitas": [
            ("Lab Akuntansi", "Praktik siklus akuntansi dengan aplikasi ACCURATE.", "calculate"),
            ("Bank Mini", "Simulasi transaksi perbankan dan kasir.", "account_balance"),
            ("Ruang Arsip", "Praktik pengelolaan dokumen dan arsip keuangan.", "folder"),
        ],
        "karir": [
            ("Staff Akuntansi", "Menyusun dan memverifikasi laporan keuangan.", "Rp 4-7 juta"),
            ("Staff Pajak", "Mengelola pelaporan dan administrasi perpajakan.", "Rp 4-7 juta"),
            ("Teller Bank", "Melayani transaksi perbankan nasabah.", "Rp 4-6 juta"),
        ],
        "sertifikasi": [("Akuntansi Muda", "BNSP"), ("Brevet A & B", "Ikatan Akuntan Indonesia")],
        "mitra": ["Bank Jatim", "Koperasi Sejahtera", "Kantor Konsultan Pajak Malang"],
        "alumni": [
            ("Putri Anggraini", "Staff Akuntansi", "Bank Jatim", 2021, "Praktik bank mini membuat saya paham alur transaksi nyata."),
            ("Hendra Wijaya", "Staff Pajak", "Kantor Konsultan Pajak Malang", 2020, "Guru akuntansi sangat detail membimbing."),
        ],
    },
    "perbankan-syariah": {
        "kode": "PBS",
        "siswa": 148,
        "guru": 6,
        "lab": 2,
        "serapan": "91%",
        "gedung": "C Lt. 2",
        "kaprodi": "Muhammad Ridwan, S.E.I.",
        "email": "perbankan@smknuruljadid.sch.id",
        "kontak": "(0335) 881-205",
        "deskripsi": "Mempelajari operasional perbankan syariah, akad, produk pembiayaan, "
        "dan layanan nasabah berbasis prinsip syariah.",
        "hard": ["Fikih Muamalah", "Akad Perbankan", "Produk Pembiayaan", "Layanan Nasabah", "Komputer Perbankan"],
        "soft": ["Ramah", "Komunikasi", "Amanah"],
        "fasilitas": [
            ("Lab Bank Syariah", "Simulasi teller dan customer service syariah.", "account_balance"),
            ("Ruang Konsultasi", "Praktik konsultasi produk pembiayaan syariah.", "support_agent"),
            ("Perpustakaan Syariah", "Koleksi literatur ekonomi dan perbankan syariah.", "menu_book"),
        ],
        "karir": [
            ("Customer Service Syariah", "Melayani kebutuhan nasabah bank syariah.", "Rp 4-6 juta"),
            ("Staff Pembiayaan", "Menganalisis dan memproses pengajuan pembiayaan.", "Rp 4-7 juta"),
            ("Teller Syariah", "Menangani transaksi tunai sesuai akad syariah.", "Rp 4-6 juta"),
        ],
        "sertifikasi": [("Perbankan Syariah", "BNSP"), ("Lembaga Sertifikasi Profesi Syariah", "LSPBS")],
        "mitra": ["Bank Syariah Indonesia", "BMT Nurul Jadid", "Koperasi Syariah Malang"],
        "alumni": [
            ("Laila Rahmawati", "Customer Service", "Bank Syariah Indonesia", 2022, "Praktik layanan nasabah di lab sangat membantu."),
            ("Ahmad Syarif", "Staff Pembiayaan", "BMT Nurul Jadid", 2021, "Nilai syariah dan teknis diajarkan seimbang."),
        ],
    },
    "teknik-kendaraan-ringan": {
        "kode": "TKR",
        "siswa": 205,
        "guru": 9,
        "lab": 3,
        "serapan": "95%",
        "gedung": "D Lt. 1",
        "kaprodi": "Joko Susilo, S.T.",
        "email": "tkr@smknuruljadid.sch.id",
        "kontak": "(0335) 881-206",
        "deskripsi": "Menguasai perawatan mesin, sistem kelistrikan, sasis, dan teknologi "
        "kendaraan ringan modern.",
        "hard": ["Perawatan Mesin", "Sistem Kelistrikan", "Sasis & Pemindah Tenaga", "Diagnosa Mesin", "Kendaraan Listrik Dasar"],
        "soft": ["Keselamatan Kerja", "Ketekunan", "Kerja Tim"],
        "fasilitas": [
            ("Bengkel Mesin", "Praktik pembongkaran dan perawatan mesin kendaraan.", "build"),
            ("Lab Kelistrikan", "Praktik sistem kelistrikan dan sensor kendaraan.", "bolt"),
            ("Lab Diagnosa", "Alat scan dan diagnosa kendaraan modern.", "troubleshoot"),
        ],
        "karir": [
            ("Teknisi Otomotif", "Merawat dan memperbaiki kendaraan ringan.", "Rp 4-7 juta"),
            ("Service Advisor", "Menangani konsultasi dan estimasi perbaikan.", "Rp 4-7 juta"),
            ("Teknisi EV", "Merawat sistem kendaraan listrik.", "Rp 5-9 juta"),
        ],
        "sertifikasi": [("Teknisi Otomotif Muda", "BNSP"), ("Toyota Technical Education Program", "Toyota")],
        "mitra": ["Astra International", "PT Toyota Astra Motor", "Daihatsu Malang"],
        "alumni": [
            ("Wahyu Kurniawan", "Teknisi Senior", "Astra International", 2019, "Bengkel sekolah jadi tempat saya belajar standar industri."),
            ("Iqbal Maulana", "Service Advisor", "Daihatsu Malang", 2021, "Komunikasi pelanggan diajarkan sejak kelas XI."),
        ],
    },
}


NEWS_DATA = [
    ("Prestasi Siswa RPL Juara 1 LKS Provinsi Jawa Timur", "Prestasi", 12),
    ("SMK Nurul Jadid Gelar Workshop AI untuk Guru", "Kegiatan", 9),
    ("Kunjungan Industri Kelas XII ke PT Telkom Surabaya", "Kegiatan", 8),
    ("Tiga Tim TKJ Lolos Seleksi Kompetisi Jaringan Nasional", "Prestasi", 11),
    ("Pengumuman Jadwal Ujian Tengah Semester Ganjil 2026", "Akademik", 15),
    ("Multimedia Produksi Film Pendek \"Jejak Santri\"", "Kegiatan", 7),
    ("Program Praktik Kerja Lapangan Angkatan 2024 Dimulai", "Akademik", 10),
    ("Akuntansi Raih Juara 2 Lomba Cerdas Cermat Perpajakan", "Prestasi", 6),
    ("Peringatan Hari Santri Nasional Berlangsung Khidmat", "Kegiatan", 5),
    ("Pendaftaran Ekstrakurikuler Semester Genap Dibuka", "Akademik", 4),
]

NEWS_BODY = (
    "<p>Kegiatan ini merupakan bagian dari komitmen SMK Nurul Jadid dalam menghubungkan "
    "pembelajaran di kelas dengan kebutuhan dunia industri. Seluruh siswa terlibat aktif "
    "mulai dari persiapan, pelaksanaan, hingga evaluasi.</p>"
    "<p>Kepala sekolah menyampaikan apresiasi kepada siswa dan guru pembimbing atas kerja "
    "keras yang ditunjukkan. Kegiatan serupa akan dilanjutkan pada semester berikutnya "
    "dengan cakupan yang lebih luas.</p>"
)


EKTRA_DATA = [
    ("Pramuka", "Wajib", "Keagamaan", "Sabtu", "07.00 - 09.00", "Ahmad Subari", "Lapangan Utama", 120, 5),
    ("PMR", "Wajib", "Akademik", "Jumat", "13.00 - 15.00", "Rina Kusuma, S.Kep.", "Ruang Kesehatan", 90, 3),
    ("Futsal", "Pilihan", "Olahraga", "Jumat", "15.00 - 17.00", "Dimas Prasetyo", "Lapangan Futsal", 34, 7),
    ("Basket", "Pilihan", "Olahraga", "Rabu", "15.00 - 17.00", "Yusuf Hakim", "Lapangan Basket", 28, 4),
    ("Hadrah", "Pilihan", "Keagamaan", "Kamis", "13.00 - 15.00", "Ust. Zainal Abidin", "Aula Sekolah", 40, 6),
    ("Paskibra", "Pilihan", "Akademik", "Sabtu", "09.00 - 11.00", "Letda Suparman", "Lapangan Utama", 32, 5),
    ("Robotik", "Pilihan", "Akademik", "Selasa", "13.00 - 15.00", "Fajar Nugroho, S.T.", "Lab Robotik", 24, 2),
    ("Seni Tari", "Pilihan", "Seni", "Sabtu", "13.00 - 15.00", "Wulan Sari", "Aula Sekolah", 26, 3),
]

EKTRA_BODY = (
    "Ekstrakurikuler ini menjadi wadah pengembangan minat, bakat, dan karakter siswa di luar "
    "kegiatan akademik. Latihan rutin dilaksanakan setiap pekan dengan pembina berpengalaman."
)

PENGUMUMAN_DATA = [
    ("Pengumuman Libur Idul Fitri 1447 H", "Akademik", True),
    ("Jadwal Ujian Akhir Semester Ganjil", "Akademik", False),
    ("Pendaftaran Praktik Kerja Lapangan Dibuka", "Akademik", False),
    ("Pemilihan Ketua OSIS Periode 2026/2027", "Kesiswaan", False),
    ("Sosialisasi Program Beasiswa Prestasi", "Umum", False),
    ("Pemberitahuan Perubahan Jam Pulang Sekolah", "Umum", False),
]

PENGUMUMAN_BODY = (
    "<p>Diberitahukan kepada seluruh siswa, guru, dan tenaga kependidikan SMK Nurul Jadid "
    "untuk memperhatikan informasi berikut. Mohon membaca dengan saksama dan mengikuti "
    "ketentuan yang berlaku.</p>"
    "<p>Informasi lebih lanjut dapat ditanyakan kepada wali kelas atau bagian administrasi "
    "sekolah pada jam kerja.</p>"
)

MAPEL = [
    "Matematika", "Bahasa Indonesia", "Bahasa Inggris", "Pendidikan Agama Islam",
    "Pendidikan Pancasila", "Informatika", "PJOK", "Sejarah Indonesia",
    "Produk Kreatif dan Kewirausahaan", "Projek IPAS",
]

STAFF_DATA = [
    ("KH. Abdul Aziz, M.Pd.", "Kepala Sekolah", "S1 Pendidikan Agama Islam, S2 Manajemen Pendidikan", "Memimpin pengembangan sekolah menuju SMK Pusat Keunggulan."),
    ("Hj. Nurul Hidayah, S.Pd.", "Wakil Kepala Sekolah Bidang Akademik", "S1 Pendidikan Matematika", "Mengelola kurikulum dan penjaminan mutu akademik."),
    ("Ahmad Fauzi, S.Kom.", "Ketua Program Keahlian RPL", "S1 Teknik Informatika", "Membina program keahlian rekayasa perangkat lunak."),
    ("Siti Nurhaliza, S.T.", "Ketua Program Keahlian TKJ", "S1 Teknik Telekomunikasi", "Membina program keahlian teknik komputer dan jaringan."),
    ("Bayu Prakoso, S.Ds.", "Ketua Program Keahlian Multimedia", "S1 Desain Komunikasi Visual", "Membina program keahlian multimedia dan produksi konten."),
    ("Dewi Kartika, S.E.", "Guru Akuntansi", "S1 Akuntansi", "Mengajar akuntansi keuangan dan komputer akuntansi."),
    ("Muhammad Ridwan, S.E.I.", "Guru Perbankan Syariah", "S1 Ekonomi Islam", "Mengajar fikih muamalah dan produk perbankan syariah."),
    ("Joko Susilo, S.T.", "Guru Teknik Kendaraan Ringan", "S1 Teknik Mesin", "Mengajar perawatan mesin dan sistem kelistrikan kendaraan."),
    ("Rina Kusuma, S.Kep.", "Pembina PMR", "S1 Keperawatan", "Membina ekstrakurikuler palang merah remaja."),
]

LAB_EQUIPMENT = [
    ("Peralatan Utama", "Komputer Workstation"),
    ("Peralatan Utama", "Proyektor Interaktif"),
    ("Fitur Tambahan", "Pendingin Ruangan"),
    ("Perangkat Lunak", "Lisensi Aplikasi Industri"),
]


class Command(BaseCommand):
    help = "Isi database dengan data dummy lengkap (idempoten)."

    def handle(self, *args, **options):
        self.stdout.write("Seeding jurusan...")
        jurusan_map = self._seed_jurusan()

        self.stdout.write("Seeding berita...")
        self._seed_news()

        self.stdout.write("Seeding ekstrakurikuler...")
        self._seed_ektra()

        self.stdout.write("Seeding pengumuman...")
        self._seed_pengumuman()

        self.stdout.write("Seeding guru & staff...")
        self._seed_staff()

        self.stdout.write("Seeding laboratorium...")
        self._seed_labs(jurusan_map)

        self.stdout.write("Seeding statistik sekolah...")
        self._seed_stats()

        cache.clear()
        self.stdout.write(self.style.SUCCESS("Selesai. Semua data dummy tersedia."))

    # ------------------------------------------------------------------ helpers

    def _jurusan(self, slug):
        return Jurusan.objects.get(slug=slug)

    def _seed_jurusan(self):
        jurusan_map = {}
        for slug, d in JURUSAN_DATA.items():
            obj = self._jurusan(slug)
            jurusan_map[slug] = obj
            obj.kode_jurusan = d["kode"]
            obj.deskripsi_singkat = d["deskripsi"]
            obj.deskripsi_lengkap = f"<p>{d['deskripsi']}</p>"
            obj.kategori = "Teknologi"
            obj.durasi = "3 Tahun"
            obj.jumlah_siswa = d["siswa"]
            obj.guru_count = d["guru"]
            obj.lab_count = d["lab"]
            obj.serapan_kerja = d["serapan"]
            obj.kuota = 72
            obj.kaprodi_nama = d["kaprodi"]
            obj.kaprodi_email = d["email"]
            obj.kontak = d["kontak"]
            obj.gedung = d["gedung"]
            obj.save()

            for nama in d["hard"]:
                Kompetensi.objects.get_or_create(jurusan=obj, nama=nama, tipe="Hard")
            for nama in d["soft"]:
                Kompetensi.objects.get_or_create(jurusan=obj, nama=nama, tipe="Soft")

            for nama, deskripsi, icon in d["fasilitas"]:
                FasilitasJurusan.objects.get_or_create(
                    jurusan=obj, nama=nama, defaults={"deskripsi": deskripsi, "icon": icon}
                )

            for posisi, deskripsi, gaji in d["karir"]:
                ProspekKarir.objects.get_or_create(
                    jurusan=obj, posisi=posisi, defaults={"deskripsi": deskripsi, "rata_gaji": gaji}
                )

            for nama, penyelenggara in d["sertifikasi"]:
                Sertifikasi.objects.get_or_create(
                    jurusan=obj, nama=nama, defaults={"penyelenggara": penyelenggara}
                )

            for nama in d["mitra"]:
                MitraIndustri.objects.get_or_create(jurusan=obj, nama=nama)

            for nama, jabatan, perusahaan, tahun, testimoni in d["alumni"]:
                TestimoniAlumni.objects.get_or_create(
                    jurusan=obj,
                    nama=nama,
                    defaults={
                        "jabatan": jabatan,
                        "perusahaan": perusahaan,
                        "tahun_lulus": tahun,
                        "testimoni": testimoni,
                    },
                )
        return jurusan_map

    def _seed_news(self):
        # Reuse the placeholder rows left by the earlier seed instead of piling
        # new rows on top of them.
        placeholders = list(news.objects.filter(title__startswith="Berita Sekolah ").order_by("id"))
        for index, (title, category_name, views) in enumerate(NEWS_DATA):
            category, _ = newsCategory.objects.get_or_create(name=category_name)
            obj = news.objects.filter(title=title).first()
            if obj is None and index < len(placeholders):
                obj = placeholders[index]
                obj.title = title
                obj.slug = ""
            if obj is None:
                obj = news(title=title, category=category)
            obj.category = category
            obj.content = NEWS_BODY
            obj.view_count = views
            obj.save()
            news.objects.filter(pk=obj.pk).update(
                created_at=timezone.now() - timedelta(days=index * 2)
            )

    def _seed_ektra(self):
        for title, tipe, category_name, hari, jadwal, pembina, lokasi, siswa, prestasi in EKTRA_DATA:
            category, _ = ektraCategory.objects.get_or_create(name=category_name)
            obj = ektra.objects.filter(title=title).first()
            if obj is None:
                obj = ektra(title=title, pembina=pembina, lokasi=lokasi, jadwal=jadwal,
                            hari=hari, type_ektra=tipe, tahun=2026, category=category)
            obj.category = category
            obj.pembina = pembina
            obj.lokasi = lokasi
            obj.content = EKTRA_BODY
            obj.jadwal = jadwal
            obj.hari = hari
            obj.type_ektra = tipe
            obj.siswa_aktif = siswa
            obj.prestasi = prestasi
            obj.tahun = 2026
            obj.save()

    def _seed_pengumuman(self):
        for judul, category_name, penting in PENGUMUMAN_DATA:
            category, _ = categoryPengumuman.objects.get_or_create(nama=category_name)
            obj, _ = Pengumuman.objects.get_or_create(judul=judul, defaults={"category": category})
            obj.category = category
            obj.deskripsi = PENGUMUMAN_BODY
            obj.penting = penting
            obj.save()

    def _seed_staff(self):
        mapel_objs = [MataPelajaran.objects.get_or_create(nama=n)[0] for n in MAPEL]
        for nama, jabatan, pendidikan, deskripsi in STAFF_DATA:
            obj, _ = StaffDanGuru.objects.get_or_create(nama=nama, defaults={"jabatan": jabatan})
            obj.jabatan = jabatan
            obj.pendidikan = pendidikan
            obj.deskripsi = deskripsi
            obj.save()
            obj.mata_pelajaran.set(mapel_objs[:3])

    def _seed_labs(self, jurusan_map):
        for slug, obj in jurusan_map.items():
            data = JURUSAN_DATA[slug]
            if not obj.laboratorium.exists():
                for nama, deskripsi, icon in data["fasilitas"][:2]:
                    FasilitasLab.objects.create(
                        jurusan=obj, nama_lab=nama, deskripsi=deskripsi, icon=icon
                    )
            for lab in obj.laboratorium.all():
                for kategori, nama_alat in LAB_EQUIPMENT:
                    PeralatanLab.objects.get_or_create(
                        fasilitas_lab=lab, nama_peralatan=nama_alat, defaults={"kategori": kategori}
                    )

    def _seed_stats(self):
        obj = SchoolStatistics.objects.filter(is_active=True).first()
        if obj is None:
            obj = SchoolStatistics(is_active=True)
        obj.persentase_pertumbuhan_siswa = "+8%"
        obj.progress_siswa = 88
        obj.status_instruktur = "Sertifikasi BNSP"
        obj.progress_instruktur = 95
        obj.label_mitra = "Perusahaan"
        obj.save()
        return obj
