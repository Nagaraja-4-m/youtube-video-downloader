from flask import Flask,render_template,request,url_for,redirect,send_file
from pytube import YouTube
from math import *
from io import BytesIO

app=Flask(__name__)

@app.route('/')
def home_page():
    return render_template("index.html",count=0)

@app.route("/link" , methods=['POST','GET'])
def open_link():
    if request.method =='POST':
        video_link=request.form['link']
        video_id=None
        is_valid_link=True
        
        try:
            global yt
            yt=YouTube(video_link)
            muted_itags=[313,271,137,136,244,18,133,17,571]
            return render_template("index.html",yt=yt,link_validity=is_valid_link,count=2,muted_itags=muted_itags)
        
        except:
            is_valid_link=False
            return render_template("index.html",link_validity=is_valid_link,count=2)
        
        return "None"

@app.route("/download/<itag>/<type>/")
def download(itag,type):

    #intializing mime_type and extention
    mime_type=None
    extension=None
    if type=="audio":
        mime_type='audio/mp3'
        extension='.mp3'
    elif type=='video':
        mime_type='video/mp4'
        extension='.mp4'

    buffer=BytesIO()
    item=yt.streams.get_by_itag(itag)
    item.stream_to_buffer(buffer)
    buffer.seek(0)
    file_name=yt.title+extension
    return send_file(buffer,as_attachment=True,download_name=file_name,mimetype=mime_type)


if __name__=='__main__':
    app.run(debug=True)