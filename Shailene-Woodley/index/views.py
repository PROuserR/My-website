from django.shortcuts import render
from GoogleNews import GoogleNews


# Create your views here.
def index(request):
    googlenews = GoogleNews()
    googlenews.search('Shailene Woodley')
    news = googlenews.result()

    context = {'news': news}
    return render(request, 'index.html', context)
