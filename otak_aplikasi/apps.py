from django.apps import AppConfig


class OtakAplikasiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otak_aplikasi'
    verbose_name = "Otak Aplikasi"

    def ready(self):
        import otak_aplikasi.signals
