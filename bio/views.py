from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from bio.models import Question, Answer
from .froms import QuestionForm, AnswerForm
import os, bs4, requests, urllib, re

# Create your views here.

def overview(request):
    return render(request, 'overview.html')


def personality(request):
    return render(request, 'personality.html')


def trailers(request):
    return render(request, 'trailers.html')


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


def edit_answer(request, id):
        answer = Answer.objects.get(id=id)
        
        if request.method != 'POST':
                form = AnswerForm()
        else:
                form = AnswerForm(data=request.POST)

        if form.is_valid():
                answer.text = answer.text + '\n' + request.POST['text']
                answer.save()
                return HttpResponseRedirect(reverse('bio:faq'))

        context = {'answer':answer, 'form':form}
        return render(request, 'edit_answer.html', context)


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
                return HttpResponseRedirect(reverse('bio:faq'))

        context = {'question':question, 'form':form}
        return render(request, 'add_answer.html', context)


def add_question(request):
        if request.method != 'POST':
                form = QuestionForm()
        else:
                form = QuestionForm(data=request.POST)
                if form.is_valid():
                        form.save()
                        return HttpResponseRedirect(reverse('bio:faq'))

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