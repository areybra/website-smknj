import os, django
import sys

# Ensure file is opened
try:
    with open('check_output.txt', 'w') as f:
        sys.stdout = f
        sys.stderr = f
        
        print("Starting check...")
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_smknj.settings')
            django.setup()
            
            from django.db import connection
            from otak_aplikasi.models import Jurusan, Kompetensi
            
            print("--- Checking Columns ---")
            with connection.cursor() as cursor:
                cursor.execute("DESCRIBE otak_aplikasi_kompetensi")
                columns = [r[0] for r in cursor.fetchall()]
                print(f"Columns in otak_aplikasi_kompetensi: {columns}")
                
            print("\n--- Checking Relationship ---")
            j = Jurusan.objects.first()
            if j:
                print(f"Jurusan: {j.nama}")
                print("Accessing j.kompetensi.all():")
                qs = j.kompetensi.all()
                print(list(qs))
            else:
                print("No Jurusan found.")
                
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            import traceback
            traceback.print_exc()

except Exception as e:
    # If we can't open file, we can't do much
    pass
