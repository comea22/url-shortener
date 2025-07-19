from django.utils.crypto import get_random_string
from .models import ShortURL

def generate_unique_short_code(length=8):
    while True:
        code = get_random_string(length=length)
        if not ShortURL.objects.filter(short_code=code).exists():
            return code
