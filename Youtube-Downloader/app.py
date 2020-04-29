from flask import Flask, render_template, request, url_for, redirect, send_file
from pytube import YouTube
import os

app = Flask(__name__)


@app.route('/')
def hello():
    url = request.args.get('url')
    choice = request.args.get('choice')

    if url:
        yt = YouTube(str(url))
        videos = yt.streams.all()
        videos_str = [str(var) for var in videos]
        if not choice:
            return render_template('home.html', videos = videos_str, loading = True, checked = True, url=url)
        else:
            choice=int(choice)
            vid = videos[choice]
            destination = 'D:\Projects\Python\WebProjects\YoutubeDownloader\YoutubeDownloader\static\downloads' # Your path
            
            if os.path.exists(destination + '\\' + vid.default_filename):
                return send_file(destination + '\\' + vid.default_filename , as_attachment = True)
            else:
                vid.download(destination)
                return send_file(destination + '\\' + vid.default_filename , as_attachment = True)

    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug = True)


