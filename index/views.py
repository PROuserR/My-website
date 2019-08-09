from django.shortcuts import render
import bs4, requests, re



# Create your views here.
def index(request):
    req = requests.get('https://www.google.com/search?q=shailene+woodley&client=ubuntu&hs=9UM&tbm=nws&source=lnms&sa=X&ved=0ahUKEwjPjcj1qOfjAhVi8eAKHRZvAg0Q_AUIDSgB&biw=1366&bih=609&dpr=1')
    soup = bs4.BeautifulSoup(req.text)
    divs = soup.select('.g')
    news = []
    pattern = r'\w+'
    for div in divs:
        new = []
        con = list(div.find(name='div', attrs={'class':'st'}).contents)
        
        for i in range(len(con)):
            con[i] = str(con[i])

        for chunck in con:
            if '<b>' in chunck:
                con.remove(chunck)

        con = str(con)
        regx = re.findall(pattern, con)
        try:
            regx.remove('xa0')
        except:
            pass
        con = ' '.join(regx)
        meta = str(div.find('span').contents)[2:-2]
        header = str(div.findAll(name='a')[1].attrs.get('href'))[14:]
        title = ' '.join(regx[:3])
        new.append(con)
        new.append(meta)
        new.append(header)
        new.append(title)

        news.append(new)
        
    
    context = {'news': news}
    return render(request, 'index.html', context)
