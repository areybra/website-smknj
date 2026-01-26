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