from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request, 'core/home.html',context)   

def sitemaps(request):
    context = {}
    return render(request, 'core/sitemap.xml',context)   