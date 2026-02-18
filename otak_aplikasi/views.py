from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404, FileResponse
from django.core.cache import cache
from django.views.generic import ListView, DetailView
from django.db.models import Q, Sum, F, Count
from django.db import models
from django.utils import timezone

from .models import (
    Jurusan, Pengumuman, StaffDanGuru, news, SchoolStatistics,
    FilePengumuman, newsCategory, ektra, ektraCategory, MitraIndustri,
    categoryPengumuman, FasilitasLab, PeralatanLab
)



def beranda(request):
    """View untuk halaman beranda dengan caching"""
    cache_key = 'beranda_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        pengumuman_list = Pengumuman.objects.select_related('category').all().order_by('-created_at')[:5]
        pengumuman_penting = Pengumuman.objects.filter(penting=True).first()
        jurusan_list = Jurusan.objects.all()
        berita_list = news.objects.select_related('category').all().order_by('-created_at')[:3]
        school_stats = SchoolStatistics.objects.filter(is_active=True).first()
        kepala_sekolah = StaffDanGuru.objects.filter(jabatan__icontains='Kepala Sekolah').first()
        
        context = {
            'jurusan_list': jurusan_list,
            'berita_list': berita_list,
            'pengumuman_list': pengumuman_list,
            'pengumuman_penting': pengumuman_penting,
            'school_stats': school_stats,
            'kepala_sekolah': kepala_sekolah,
        }
        
        # Cache selama 1 jam, akan di-reset otomatis via signals jika ada perubahan data
        cache.set(cache_key, context, 3600)

    return render(request, 'index.html', context)



def profil(request):
    """View untuk halaman profil sekolah"""
    cache_key = 'profil_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        struktur_organisasi = StaffDanGuru.objects.all()
        context = {'struktur_organisasi': struktur_organisasi}
        cache.set(cache_key, context, 3600)
    return render(request, 'profil/profil_sekolah.html', context)


def fasilitas(request):
    """View untuk halaman fasilitas laboratorium"""
    cache_key = 'fasilitas_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        laboratorium_list = FasilitasLab.objects.select_related('jurusan').prefetch_related('peralatan').all()
        context = {'laboratorium_list': laboratorium_list}
        cache.set(cache_key, context, 3600)
    return render(request, 'profil/fasilitas.html', context)

def guru_staff(request):
    leader_titles = settings.LEADER_TITLES if hasattr(settings, 'LEADER_TITLES') else [
        'Kepala Sekolah', 'Waka bidang Sarana dan Prasarana', 'Waka bidang Kurikulum', 
        'Waka bidang Hubungan Masyarakat', 'Waka bidang Kesiswaan'
    ]
    
    page_number = request.GET.get('page', '1')
    cache_key = f'guru_staff_data_page_{page_number}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        all_staff = StaffDanGuru.objects.filter(jabatan__in=leader_titles).prefetch_related('mata_pelajaran').order_by('created_at')
        regular_staff = StaffDanGuru.objects.exclude(jabatan__in=leader_titles).prefetch_related('mata_pelajaran').order_by('created_at')
        
        paginator = Paginator(regular_staff, 6)
        page_obj = paginator.get_page(page_number)
        
        context = {
            'leaders_list': all_staff,
            'guru_staff_list': page_obj,
        }
        
        cache.set(cache_key, context, 3600)
    return render(request, 'profil/guru-staff.html', context)

def berita(request):
    """View untuk halaman daftar berita dengan filter dan pencarian"""
    search_query = request.GET.get('search', '')
    kategori_filter = request.GET.get('kategori', '')
    page_number = request.GET.get('page', '1')

    cache_key = f'berita_{search_query}_{kategori_filter}_{page_number}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        berita_list = news.objects.select_related('category').all().order_by('-created_at')
        berita_utama = berita_list.first() if berita_list.exists() else None
        kategori_list = newsCategory.objects.all()
        
        if kategori_filter:
            berita_list = berita_list.filter(category__slug=kategori_filter)
        
        if search_query:
            berita_list = berita_list.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query) |
                Q(category__name__icontains=search_query)
            ).distinct()
        
        # Client-side pagination request: pass all data
        # paginator = Paginator(berita_list, 6)
        # page_obj = paginator.get_page(page_number)
        
        context = {
            'berita_list': berita_list,
            'berita_utama': berita_utama,
            'kategori_list': kategori_list,
        }
        
        cache.set(cache_key, context, 3600)
    return render(request, 'berita/berita.html', context)

def detail_berita(request, slug):
    """View untuk detail berita dengan increment view count"""
    berita_detail = get_object_or_404(news, slug=slug)
    
    news.objects.filter(slug=slug).update(view_count=F('view_count') + 1)
    
    berita_terkait = news.objects.filter(category=berita_detail.category).exclude(slug=slug).order_by('-created_at')[:3]
    berita_terbaru = news.objects.exclude(slug=slug).order_by('-created_at')[:3]
    berita_trending = news.objects.exclude(slug=slug).order_by('-view_count')[:5]
    berita_sebelumnya = news.objects.filter(created_at__lt=berita_detail.created_at).order_by('-created_at').first()
    berita_selanjutnya = news.objects.filter(created_at__gt=berita_detail.created_at).order_by('created_at').first()
    
    context = {
        'berita': berita_detail,
        'berita_terkait': berita_terkait,
        'berita_terbaru': berita_terbaru,
        'berita_trending': berita_trending,
        'berita_sebelumnya': berita_sebelumnya,
        'berita_selanjutnya': berita_selanjutnya,
    }
    return render(request, 'berita/detail_berita.html', context)


def download_pengumuman_file(request, file_id):
    file_obj = get_object_or_404(FilePengumuman, id=file_id)
    
    try:
        # Buka file untuk di-download
        response = FileResponse(file_obj.file.open('rb'))
        
        # Update counter download
        file_obj.download_count += 1
        file_obj.last_downloaded = timezone.now()
        if request.user.is_authenticated:
            file_obj.last_downloaded_by = request.user
        file_obj.save()
        
        # Set header untuk download
        response['Content-Disposition'] = f'attachment; filename="{file_obj.file_name()}"'
        
        return response
        
    except Exception as e:
        raise Http404(f"Error saat download file: {str(e)}")

def pengumuman_view(request):
    """View untuk halaman pengumuman dengan filter, pencarian, dan statistik download"""
    search_query = request.GET.get('search', '')
    category_name = request.GET.get('category', '')
    page_number = request.GET.get('page', '1')

    cache_key = f'pengumuman_{search_query}_{category_name}_{page_number}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        pengumuman_list = Pengumuman.objects.select_related('category').all().order_by('-created_at')
        pengumuman_penting = Pengumuman.objects.filter(penting=True).order_by('-created_at')
        
        if search_query:
            pengumuman_list = pengumuman_list.filter(
                Q(judul__icontains=search_query) | 
                Q(deskripsi__icontains=search_query) |
                Q(category__nama__icontains=search_query)
            )
        
        pengumuman_category = categoryPengumuman.objects.all().order_by('nama')
        
        if category_name:
            pengumuman_list = pengumuman_list.filter(category__nama__iexact=category_name)
        
        pengumuman_file = pengumuman_list.filter(files__isnull=False).distinct().order_by('-created_at')

        file_stats = FilePengumuman.objects.filter(pengumuman__in=pengumuman_list).aggregate(
            total_files=models.Count('id'),
            total_downloads=Sum('download_count')
        )
        
        most_downloaded_file = FilePengumuman.objects.filter(
            pengumuman__in=pengumuman_list
        ).order_by('-download_count').first()

        paginator = Paginator(pengumuman_list, 6)
        page_obj = paginator.get_page(page_number)

        context = {
            'pengumuman_list': page_obj,
            'search_query': search_query,
            'pengumuman_penting': pengumuman_penting,
            'pengumuman_category': pengumuman_category,
            'pengumuman_file': pengumuman_file,
            'total_files': file_stats['total_files'] or 0,
            'total_downloads': file_stats['total_downloads'] or 0,
            'most_downloaded_file': most_downloaded_file,
        }
        
        cache.set(cache_key, context, 3600)
    return render(request, 'pengumuman/pengumuman.html', context)

def detail_pengumuman(request, slug):
    """View untuk detail pengumuman dengan increment view count"""
    pengumuman_detail = get_object_or_404(Pengumuman, slug=slug)
    
    Pengumuman.objects.filter(slug=slug).update(view_count=F('view_count') + 1)
    
    pengumuman_terkait = Pengumuman.objects.filter(category=pengumuman_detail.category).exclude(slug=slug).order_by('-created_at')[:3]
    pengumuman_sebelumnya = Pengumuman.objects.filter(created_at__lt=pengumuman_detail.created_at).order_by('-created_at').first()
    pengumuman_selanjutnya = Pengumuman.objects.filter(created_at__gt=pengumuman_detail.created_at).order_by('created_at').first()
    
    context = {
        'pengumuman': pengumuman_detail,
        'pengumuman_terkait': pengumuman_terkait,
        'pengumuman_sebelumnya': pengumuman_sebelumnya,
        'pengumuman_selanjutnya': pengumuman_selanjutnya,
    }
    return render(request, 'pengumuman/detail_pengumuman.html', context)


def ektrakurikuler(request):
    """View untuk halaman ekstrakurikuler dengan filter dan pencarian"""
    cache_key = 'ektrakurikuler_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        ektra_list = ektra.objects.select_related('category').all().order_by('-created_at')
        ektra_utama = ektra_list.first() if ektra_list.exists() else None
        kategori_list = ektraCategory.objects.all()
        
        kategori_filter = request.GET.get('kategori')
        if kategori_filter:
            ektra_list = ektra_list.filter(category__slug=kategori_filter)
        
        search_query = request.GET.get('search')
        if search_query:
            ektra_list = ektra_list.filter(title__icontains=search_query)
        
        context = {
            'ektra_list': ektra_list,
            'ektra_utama': ektra_utama,
            'kategori_list': kategori_list,
            'count_ektra': ektra.objects.count(),
        }
        
        cache.set(cache_key, context, 3600)
    return render(request, 'program/ektrakurikuler/ektrakurikuler.html', context)

def detail_ektrakurikuler(request, slug):
    """View untuk detail ekstrakurikuler dengan increment view count"""
    ektra_detail = get_object_or_404(ektra, slug=slug)
    
    ektra.objects.filter(slug=slug).update(view_count=F('view_count') + 1)
    
    ektra_terkait = ektra.objects.filter(category=ektra_detail.category).exclude(slug=slug).order_by('-created_at')[:3]
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
    """View untuk halaman program studi/jurusan"""
    cache_key = 'program_studi_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        jurusan_list = Jurusan.objects.prefetch_related('testimoni_alumni', 'kompetensi', 'prospek_karir', 'mitra_industri').all()
        jurusan_utama = Jurusan.objects.all()[:4]
        mitra_industri_list = MitraIndustri.objects.all()
        
        context = {
            'jurusan_list': jurusan_list, 
            'jurusan_utama': jurusan_utama,
            'mitra_industri_list': mitra_industri_list
        }
        cache.set(cache_key, context, 3600)
    
    return render(request, 'program/jurusan/jurusan.html', context)


def program_studi_detail(request, slug):
    """View untuk detail program studi/jurusan"""
    jurusan_detail = get_object_or_404(Jurusan.objects.prefetch_related('testimoni_alumni', 'kompetensi', 'fasilitas', 'prospek_karir', 'sertifikasi', 'mitra_industri'), slug=slug)
    jurusan_lainnya = Jurusan.objects.exclude(id=jurusan_detail.id)[:3]
    context = {
        'jurusan': jurusan_detail,
        'jurusan_lainnya': jurusan_lainnya
    }
    return render(request, 'program/jurusan/detail_jurusan.html', context)

def kontak(request):
    """View untuk halaman kontak dengan form email"""
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        telepon = request.POST.get('telepon')
        subjek = request.POST.get('subjek')
        pesan_user = request.POST.get('pesan')
        
        if not nama or not email or not pesan_user:
            messages.error(request, 'Mohon lengkapi data yang wajib diisi.')
            return render(request, 'kontak/kontak.html')

        subject_email = f"[Website Contact] {subjek} - {nama}"
        message_body = f"""
Anda menerima pesan baru dari formulir kontak website.

Detail Pengirim:
Nama    : {nama}
Email   : {email}
Telepon : {telepon}
Subjek  : {subjek}

Pesan:
{pesan_user}
-------------------------------------------------------
"""
        
        try:
            from_email = getattr(settings, 'EMAIL_HOST_USER', 'noreply@smknuruljadid.sch.id')
            recruit_email = getattr(settings, 'RECIPIENT_ADDRESS', 'smknurja.paiton@gmail.com')
            
            email_msg = EmailMessage(
                subject=subject_email,
                body=message_body,
                from_email=from_email,
                to=[recruit_email],
                reply_to=[email],
            )
            email_msg.send(fail_silently=False)
            messages.success(request, 'Pesan Anda berhasil dikirim! Terima kasih telah menghubungi kami.')
        except Exception as e:
            messages.error(request, f'Maaf, terjadi kesalahan saat mengirim pesan. Silakan coba lagi nanti.')
            
    return render(request, 'kontak/kontak.html')

def global_search(request):
    """View untuk pencarian global di seluruh konten website"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        news_results = news.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
        for item in news_results:
            results.append({
                'title': item.title,
                'url': f'/berita/{item.slug}/',
                'category': 'Berita',
                'description': item.content[:200] if item.content else '',
                'date': item.created_at,
                'image': item.image.url if item.image else None
            })
            
        announcement_results = Pengumuman.objects.filter(
            Q(judul__icontains=query) | Q(deskripsi__icontains=query)
        ).distinct()
        for item in announcement_results:
            results.append({
                'title': item.judul,
                'url': f'/pengumuman/{item.slug}/',
                'category': 'Pengumuman',
                'description': item.deskripsi[:200] if item.deskripsi else '',
                'date': item.created_at,
                'image': None
            })

        jurusan_results = Jurusan.objects.filter(
            Q(nama__icontains=query) | Q(deskripsi_singkat__icontains=query) | Q(deskripsi_lengkap__icontains=query)
        ).distinct()
        for item in jurusan_results:
            results.append({
                'title': item.nama,
                'url': f'/program-studi/{item.slug}/',
                'category': 'Jurusan',
                'description': item.deskripsi_singkat or '',
                'date': item.created_at,
                'image': item.gambar_utama.url if item.gambar_utama else None
            })

        ektra_results = ektra.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
        for item in ektra_results:
            results.append({
                'title': item.title,
                'url': f'/ektrakurikuler/{item.slug}/',
                'category': 'Ekstrakurikuler',
                'description': item.content[:200] if item.content else '',
                'date': item.created_at,
                'image': item.image.url if item.image else None
            })

    context = {
        'query': query,
        'results': results,
        'total_results': len(results)
    }
    
    return render(request, 'search_results.html', context)
