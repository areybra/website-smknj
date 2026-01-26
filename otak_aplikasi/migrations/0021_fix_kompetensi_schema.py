from django.db import migrations, models, connection
import django.db.models.deletion

def add_jurusan_column_if_missing(apps, schema_editor):
    def column_exists(table, column):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"SHOW COLUMNS FROM {table} LIKE '{column}'")
                return cursor.fetchone() is not None
            except Exception:
                return False

    Kompetensi = apps.get_model('otak_aplikasi', 'Kompetensi')
    Jurusan = apps.get_model('otak_aplikasi', 'Jurusan')

    if not column_exists('otak_aplikasi_kompetensi', 'jurusan_id'):
        print("Adding missing column: jurusan_id to Kompetensi")
        # Since we can't easily use schema_editor.add_field with ForeignKey in RunPython easily without strict state,
        # we will use raw SQL for safety in this specific rescue scenario, OR try standard add_field.
        # Standard add_field is better if we trust the state.
        # But wait, we are in RunPython.
        
        # Let's try standard add_field on the retrieved model.
        field = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='kompetensi', null=True) # temporarily null
        field.set_attributes_from_name('jurusan')
        schema_editor.add_field(Kompetensi, field)
    else:
        print("Column jurusan_id exists in Kompetensi, skipping.")

class Migration(migrations.Migration):

    dependencies = [
        ('otak_aplikasi', '0020_remove_galerijurusan_jurusan_delete_guru_and_more'),
    ]

    operations = [
       migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_jurusan_column_if_missing, migrations.RunPython.noop)
            ],
            state_operations=[
                migrations.AddField(
                    model_name='kompetensi',
                    name='jurusan',
                    field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='kompetensi', to='otak_aplikasi.jurusan'),
                    preserve_default=False,
                ),
            ]
        )
    ]
