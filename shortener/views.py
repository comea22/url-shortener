from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import ShortURL
from .utils import generate_unique_short_code
from .forms import ShortURLForm


def create_short_url(request):
    if request.method == "POST":
        form = ShortURLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            password = form.cleaned_data['password']

            short_code = generate_unique_short_code(length=8)

            short_url_obj = ShortURL.objects.create(
                original_url=original_url,
                short_code=short_code,
                password=password,
            )

            form = ShortURLForm(initial={'original_url': original_url})
            return render(request, "shortener/form.html", {
                "form": form,
                "short_url": short_url_obj.get_short_url(),
            })
        else:
            # 表單驗證失敗，返回帶有錯誤訊息的表單
            return render(request, "shortener/form.html", {
                "form": form,
            })
    else:
        form = ShortURLForm()
        return render(request, "shortener/form.html", {
            "form": form,
        })


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