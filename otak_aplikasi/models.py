from django.db import models
import os
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone

# Buat model Anda di sini.
class newsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
            original_slug = self.slug
            counter = 1
            while newsCategory.objects.filter(slug=self.slug).exists():
                if self.pk and newsCategory.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    self.slug = f"{original_slug}-{counter}"
                    counter += 1
                else:
                    break
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class news(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='news/images/%Y_%m_%d', blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    category = models.ForeignKey(newsCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def compress_image(self, image):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile
        
        img = Image.open(image)
        img.thumbnail((800, 800))
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        content_file = ContentFile(output.getvalue(), name=image.name)
        return content_file

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
            original_slug = self.slug
            counter = 1
            while news.objects.filter(slug=self.slug).exists():
                if self.pk and news.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    self.slug = f"{original_slug}-{counter}"
                    counter += 1
                else:
                    break
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ektraCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
            original_slug = self.slug
            counter = 1
            while ektraCategory.objects.filter(slug=self.slug).exists():
                if self.pk and ektraCategory.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    self.slug = f"{original_slug}-{counter}"
                    counter += 1
                else:
                    break
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ektra(models.Model):
    jam = [
        ('07.00 - 09.00', '07.00 - 09.00'),
        ('09.00 - 11.00', '09.00 - 11.00'),
        ('11.00 - 13.00', '11.00 - 13.00'),
        ('13.00 - 15.00', '13.00 - 15.00'),
        ('15.00 - 17.00', '15.00 - 17.00'),
    ]
    hari = [
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
        ('Sabtu', 'Sabtu'),
        ('Minggu', 'Minggu'),
    ]
    type_ektra = [
        ('Wajib', 'Wajib'),
        ('Pilihan', 'Pilihan'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    pembina = models.CharField(max_length=200)
    lokasi = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    jadwal = models.CharField(max_length=200, choices=jam)
    hari = models.CharField(max_length=200, choices=hari)
    type_ektra = models.CharField(max_length=200, choices=type_ektra)
    siswa_aktif = models.IntegerField(default=0)
    prestasi = models.IntegerField(default=0)
    tahun = models.IntegerField()
    image = models.ImageField(upload_to='ektra/images/%Y_%m_%d', blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    category = models.ForeignKey(ektraCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def compress_image(self, image):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile
        
        img = Image.open(image)
        img.thumbnail((800, 800))
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        content_file = ContentFile(output.getvalue(), name=image.name)
        return content_file

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
            original_slug = self.slug
            counter = 1
            while ektra.objects.filter(slug=self.slug).exists():
                if self.pk and ektra.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    self.slug = f"{original_slug}-{counter}"
                    counter += 1
                else:
                    break
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Jurusan(models.Model):
    nama = models.CharField(max_length=200)
    kode_jurusan = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    deskripsi_singkat = models.TextField(blank=True, null=True)
    deskripsi_lengkap = RichTextField(blank=True, null=True)
    gambar_utama = models.ImageField(upload_to='jurusan/images/', blank=True, null=True)
    kategori = models.CharField(max_length=100, default='Teknologi')
    durasi = models.CharField(max_length=50, default='3 Tahun')
    jumlah_siswa = models.PositiveIntegerField(default=0)
    guru_count = models.PositiveIntegerField(default=0)
    lab_count = models.PositiveIntegerField(default=0)
    serapan_kerja = models.CharField(max_length=10, default='95%')
    logo = models.ImageField(upload_to='jurusan/logos/', blank=True, null=True)
    kuota = models.PositiveIntegerField(default=40)
    
    # Kaprodi info
    kaprodi_nama = models.CharField(max_length=200, blank=True, null=True)
    kaprodi_email = models.EmailField(blank=True, null=True)
    kaprodi_foto = models.ImageField(upload_to='jurusan/kaprodi/', blank=True, null=True)
    
    kontak = models.CharField(max_length=100, blank=True, null=True)
    gedung = models.CharField(max_length=100, blank=True, null=True)
    view_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def compress_image(self, image):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile
        
        img = Image.open(image)
        img.thumbnail((800, 800))
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        content_file = ContentFile(output.getvalue(), name=image.name)
        return content_file
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
            original_slug = self.slug
            counter = 1
            while Jurusan.objects.filter(slug=self.slug).exists():
                if self.pk and Jurusan.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    self.slug = f"{original_slug}-{counter}"
                    counter += 1
                else:
                    break
        super().save(*args, **kwargs)

    @property
    def kompetensi_hard(self):
        return self.kompetensi.filter(tipe='Hard')

    @property
    def kompetensi_soft(self):
        return self.kompetensi.filter(tipe='Soft')

    def __str__(self):
        return self.nama

class Kompetensi(models.Model):
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='kompetensi')
    TYPES = [('Hard', 'Hard Skill'), ('Soft', 'Soft Skill')]
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='kompetensi')
    nama = models.CharField(max_length=200)
    tipe = models.CharField(max_length=10, choices=TYPES)

    def __str__(self):
        return f"{self.nama} ({self.jurusan.nama})"

class FasilitasJurusan(models.Model):
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='fasilitas')
    nama = models.CharField(max_length=200)
    deskripsi = models.TextField()
    icon = models.CharField(max_length=50, default='computer', help_text='Material Symbols name')

    def __str__(self):
        return f"{self.nama} ({self.jurusan.nama})"

class ProspekKarir(models.Model):
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='prospek_karir')
    posisi = models.CharField(max_length=200)
    deskripsi = models.TextField()
    rata_gaji = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.posisi} ({self.jurusan.nama})"

class Sertifikasi(models.Model):
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='sertifikasi')
    nama = models.CharField(max_length=200)
    penyelenggara = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nama} ({self.jurusan.nama})"

class MitraIndustri(models.Model):
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='mitra_industri')
    nama = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='jurusan/mitra/', blank=True, null=True)

    def __str__(self):
        return f"{self.nama} ({self.jurusan.nama})"

class TestimoniAlumni(models.Model):
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='testimoni_alumni')
    nama = models.CharField(max_length=200)
    jabatan = models.CharField(max_length=200)
    perusahaan = models.CharField(max_length=200)
    tahun_lulus = models.IntegerField()
    testimoni = models.TextField()
    image = models.ImageField(upload_to='jurusan/testimoni/%Y_%m_%d', blank=True, null=True)

    def compress_image(self, image):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile
        
        img = Image.open(image)
        img.thumbnail((800, 800))
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        content_file = ContentFile(output.getvalue(), name=image.name)
        return content_file

    def __str__(self):
        return f"{self.nama} ({self.jurusan.nama})"

class categoryPengumuman(models.Model):
    nama = models.CharField(max_length=200)

    def __str__(self):
        return self.nama


def upload_pengumuman_file(instance, filename):
    return f'pengumuman/files/{filename}'

class Pengumuman(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    deskripsi = RichTextField(blank=True, null=True)
    category = models.ForeignKey(categoryPengumuman, on_delete=models.CASCADE, related_name='pengumuman')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
            original_slug = self.slug
            counter = 1
            while Pengumuman.objects.filter(slug=self.slug).exists():
                if self.pk and Pengumuman.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    self.slug = f"{original_slug}-{counter}"
                    counter += 1
                else:
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

class FilePengumuman(models.Model):
    pengumuman = models.ForeignKey('Pengumuman', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=upload_pengumuman_file)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)
    last_downloaded = models.DateTimeField(null=True, blank=True)
    last_downloaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='downloaded_pengumuman_files'
    )
    
    def file_name(self):
        return os.path.basename(self.file.name)

    def file_type(self):
        name, ext = os.path.splitext(self.file.name)
        return ext.lower().lstrip('.')

    def file_size(self):
        size = self.file.size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    def __str__(self):
        return self.file_name()
class MataPelajaran(models.Model):
    nama = models.CharField(max_length=200)

    
    def __str__(self):
        return self.nama

class StaffDanGuru(models.Model):
    nama = models.CharField(max_length=200)
    jabatan = models.CharField(max_length=200)
    deskripsi = models.TextField()
    mata_pelajaran = models.ManyToManyField(MataPelajaran, related_name='guru_staff')
    pendidikan = models.CharField(max_length=200)
    image = models.ImageField(upload_to='staff_dan_guru/%Y_%m_%d', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def compress_image(self, image):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile
        
        img = Image.open(image)
        img.thumbnail((800, 800))
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        content_file = ContentFile(output.getvalue(), name=image.name)
        return content_file

    def __str__(self):
        return self.nama

class FasilitasLab(models.Model):
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='laboratorium')
    nama_lab = models.CharField(max_length=200, help_text='Nama Laboratorium')
    deskripsi = models.TextField(help_text='Deskripsi singkat tentang laboratorium')
    gambar = models.ImageField(upload_to='fasilitas_lab/images/%Y_%m_%d', blank=True, null=True)
    icon = models.CharField(max_length=50, default='terminal', help_text='Material Symbols icon name')
    warna_tema = models.CharField(max_length=50, default='blue', help_text='Warna tema untuk card (blue, purple, red, pink, green, dll)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def compress_image(self, image):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile
        
        img = Image.open(image)
        img.thumbnail((800, 800))
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        output.seek(0)
        content_file = ContentFile(output.getvalue(), name=image.name)
        return content_file

    def __str__(self):
        return f"{self.nama_lab} - {self.jurusan.nama}"

class PeralatanLab(models.Model):
    KATEGORI_CHOICES = [
        ('Peralatan Utama', 'Peralatan Utama'),
        ('Fitur Tambahan', 'Fitur Tambahan'),
        ('Peralatan Produksi', 'Peralatan Produksi'),
        ('Workstation', 'Workstation'),
        ('Perangkat Lunak', 'Perangkat Lunak'),
        ('Robotika & IoT', 'Robotika & IoT'),
    ]
    
    fasilitas_lab = models.ForeignKey(FasilitasLab, on_delete=models.CASCADE, related_name='peralatan')
    nama_peralatan = models.CharField(max_length=200)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, default='Peralatan Utama')
    
    def __str__(self):
        return f"{self.nama_peralatan} - {self.fasilitas_lab.nama_lab}"

class SchoolStatistics(models.Model):
    """
    Model untuk menyimpan statistik sekolah yang ditampilkan di halaman beranda
    """
    # Data Siswa
    total_siswa = models.IntegerField(default=0, help_text='Total siswa aktif')
    persentase_pertumbuhan_siswa = models.CharField(max_length=10, default='+0%', help_text='Contoh: +12%')
    progress_siswa = models.IntegerField(default=85, help_text='Progress bar (0-100)')
    
    # Data Instruktur/Guru
    total_instruktur = models.IntegerField(default=0, help_text='Total instruktur profesional')
    status_instruktur = models.CharField(max_length=50, default='Sertifikasi', help_text='Status instruktur')
    progress_instruktur = models.IntegerField(default=95, help_text='Progress bar (0-100)')
    
    # Data Mitra Industri
    @property
    def total_mitra(self):
        return MitraIndustri.objects.count()
        
    label_mitra = models.CharField(max_length=50, default='Perusahaan', help_text='Label untuk mitra')
    
    # Metadata
    is_active = models.BooleanField(default=True, help_text='Aktifkan statistik ini')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Statistik Sekolah'
        verbose_name_plural = 'Statistik Sekolah'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Statistik Sekolah - {self.updated_at.strftime('%d %B %Y')}"
    
    def save(self, *args, **kwargs):
        # Pastikan hanya ada satu statistik yang aktif
        if self.is_active:
            SchoolStatistics.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)