from django.db import migrations, models, connection

def add_columns_if_missing(apps, schema_editor):
    def column_exists(table, column):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"SHOW COLUMNS FROM {table} LIKE '{column}'")
                return cursor.fetchone() is not None
            except Exception:
                return False

    Jurusan = apps.get_model('otak_aplikasi', 'Jurusan')
    ProspekKarir = apps.get_model('otak_aplikasi', 'ProspekKarir')

    # JURUSAN FIELDS
    fields_to_check = [
        ('icon', models.CharField(default='terminal', help_text='Material Symbols name', max_length=50)),
        ('view_count', models.IntegerField(default=0)),
        ('kaprodi_nama', models.CharField(blank=True, max_length=200, null=True)),
        ('kaprodi_email', models.EmailField(blank=True, max_length=254, null=True)),
        ('kaprodi_foto', models.ImageField(blank=True, null=True, upload_to='jurusan/kaprodi/')),
    ]
    
    for name, field in fields_to_check:
        field.name = name
        if not column_exists('otak_aplikasi_jurusan', name):
            print(f"Adding missing column: {name}")
            schema_editor.add_field(Jurusan, field)
        else:
            print(f"Column {name} exists, skipping.")

    # REMOVE KAPRODI
    if column_exists('otak_aplikasi_jurusan', 'kaprodi_id'):
        print("Removing kaprodi_id column")
        try:
            field = Jurusan._meta.get_field('kaprodi')
            schema_editor.remove_field(Jurusan, field)
        except Exception as e:
            print(f"Error removing kaprodi: {e}")

    # PROSPEK KARIR
    rata_gaji_field = models.CharField(blank=True, max_length=100, null=True)
    rata_gaji_field.name = 'rata_gaji'
    if not column_exists('otak_aplikasi_prospekkarir', 'rata_gaji'):
        print("Adding missing column: rata_gaji")
        schema_editor.add_field(ProspekKarir, rata_gaji_field)
    else:
        print("Column rata_gaji exists, skipping.")


class Migration(migrations.Migration):

    dependencies = [
        ('otak_aplikasi', '0018_alter_ektra_content'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_columns_if_missing, migrations.RunPython.noop)
            ],
            state_operations=[
                migrations.AddField(
                    model_name='jurusan',
                    name='icon',
                    field=models.CharField(default='terminal', help_text='Material Symbols name', max_length=50),
                ),
                migrations.AddField(
                    model_name='jurusan',
                    name='view_count',
                    field=models.IntegerField(default=0),
                ),
                migrations.AddField(
                    model_name='jurusan',
                    name='kaprodi_nama',
                    field=models.CharField(blank=True, max_length=200, null=True),
                ),
                migrations.AddField(
                    model_name='jurusan',
                    name='kaprodi_email',
                    field=models.EmailField(blank=True, max_length=254, null=True),
                ),
                migrations.AddField(
                    model_name='jurusan',
                    name='kaprodi_foto',
                    field=models.ImageField(blank=True, null=True, upload_to='jurusan/kaprodi/'),
                ),
                migrations.AddField(
                    model_name='prospekkarir',
                    name='rata_gaji',
                    field=models.CharField(blank=True, max_length=100, null=True),
                ),
                migrations.RemoveField(
                    model_name='jurusan',
                    name='kaprodi',
                ),
            ]
        )
    ]