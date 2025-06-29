from django.shortcuts import render,  get_object_or_404, redirect
from django.http import HttpResponse
from .models import ShortURL
from .utils import generate_unique_short_code
from .forms import ShortURLForm



def create_short_url(request):
    if request.method == "POST":
        original_url = request.POST.get("original_url")
        password = request.POST.get("password")

        short_code = generate_unique_short_code(length=8)

        short_url_obj = ShortURL.objects.create(
            original_url=original_url,
            short_code=short_code,
            password=password,
        )

        return render(request, "shortener/form.html", {
            "original_url": original_url,
            "short_url": short_url_obj.get_short_url(),
        })

    return render(request, "shortener/form.html")


def redirect_short_url(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    if short_url.password:
        if request.method == 'POST':
            entered_password = request.POST.get('password')
            if entered_password == short_url.password:
                return redirect(short_url.original_url)
            else:
                return render(request, 'shortener/password_prompt.html', {
                    'short_code': short_code,
                    'error': '密碼錯誤，請再試一次！'
                })
        else:
            return render(request, 'shortener/password_prompt.html', {
                'short_code': short_code
            })
    return redirect(short_url.original_url)


# Create your views here.
