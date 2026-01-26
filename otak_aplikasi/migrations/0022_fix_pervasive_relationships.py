from django.db import migrations, models, connection
import django.db.models.deletion

def add_jurusan_column_if_missing(apps, schema_editor):
    Jurusan = apps.get_model('otak_aplikasi', 'Jurusan')
    
    # List of models and their table names to check/fix
    models_to_fix = [
        ('ProspekKarir', 'otak_aplikasi_prospekkarir'),
        ('MitraIndustri', 'otak_aplikasi_mitraindustri'),
        ('Sertifikasi', 'otak_aplikasi_sertifikasi'),
        ('FasilitasJurusan', 'otak_aplikasi_fasilitasjurusan'),
        ('TestimoniAlumni', 'otak_aplikasi_testimonialumni'),
    ]

    for model_name, table_name in models_to_fix:
        # Check if table exists first (to be safe against previous drops)
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            if not cursor.fetchone():
                print(f"Table {table_name} does not exist, skipping.")
                continue
            
            # Check if column exists
            cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'jurusan_id'")
            if not cursor.fetchone():
                print(f"Adding missing column: jurusan_id to {table_name}")
                Model = apps.get_model('otak_aplikasi', model_name)
                field = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name=model_name.lower(), null=True)
                field.set_attributes_from_name('jurusan')
                schema_editor.add_field(Model, field)
            else:
                print(f"Column jurusan_id exists in {table_name}, skipping.")

class Migration(migrations.Migration):

    dependencies = [
        ('otak_aplikasi', '0021_fix_kompetensi_schema'),
    ]

    operations = [
       migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_jurusan_column_if_missing, migrations.RunPython.noop)
            ],
            state_operations=[
                migrations.AddField(
                    model_name='prospekkarir',
                    name='jurusan',
                    field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='prospek_karir', to='otak_aplikasi.jurusan'),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='mitraindustri',
                    name='jurusan',
                    field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mitra_industri', to='otak_aplikasi.jurusan'),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='sertifikasi',
                    name='jurusan',
                    field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sertifikasi', to='otak_aplikasi.jurusan'),
                    preserve_default=False,
                ),
                 migrations.AddField(
                    model_name='fasilitasjurusan',
                    name='jurusan',
                    field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fasilitas', to='otak_aplikasi.jurusan'),
                    preserve_default=False,
                ),
                 migrations.AddField(
                    model_name='testimonialumni',
                    name='jurusan',
                    field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='testimoni_alumni', to='otak_aplikasi.jurusan'),
                    preserve_default=False,
                ),
            ]
        )
    ]
