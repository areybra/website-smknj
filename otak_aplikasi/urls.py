from django.urls import path
from . import views

urlpatterns = [
   path('', views.beranda, name='home'),
   path('profil-sekolah/', views.profil, name='profile'),
   path('fasilitas/', views.fasilitas, name='facilities'),
   path('guru-staff/', views.guru_staff, name='teachers_staff'),
   path('berita/', views.berita, name='berita'),
   path('berita/<slug:slug>/', views.detail_berita, name='news_detail'),
   path('pengumuman/', views.pengumuman_view, name='announcements'),
   path('pengumuman/<slug:slug>/', views.detail_pengumuman, name='announcements_detail'),
   path('ektrakurikuler/', views.ektrakurikuler, name='extracurricular'),
   path('ektrakurikuler/<slug:slug>/', views.detail_ektrakurikuler, name='extracurricular_detail'),
   path('program-studi/', views.program_studi, name='program_studi'),
   path('program-studi/<slug:slug>/', views.program_studi_detail, name='program_studi_detail'),
   path('kontak/', views.kontak, name='kontak'),
   path('pengumuman/download/<int:file_id>/', views.download_pengumuman_file, name='download_pengumuman_file'),
   path('search/', views.global_search, name='global_search'),
]
