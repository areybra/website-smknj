from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import (
    news, newsCategory, Pengumuman, categoryPengumuman, 
    Jurusan, StaffDanGuru, ektra, ektraCategory, FasilitasLab, 
    SchoolStatistics, MitraIndustri, FilePengumuman,
    MataPelajaran, TestimoniAlumni, Kompetensi, FasilitasJurusan,
    ProspekKarir, Sertifikasi, PeralatanLab
)

def clear_all_cache():
    """Membersihkan seluruh cache aplikasi"""
    cache.clear()

@receiver([post_save, post_delete], sender=news)
@receiver([post_save, post_delete], sender=newsCategory)
@receiver([post_save, post_delete], sender=Pengumuman)
@receiver([post_save, post_delete], sender=categoryPengumuman)
@receiver([post_save, post_delete], sender=Jurusan)
@receiver([post_save, post_delete], sender=StaffDanGuru)
@receiver([post_save, post_delete], sender=ektra)
@receiver([post_save, post_delete], sender=ektraCategory)
@receiver([post_save, post_delete], sender=FasilitasLab)
@receiver([post_save, post_delete], sender=SchoolStatistics)
@receiver([post_save, post_delete], sender=MitraIndustri)
@receiver([post_save, post_delete], sender=FilePengumuman)
@receiver([post_save, post_delete], sender=MataPelajaran)
@receiver([post_save, post_delete], sender=TestimoniAlumni)
@receiver([post_save, post_delete], sender=Kompetensi)
@receiver([post_save, post_delete], sender=FasilitasJurusan)
@receiver([post_save, post_delete], sender=ProspekKarir)
@receiver([post_save, post_delete], sender=Sertifikasi)
@receiver([post_save, post_delete], sender=PeralatanLab)
def invalidate_cache(sender, **kwargs):
    """Signal handler untuk menghapus cache saat data berubah"""
    clear_all_cache()
