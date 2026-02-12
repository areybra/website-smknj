import os
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def compress_image(image, size=(800, 800), quality=85):
    """
    Mengompres gambar sebelum disimpan ke database.
    """
    if not image:
        return None
        
    img = Image.open(image)
    
    # Konversi ke RGB jika formatnya RGBA atau P (penting untuk JPEG)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    img.thumbnail(size)
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality)
    output.seek(0)
    
    return ContentFile(output.getvalue(), name=image.name)

def generate_unique_slug(model_class, text, slug_field='slug', exclude_pk=None):
    """
    Menghasilkan slug unik untuk model tertentu.
    """
    slug = slugify(text)
    unique_slug = slug
    counter = 1
    
    queryset = model_class.objects.filter(**{slug_field: unique_slug})
    if exclude_pk:
        queryset = queryset.exclude(pk=exclude_pk)
        
    while queryset.exists():
        unique_slug = f"{slug}-{counter}"
        queryset = model_class.objects.filter(**{slug_field: unique_slug})
        if exclude_pk:
            queryset = queryset.exclude(pk=exclude_pk)
        counter += 1
        
    return unique_slug
