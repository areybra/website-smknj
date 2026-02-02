from django.contrib import admin
from .models import *

admin.site.register(newsCategory)
admin.site.register(news)
admin.site.register(ektraCategory)
admin.site.register(ektra)


class KompetensiInline(admin.TabularInline):
    model = Kompetensi
    extra = 1

class MitraIndustriInline(admin.TabularInline):
    model = MitraIndustri
    extra = 1

class prospekKarirInline(admin.TabularInline):
    model = ProspekKarir
    extra = 1
class fasilitasJurusanInline(admin.TabularInline):
    model = FasilitasJurusan
    extra = 1        
class testimoniAlumniInline(admin.TabularInline):
    model = TestimoniAlumni
    extra = 1        
class sertifikasiInline(admin.TabularInline):
    model = Sertifikasi
    extra = 1               

class jurusanAdmin(admin.ModelAdmin):
    inlines = [prospekKarirInline, fasilitasJurusanInline, testimoniAlumniInline, sertifikasiInline, KompetensiInline, MitraIndustriInline]     
admin.site.register(Jurusan, jurusanAdmin)

class FilePengumumanInline(admin.TabularInline):
    model = FilePengumuman
    extra = 1

class pengumumanAdmin(admin.ModelAdmin):
    inlines = [FilePengumumanInline]    
    list_display = ('judul', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('judul', 'deskripsi')
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(category__nama='PPDB')
        return queryset

admin.site.register(categoryPengumuman)
admin.site.register(Pengumuman, pengumumanAdmin)

class staffDanGuruAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jabatan', 'pendidikan', 'created_at', 'updated_at')
    list_filter = ('pendidikan', 'jabatan', 'created_at', 'updated_at')
    search_fields = ('nama', 'pendidikan')
    ordering = ('-created_at',)
    filter_horizontal = ('mata_pelajaran',)

admin.site.register(StaffDanGuru, staffDanGuruAdmin)
admin.site.register(MataPelajaran)

class PeralatanLabInline(admin.TabularInline):
    model = PeralatanLab
    extra = 1

class FasilitasLabAdmin(admin.ModelAdmin):
    inlines = [PeralatanLabInline]
    list_display = ('nama_lab', 'jurusan', 'warna_tema', 'created_at', 'updated_at')
    list_filter = ('jurusan', 'warna_tema', 'created_at')
    search_fields = ('nama_lab', 'deskripsi', 'jurusan__nama')
    ordering = ('-created_at',)

admin.site.register(FasilitasLab, FasilitasLabAdmin)

class SchoolStatisticsAdmin(admin.ModelAdmin):
    list_display = ('total_siswa', 'total_instruktur', 'total_mitra', 'is_active', 'updated_at')
    list_filter = ('is_active', 'updated_at')
    readonly_fields = ('total_mitra',)
    fieldsets = (
        ('Data Siswa', {
            'fields': ('total_siswa', 'persentase_pertumbuhan_siswa', 'progress_siswa')
        }),
        ('Data Instruktur', {
            'fields': ('total_instruktur', 'status_instruktur', 'progress_instruktur')
        }),
        ('Data Mitra Industri', {
            'fields': ('total_mitra', 'label_mitra'),
            'description': 'Jumlah mitra dihitung otomatis dari data Mitra Industri.'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

admin.site.register(SchoolStatistics, SchoolStatisticsAdmin)

