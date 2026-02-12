from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404, FileResponse
from django.core.cache import cache
from .models import *
from django.views.generic import ListView, DetailView
from django.db.models import Q, Sum, F
from django.utils import timezone



def beranda(request):
    
    # Check if data is already cached
    cache_key = 'beranda_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        jurusan_list = Jurusan.objects.all()
        pengumuman_list = Pengumuman.objects.select_related('category').all().order_by('-created_at')[:5]
        pengumuman_penting = Pengumuman.objects.filter(category__nama='Penting').first()
        guru_staff_list = StaffDanGuru.objects.prefetch_related('mata_pelajaran').all()
        # Queryset Berita (tanpa pagination)
        berita_list = news.objects.select_related('category').all().order_by('-created_at')[:3]
        
        # Ambil statistik sekolah yang aktif
        school_stats = SchoolStatistics.objects.filter(is_active=True).first()

        # Ambil data kepala sekolah secara spesifik
        kepala_sekolah = StaffDanGuru.objects.filter(jabatan__icontains='Kepala Sekolah').first()
        context = {
            'jurusan_list': jurusan_list,
            'berita_list': berita_list,
            'pengumuman_list': pengumuman_list,
            'pengumuman_penting': pengumuman_penting,
            'school_stats': school_stats,
            'guru_staff_list': guru_staff_list,
            'kepala_sekolah': kepala_sekolah,
        }
        
        # Cache the data for a shorter time or clear it
        cache.set(cache_key, context, 300) # Balanced cache time

    return render(request, 'index.html', context)



def profil(request):

    # Check if data is already cached
    cache_key = 'profil_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        struktur_organisasi = StaffDanGuru.objects.all()
        
        context = {
            'struktur_organisasi': struktur_organisasi,
        }
        
        # Cache the data for 15 minutes (900 seconds)
        cache.set(cache_key, context, 900)
    return render(request, 'profil/profil_sekolah.html', context)

def fasilitas(request):
    # Check if data is already cached
    cache_key = 'fasilitas_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        # Ambil semua data laboratorium beserta peralatannya
        peralatanlab_list = PeralatanLab.objects.all()
        laboratorium_list = FasilitasLab.objects.select_related('jurusan').prefetch_related('peralatan').all()
        
        context = {
            'laboratorium_list': laboratorium_list,
            'peralatanlab_list': peralatanlab_list,
        }
        
        # Cache the data for 15 minutes (900 seconds)
        cache.set(cache_key, context, 900)
    return render(request, 'profil/fasilitas.html', context)

def guru_staff(request):
    leader_titles = ['Kepala Sekolah', 'Waka bidang Sarana dan Prasarana', 'Waka bidang Kurikulum', 'Waka bidang Hubungan Masyarakat', 'Waka bidang Kesiswaan']
    
    # Check if data is already cached
    cache_key = 'guru_staff_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        # Ambil semua data staff untuk bagian pimpinan (filter di template)
        all_staff = StaffDanGuru.objects.filter(jabatan__in=leader_titles).prefetch_related('mata_pelajaran').order_by('created_at')
        
        # Filter untuk paginasi (hanya guru reguler, exclude pimpinan)
        regular_staff = StaffDanGuru.objects.exclude(jabatan__in=leader_titles).prefetch_related('mata_pelajaran').order_by('created_at')
        
        # Pagination (6 guru per halaman)
        paginator = Paginator(regular_staff, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        

        context = {
            'leaders_list': all_staff, # Untuk section Kepala Sekolah & Waka
            'guru_staff_list': page_obj, # Untuk section Daftar Guru (paginated)
        }
        
        # Cache the data for 15 minutes (900 seconds)
        cache.set(cache_key, context, 900)
    return render(request, 'profil/guru-staff.html', context)

def berita(request):
    # Ambil parameter query
    search_query = request.GET.get('search', '')
    kategori_filter = request.GET.get('kategori', '')
    page_number = request.GET.get('page', '1')

    # Buat cache key yang dinamis berdasarkan parameter agar pencarian tidak salah cache
    cache_key = f'berita_v2_{search_query}_{kategori_filter}_{page_number}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        # Mengambil semua berita dari database, diurutkan dari yang terbaru
        berita_list = news.objects.select_related('category').all().order_by('-created_at')
        
        # Mengambil berita utama (berita terbaru) - Simpan sebelum difilter untuk hero section
        berita_utama = berita_list.first() if berita_list.exists() else None
        
        # Mengambil kategori untuk filter
        kategori_list = newsCategory.objects.all()
        
        # Filter berdasarkan kategori jika ada parameter
        if kategori_filter:
            berita_list = berita_list.filter(category__slug=kategori_filter)
        
        # Pencarian: Judul, Konten, dan Nama Kategori
        if search_query:
            berita_list = berita_list.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query) |
                Q(category__name__icontains=search_query)
            ).distinct()
        
        # Pagination (6 berita per halaman)
        paginator = Paginator(berita_list, 6)
        page_number = request.GET.get('page', '1')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'berita_list': page_obj,
            'berita_utama': berita_utama,
            'kategori_list': kategori_list,
        }
        
        # Cache the data for shorter time for dynamic results
        cache.set(cache_key, context, 300)
    return render(request, 'berita/berita.html', context)

def detail_berita(request, slug):
    # Mengambil berita berdasarkan slug
    berita_detail = get_object_or_404(news, slug=slug)
    
    # Increment view count efficiently without modifying updated_at
    news.objects.filter(slug=slug).update(view_count=F('view_count') + 1)
    
    # Mengambil berita terkait (dari kategori yang sama)
    berita_terkait = news.objects.filter(category=berita_detail.category).exclude(slug=slug).order_by('-created_at')[:3]
    
    # Mengambil berita terbaru
    berita_terbaru = news.objects.exclude(slug=slug).order_by('-created_at')[:5]
    
    # Mengambil berita trending (berdasarkan view_count)
    berita_trending = news.objects.exclude(slug=slug).order_by('-view_count')[:5]
    
    # Mengambil berita sebelumnya dan selanjutnya
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
    # Ambil parameter query
    search_query = request.GET.get('search', '')
    category_name = request.GET.get('category', '')
    page_number = request.GET.get('page', '1')

    # Buat cache key yang unik berdasarkan parameter (search, category, page)
    # Gunakan string sederhana untuk key
    cache_key = f'pengumuman_v2_{search_query}_{category_name}_{page_number}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        pengumuman_list = Pengumuman.objects.select_related('category').all().order_by('-created_at')
        # Gunakan iexact agar tidak case-sensitive
        pengumuman_penting = Pengumuman.objects.select_related('category').filter(category__nama__iexact='Penting').order_by('-created_at')
        
        # Pencarian
        if search_query:
            pengumuman_list = pengumuman_list.filter(
                Q(judul__icontains=search_query) | 
                Q(deskripsi__icontains=search_query) |
                Q(category__nama__icontains=search_query)
            )
        
        # Fetch all categories for the filter buttons
        pengumuman_category = categoryPengumuman.objects.all().order_by('nama')
        
        # Filter by category if present
        selected_category = None
        if category_name:
            selected_category = categoryPengumuman.objects.filter(nama__iexact=category_name).first()
            if selected_category:
                pengumuman_list = pengumuman_list.filter(category=selected_category)
            else:
                # Jika ada parameter category tapi tidak valid, return empty list atau abaikan filter?
                # Di sini kita filter dengan nama asli yang diberikan jika tidak found di selected_category
                pengumuman_list = pengumuman_list.filter(category__nama__iexact=category_name)
        
        # For files section - filter based on filtered announcements
        pengumuman_file = pengumuman_list.filter(files__isnull=False).distinct().order_by('-created_at')

        # ===== HITUNG STATISTIK DOWNLOAD =====
        total_files = FilePengumuman.objects.filter(pengumuman__in=pengumuman_list).count()
        total_downloads = FilePengumuman.objects.filter(
            pengumuman__in=pengumuman_list
        ).aggregate(total=Sum('download_count'))['total'] or 0
        
        most_downloaded_file = FilePengumuman.objects.filter(
            pengumuman__in=pengumuman_list
        ).order_by('-download_count').first()

        # Increase pagination size from 2 to 6 for better UX
        paginator = Paginator(pengumuman_list, 6)
        page_obj = paginator.get_page(page_number)

        context = {
            'pengumuman_list': page_obj,
            'search_query': search_query,
            'pengumuman_penting': pengumuman_penting,
            'pengumuman_category': pengumuman_category,
            'pengumuman_file': pengumuman_file,
            'selected_category': selected_category,
            'total_files': total_files,
            'total_downloads': total_downloads,
            'most_downloaded_file': most_downloaded_file,
        }
        
        # Cache the data for a shorter time (e.g., 5 minutes instead of 15)
        cache.set(cache_key, context, 300)
    return render(request, 'pengumuman/pengumuman.html', context)

def detail_pengumuman(request, slug):
    # Mengambil pengumuman berdasarkan slug
    pengumuman_detail = get_object_or_404(Pengumuman, slug=slug)
    
    # Increment view count
    Pengumuman.objects.filter(slug=slug).update(view_count=F('view_count') + 1)
    
    # Mengambil pengumuman terkait (dari kategori yang sama)
    pengumuman_terkait = Pengumuman.objects.filter(category=pengumuman_detail.category).exclude(slug=slug).order_by('-created_at')[:3]
    
    # Mengambil pengumuman sebelumnya dan selanjutnya
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
    # Check if data is already cached
    cache_key = 'ektrakurikuler_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        context = cached_data
    else:
        ektra_list = ektra.objects.select_related('category').all().order_by('-created_at')
        
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
        
        # Cache the data for 15 minutes (900 seconds)
        cache.set(cache_key, context, 900)
    return render(request, 'program/ektrakurikuler/ektrakurikuler.html', context)

def detail_ektrakurikuler(request, slug):
    # Mengambil ektra berdasarkan slug
    ektra_detail = get_object_or_404(ektra, slug=slug)
    
    # Mengambil data tambahan
    
    # Increment view count
    ektra.objects.filter(slug=slug).update(view_count=F('view_count') + 1)
    
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
    # Check if data is already cached
    cache_key = 'program_studi_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        jurusan_utama, jurusan_list, mitra_industri_list = cached_data
    else:
        # Mengambil semua jurusan dari database, diurutkan dari yang terbaru
        jurusan_utama = Jurusan.objects.all()[:4]
        jurusan_list = Jurusan.objects.all()
        mitra_industri_list = MitraIndustri.objects.all()
        
        # Cache the data for 15 minutes (900 seconds)
        cache.set(cache_key, (jurusan_utama, jurusan_list, mitra_industri_list), 900)
    
    return render(request, 'program/jurusan/jurusan.html', {
        'jurusan_list': jurusan_list, 
        'jurusan_utama': jurusan_utama,
        'mitra_industri_list': mitra_industri_list
    })

def program_studi_detail(request, slug):
    # Mengambil jurusan berdasarkan slug
    jurusan_detail = get_object_or_404(Jurusan, slug=slug)

    return render(request, 'program/jurusan/detail_jurusan.html', {'jurusan': jurusan_detail})

def kontak(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        telepon = request.POST.get('telepon')
        subjek = request.POST.get('subjek')
        pesan_user = request.POST.get('pesan')
        
        # Validasi sederhana
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
            # Mengirim email
            # Sender address default to settings.EMAIL_HOST_USER or a dummy one if not set
            from_email = getattr(settings, 'EMAIL_HOST_USER', 'noreply@smknuruljadid.sch.id')
            recruit_email = 'smknurja.paiton@gmail.com'
            
            # Menggunakan EmailMessage agar bisa mengatur Reply-To
            # Note: Gmail dan provider email modern biasanya memaksa 'From' email sama dengan
            # akun yang digunakan untuk login (EMAIL_HOST_USER) untuk mencegah spam/spoofing.
            # Oleh karena itu, kita set 'Reply-To' ke email pengirim (input user)
            # agar ketika admin klik Reply, langsung tertuju ke user.
            
            email_msg = EmailMessage(
                subject=subject_email,
                body=message_body,
                from_email=from_email,
                to=[recruit_email],
                reply_to=[email],  # Ini akan membuat tombol Reply mengarah ke email user
            )
            email_msg.send(fail_silently=False)
            messages.success(request, 'Pesan Anda berhasil dikirim! Terima kasih telah menghubungi kami.')
        except Exception as e:
            messages.error(request, f'Maaf, terjadi kesalahan saat mengirim pesan. Silakan coba lagi nanti. ({str(e)})')
            
    return render(request, 'kontak/kontak.html')

def global_search(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Search in news (Berita)
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
            
        # Search in Pengumuman
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

        # Search in Jurusan
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

        # Search in ektra (Ekstrakurikuler)
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
            
        # Sort results by date descending if possible, or just keep order
        # results.sort(key=lambda x: x['date'], reverse=True)

    context = {
        'query': query,
        'results': results,
        'total_results': len(results)
    }
    
    return render(request, 'search_results.html', context)
