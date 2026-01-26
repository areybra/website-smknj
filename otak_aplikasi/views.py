from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
from .models import *
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import render


def beranda(request):
    # Queryset Jurusan (yang dipagination)
    jurusan_qs = Jurusan.objects.all().order_by('id')

    paginator = Paginator(jurusan_qs, 3)  # 3 jurusan per halaman
    page_number = request.GET.get('page')
    jurusan_page = paginator.get_page(page_number)

    # Queryset Berita (tanpa pagination)
    berita_list = news.objects.all().order_by('-created_at')[:3]

    context = {
        'jurusan_list': jurusan_page,
        'berita_list': berita_list,
    }

    return render(request, 'index.html', context)


def profil(request):
    return render(request, 'profil/profil_sekolah.html')

def fasilitas(request):
    return render(request, 'profil/fasilitas.html')

def guru_staff(request):
    return render(request, 'profil/guru-staff.html')

def berita(request):
    # Mengambil semua berita dari database, diurutkan dari yang terbaru
    berita_list = news.objects.all().order_by('-created_at')
    
    # Mengambil berita utama (berita terbaru)
    berita_utama = berita_list.first() if berita_list.exists() else None
    
    # Mengambil kategori untuk filter
    kategori_list = newsCategory.objects.all()
    
    # Filter berdasarkan kategori jika ada parameter
    kategori_filter = request.GET.get('kategori')
    if kategori_filter:
        berita_list = berita_list.filter(category__slug=kategori_filter)
    
    # Pencarian
    search_query = request.GET.get('search')
    if search_query:
        berita_list = berita_list.filter(title__icontains=search_query)
    
    # Pagination (6 berita per halaman)
    paginator = Paginator(berita_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'berita_list': page_obj,
        'berita_utama': berita_utama,
        'kategori_list': kategori_list,
    }
    return render(request, 'berita/berita.html', context)

def detail_berita(request, slug):
    # Mengambil berita berdasarkan slug
    berita_detail = get_object_or_404(news, slug=slug)
    
    # Increment view count
    berita_detail.view_count += 1
    berita_detail.save()
    
    # Mengambil berita terkait (dari kategori yang sama)
    berita_terkait = news.objects.filter(category=berita_detail.category).exclude(slug=slug).order_by('-created_at')[:3]
    
    # Mengambil berita sebelumnya dan selanjutnya
    berita_sebelumnya = news.objects.filter(created_at__lt=berita_detail.created_at).order_by('-created_at').first()
    berita_selanjutnya = news.objects.filter(created_at__gt=berita_detail.created_at).order_by('created_at').first()
    
    context = {
        'berita': berita_detail,
        'berita_terkait': berita_terkait,
        'berita_sebelumnya': berita_sebelumnya,
        'berita_selanjutnya': berita_selanjutnya,
    }
    return render(request, 'berita/detail_berita.html', context)

def pengumuman(request):
    return render(request, 'pengumuman/pengumuman.html')

def ektrakurikuler(request):
    ektra_list = ektra.objects.all().order_by('-created_at')
    
    # Mengambil ektra utama (ektra terbaru)
    ektra_utama = ektra_list.first() if ektra_list.exists() else None
    
    # Mengambil kategori untuk filter
    kategori_list = ektraCategory.objects.all()
    
    # Filter berdasarkan kategori jika ada parameter
    kategori_filter = request.GET.get('kategori')
    if kategori_filter:
        ektra_list = ektra_list.filter(category__slug=kategori_filter)
    
    # Pencarian
    search_query = request.GET.get('search')
    if search_query:
        ektra_list = ektra_list.filter(title__icontains=search_query)
    
    context = {
        'ektra_list': ektra_list,
        'ektra_utama': ektra_utama,
        'kategori_list': kategori_list,
        'count_ektra': ektra.objects.all().count(),
    }
    return render(request, 'program/ektrakurikuler/ektrakurikuler.html', context)

def detail_ektrakurikuler(request, slug):
    # Mengambil ektra berdasarkan slug
    ektra_detail = get_object_or_404(ektra, slug=slug)
    
    # Mengambil data tambahan
    
    # Increment view count
    ektra_detail.view_count += 1
    ektra_detail.save()
    
    # Mengambil ektra terkait (dari kategori yang sama)
    ektra_terkait = ektra.objects.filter(category=ektra_detail.category).exclude(slug=slug).order_by('-created_at')[:3]
    
    # Mengambil ektra sebelumnya dan selanjutnya
    ektra_sebelumnya = ektra.objects.filter(created_at__lt=ektra_detail.created_at).order_by('-created_at').first()
    ektra_selanjutnya = ektra.objects.filter(created_at__gt=ektra_detail.created_at).order_by('created_at').first()
    
    context = {
        'ektra': ektra_detail,
        'ektra_terkait': ektra_terkait,
        'ektra_sebelumnya': ektra_sebelumnya,
        'ektra_selanjutnya': ektra_selanjutnya,
    }
    return render(request, 'program/ektrakurikuler/detail_ektrakurikuler.html', context)

def program_studi(request):
    # Mengambil semua jurusan dari database, diurutkan dari yang terbaru
    jurusan_utama = Jurusan.objects.all()[:4]
    jurusan_list = Jurusan.objects.all()
    return render(request, 'program/jurusan/jurusan.html', {'jurusan_list': jurusan_list, 'jurusan_utama': jurusan_utama})

def program_studi_detail(request, slug):
    # Mengambil jurusan berdasarkan slug
    jurusan_detail = get_object_or_404(Jurusan, slug=slug)
    jurusan_detail = Jurusan.objects.get(slug=slug)
    return render(request, 'program/jurusan/detail_jurusan.html', {'jurusan': jurusan_detail})

def kontak(request):
    return render(request, 'kontak/kontak.html')