from django.contrib import admin
from .models import *

admin.site.register(newsCategory)
admin.site.register(news)
admin.site.register(ektraCategory)
admin.site.register(ektra)


class KompetensiInline(admin.TabularInline):
    model = Kompetensi
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
    inlines = [prospekKarirInline, fasilitasJurusanInline, testimoniAlumniInline, sertifikasiInline, KompetensiInline]     
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

