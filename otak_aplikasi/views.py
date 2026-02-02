from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404, FileResponse
from .models import *
from django.views.generic import ListView, DetailView
from django.db.models import Q, Sum
from django.shortcuts import render
from django.utils import timezone



def beranda(request):
    
    guru_staff_list = StaffDanGuru.objects.all()
    pengumuman_penting = Pengumuman.objects.filter(category__nama='Penting').order_by('-created_at')[:2]
    pengumuman_list = Pengumuman.objects.all().order_by('-created_at')[:3]
    # Queryset Jurusan (yang dipagination)
    jurusan_qs = Jurusan.objects.all().order_by('id')

    paginator = Paginator(jurusan_qs, 3)  # 3 jurusan per halaman
    page_number = request.GET.get('page')
    jurusan_page = paginator.get_page(page_number)

    # Queryset Berita (tanpa pagination)
    berita_list = news.objects.all().order_by('-created_at')[:1]
    
    # Ambil statistik sekolah yang aktif
    school_stats = SchoolStatistics.objects.filter(is_active=True).first()

    context = {
        'jurusan_list': jurusan_page,
        'berita_list': berita_list,
        'pengumuman_list': pengumuman_list,
        'pengumuman_penting': pengumuman_penting,
        'school_stats': school_stats,
        'guru_staff_list': guru_staff_list,
    }

    return render(request, 'index.html', context)



def profil(request):

    struktur_organisasi = StaffDanGuru.objects.all()
    
    context = {
        'struktur_organisasi': struktur_organisasi,
    }
    return render(request, 'profil/profil_sekolah.html', context)

def fasilitas(request):
    # Ambil semua data laboratorium beserta peralatannya
    peralatanlab_list = PeralatanLab.objects.all()
    laboratorium_list = FasilitasLab.objects.select_related('jurusan').prefetch_related('peralatan').all()
    
    context = {
        'laboratorium_list': laboratorium_list,
        'peralatanlab_list': peralatanlab_list,
    }
    return render(request, 'profil/fasilitas.html', context)

def guru_staff(request):
    leader_titles = ['Kepala Sekolah', 'Waka bidang Sarana dan Prasarana', 'Waka bidang Kurikulum', 'Waka bidang Hubungan Masyarakat', 'Waka bidang Kesiswaan']
    # Ambil semua data staff untuk bagian pimpinan (filter di template)
    all_staff = StaffDanGuru.objects.filter(jabatan__in=leader_titles).order_by('created_at')
    
    # Filter untuk paginasi (hanya guru reguler, exclude pimpinan)
    regular_staff = StaffDanGuru.objects.exclude(jabatan__in=leader_titles).order_by('created_at')
    
    # Pagination (6 guru per halaman)
    paginator = Paginator(regular_staff, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    context = {
        'leaders_list': all_staff, # Untuk section Kepala Sekolah & Waka
        'guru_staff_list': page_obj, # Untuk section Daftar Guru (paginated)
    }
    return render(request, 'profil/guru-staff.html', context)

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
    pengumuman_list = Pengumuman.objects.all().order_by('-created_at')
    pengumuman_penting = Pengumuman.objects.filter(category__nama='Penting').order_by('-created_at')
    
    # Pencarian
    search_query = request.GET.get('search')
    if search_query:
        pengumuman_list = pengumuman_list.filter(
            Q(judul__icontains=search_query) | 
            Q(deskripsi__icontains=search_query) |
            Q(category__nama__icontains=search_query)
        )
    
    # Fetch all categories for the filter buttons
    pengumuman_category = categoryPengumuman.objects.all().order_by('nama')
    
    # Filter by category if present
    category_name = request.GET.get('category')
    selected_category = categoryPengumuman.objects.filter(nama=category_name).first() if category_name else None
    
    if category_name:
        try:
            pengumuman_list = pengumuman_list.filter(category__nama=category_name)
        except (ValueError, categoryPengumuman.DoesNotExist):
            pass

    # For files section - filter based on filtered announcements
    pengumuman_file = pengumuman_list.filter(files__isnull=False).distinct().order_by('-created_at')

    # ===== HITUNG STATISTIK DOWNLOAD =====
    # Total file yang ada
    total_files = FilePengumuman.objects.filter(pengumuman__in=pengumuman_list).count()
    
    # Total download dari semua file
    total_downloads = FilePengumuman.objects.filter(
        pengumuman__in=pengumuman_list
    ).aggregate(total=Sum('download_count'))['total'] or 0
    
    # File paling banyak di-download
    most_downloaded_file = FilePengumuman.objects.filter(
        pengumuman__in=pengumuman_list
    ).order_by('-download_count').first()

    paginator = Paginator(pengumuman_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'pengumuman_list': page_obj,
        'search_query': search_query,
        'pengumuman_penting': pengumuman_penting,
        'pengumuman_category': pengumuman_category,
        'pengumuman_file': pengumuman_file,
        'selected_category': selected_category,
        # ===== TAMBAHKAN STATISTIK KE CONTEXT =====
        'total_files': total_files,
        'total_downloads': total_downloads,
        'most_downloaded_file': most_downloaded_file,
    }
    return render(request, 'pengumuman/pengumuman.html', context)

def detail_pengumuman(request, slug):
    # Mengambil pengumuman berdasarkan slug
    pengumuman_detail = get_object_or_404(Pengumuman, slug=slug)
    
    # Increment view count
    pengumuman_detail.view_count += 1
    pengumuman_detail.save()
    
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
    mitra_industri_list = MitraIndustri.objects.all()
    return render(request, 'program/jurusan/jurusan.html', {
        'jurusan_list': jurusan_list, 
        'jurusan_utama': jurusan_utama,
        'mitra_industri_list': mitra_industri_list
    })

def program_studi_detail(request, slug):
    # Mengambil jurusan berdasarkan slug
    jurusan_detail = get_object_or_404(Jurusan, slug=slug)
    jurusan_detail = Jurusan.objects.get(slug=slug)
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