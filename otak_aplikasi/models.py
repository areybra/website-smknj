from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
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
    video = models.FileField(upload_to='news/videos/%Y_%m_%d', blank=True, null=True)
    view_count = models.IntegerField(default=0)
    category = models.ForeignKey(newsCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    pretasi = models.IntegerField(default=0)
    tahun = models.IntegerField()
    image = models.ImageField(upload_to='ektra/images/%Y_%m_%d', blank=True, null=True)
    video = models.FileField(upload_to='ektra/videos/%Y_%m_%d', blank=True, null=True)
    view_count = models.IntegerField(default=0)
    category = models.ForeignKey(ektraCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    foto = models.ImageField(upload_to='jurusan/testimoni/', blank=True, null=True)

    def __str__(self):
        return f"{self.nama} ({self.jurusan.nama})"
