# ---------- VERSATILE IMAGE FIELD CONFIG ---------- #

# Versatile image field sizes: http://django-versatileimagefield.readthedocs.org/en/latest/drf_integration.html
# ------------------------------------------------------------------------------
VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "default_image_sizes": [
        ("original", "url"),
        ("full_size", "thumbnail__1080x1080"),
        ("medium", "thumbnail__600x600"),
        ("small", "thumbnail__150x150"),
    ]
}

VERSATILEIMAGEFIELD_SETTINGS = {
    "jpeg_resize_quality": 100,  # default is 70
    "progressive_jpeg": True,  # default is False
    "cache_length": 365 * 24 * 60 * 60,  # a year cache for the image
    "create_images_on_demand": False,  # default is True
}

# Valid Image Mime Types
VALID_MIME_TYPES = [
    "image/jpeg",
    "image/gif",
    "image/png",
    "image/bmp",
    "image/eps",
    "image/ico",
    "image/im",
    "image/gif",
    "image/pcx",
    "image/ppm",
    "image/sgi",
    "image/xbm",
    "image/webp",
]
