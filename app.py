from flask import Flask,render_template,request,url_for,redirect,send_file
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, VideoPrivate
from math import *
from io import BytesIO

app=Flask(__name__)

yt='None of the '
version='2.0.1'

@app.context_processor
def getAppVerion():
    return {'version':version}

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route("/show" , methods=['POST','GET'])
def open_link():
    if request.method=='GET':
        link=request.args.get('link')
        is_valid_link=False
        try:
            global yt
            yt=YouTube(link)
            print(yt.check_availability)
            titile=yt.title
            # muted_itags=[313,271,137,136,244,18,133,17,571]
            return render_template("index.html",yt=yt,is_valid_link=True)
        except VideoUnavailable:
            yt=False
            message=f'video found!, pls recheck the link "{link}" '            
        except VideoPrivate:
            yt=False
            message=f'This video is in private mode!, we cannot serve this video '
        except Exception as e:
            yt=False
            message=f'something is fishy!!, we are not able to process your request at this time!, pls try again after sometime!'
            return render_template("index.html",yt=yt,message=message,is_valid_link=is_valid_link)
    else:
        redirect('/')  

@app.route("/download/<itag>/<type>/")
def download(itag,type):
    mime_type=None
    extension=None
    if type=="audio":
        mime_type='audio/mp3'
        extension='.mp3'
    elif type=='video':
        mime_type='video/mp4'
        extension='.mp4'
    try:
        buffer=BytesIO()
        item=yt.streams.get_by_itag(itag)
        item.stream_to_buffer(buffer)
        buffer.seek(0)
        file_name=yt.title+extension
        return send_file(buffer,as_attachment=True,download_name=file_name,mimetype=mime_type)
    except AttributeError:
        return render_template('alert.html',message='Link expired, pls enter the link once again!')
    except:
        return render_template('alert.html',message='Link expired, pls enter the link once again!')


if __name__=='__main__':
    app.run(debug=True)