from django.shortcuts import render, reverse, redirect
from bio.models import Question, Answer
from .froms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
import time, bs4, requests, urllib, re, os

# Create your views here.

def overview(request):
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    if not month > 11:
            year -= 1
    shai_age = year - 1991
    context = {'shai_age': shai_age}
    return render(request, 'overview.html', context)


def personality(request):
        if request.method == 'POST':
           url = 'https://www.celebrities-galore.com/index.php?id=517'
           data = {'CelebID': '287718', 'CelebFileName': 'shailene-woodley', 'CommonName': request.POST['name']
           , 'Gender': request.POST['gender'], 'monthDOB': request.POST['month'], 
           'dayDOB': request.POST['day'], 'yearDOB': request.POST['year']}
           req = requests.post(url, data=data)
           soup = bs4.BeautifulSoup(req.text)
           ps = soup.select('p')
           fetcheData = []
           for p in ps:
                p = str(p.getText())
                fetcheData.append(p)
           context = {'fetcheData': fetcheData}
           return render(request, 'compatibility.html', context)
        else:
           return render(request, 'personality.html')


def trailers(request):
    return render(request, 'trailers.html')


@login_required
def faq(request):
        answers = Answer.objects.order_by('date_added')
        q = Question.objects.order_by('date_added')
        questions = []
        for i in range(len(q)):
                try:
                        if str(q[i]) not in str(answers[i].question):
                                questions.append(q[i])
                except:
                        questions.append(q[i])
                
        
        context = {'answers':answers, 'questions':questions}
        return render(request, 'faq.html', context)


@login_required
def edit_answer(request, id):
        answer = Answer.objects.get(id=id)
        
        if request.method != 'POST':
                form = AnswerForm()
        else:
                form = AnswerForm(data=request.POST)

        if form.is_valid():
                answer.text = answer.text + '\n' + request.POST['text']
                answer.save()
                return redirect('bio:faq')

        context = {'answer':answer, 'form':form}
        return render(request, 'edit_answer.html', context)


@login_required
def add_answer(request, id):
        question = Question.objects.get(id=id)
        if request.method != 'POST':
                form = AnswerForm()
        else:
                form = AnswerForm(data=request.POST)

                if form.is_valid():
                        new_answer = form.save(commit=False)
                        new_answer.question = question
                        new_answer.save()
                return redirect('bio:faq')

        context = {'question':question, 'form':form}
        return render(request, 'add_answer.html', context)


@login_required
def add_question(request):
        if request.method != 'POST':
                form = QuestionForm()
        else:
                form = QuestionForm(data=request.POST)
                if form.is_valid():
                        new_question = form.save(commit=False)
                        new_question.owner = request.user
                        new_question.save()
                        return redirect('bio:faq')

        context = {'form':form}
        return render(request, 'add_question.html', context)
   

def movies(request):
    req = requests.get('https://www.thefamouspeople.com/filmography/shailene-woodley-29853.php')
    soup = bs4.BeautifulSoup(req.text)
    imgs = soup.select('.img-responsive')
    imgs2 = soup.findAll(name='img', attrs={'class': 'loader_image img-responsive'})


    sources = []
    for img in imgs:
            if img.attrs.get('src') != None and img.attrs.get('src') != '':
                source = 'https:' + img.attrs.get('src')
                sources.append(source)


    for img in imgs2:
        source = 'https:' + img.attrs.get('data-src')
        sources.append(source)


    data = []
    pattern = r'\w+'
    for i in range(len(sources)):
            d = []
            d.append(sources[i])
            title = os.path.basename(urllib.parse.urlparse(sources[i]).path)
            title = title[:-4]
            
            title = re.findall(pattern, title)
            for chunck in title:
                if chunck.isnumeric():
                        title.remove(chunck)

            for i in range(len(title)):
                    title[i] = title[i]
            title = ' '.join(title)
            title = title.upper()
            d.append(title)
            data.append(d)


    context = {'data':data}
    return render(request, 'movies.html', context)


def butwhy(request):
    return render(request, 'butwhy.html')