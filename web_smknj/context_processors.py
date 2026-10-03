from otak_aplikasi.models import Jurusan, ektraCategory, newsCategory

def global_navbar_data(request):
    return {
        'nav_jurusan_list': Jurusan.objects.all(),
        'nav_news_categories': newsCategory.objects.all(),
    }
