from __future__ import unicode_literals
import yt_dlp as youtube_dl
from youtube_search import YoutubeSearch
import uuid

from flask import Flask, request, abort, send_from_directory

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

SongsList = []
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('gSll+ibOBywXRyYMtqoR2DC2+TdZWqOBLjtKwvbfQHZ4L9uVFkKjK6gHYM++Vl+3vBr9yy3EkEcnvo5WLyfpa6Pgoe7EDPFlAA/MpF2QNh5QLJEBnK8QnDeMmCXL81TgerhoMPLTTxvXG6C54DgDuwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a0d741e8d30f007a1f55f800d6c60b80')

def download(music_url):
    name = str(uuid.uuid4())
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl' : f'/tmp/{name}.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([music_url])
        return name

def send(music_url):
    name = download(str(music_url))
    return f'https://cloversfamily.herokuapp.com/file/{name}'

def show_list():
    return SongsList

def Sticker():
    message = StickerSendMessage(
        package_id='11539',
        sticker_id='52114116'
    )
    return message

def Confirm_Template():
    message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='Download Ways',
            actions=[
                PostbackTemplateAction(
                    label='Send URL',
                    text='URL：',
                    data='1'
                ),
                MessageTemplateAction(
                    label='Search Name',
                    text='Name：'
                )
            ]
        )
    )
    return message

def Carousel_Template(results):
    message = TemplateSendMessage(
        alt_text='一則旋轉木馬按鈕訊息',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=results[0]['thumbnails'][0],
                    title='Time：' + results[0]['duration'] + '／' + results[0]['views'],
                    text=(results[0]['title'])[:60],
                    actions=[
                        PostbackTemplateAction(
                            label='♡',
                            # data='1'
                            data='https://www.youtube.com/' + results[0]['url_suffix']
                        ),
                        URITemplateAction(
                            label='download',
                            uri=send('https://www.youtube.com/' + results[0]['url_suffix'])
                        ),
                        URITemplateAction(
                            label='Website',
                            uri='https://www.youtube.com/' + results[0]['url_suffix']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=results[1]['thumbnails'][0],
                    title='Time：' + results[1]['duration'] + '／' + results[1]['views'],
                    text=(results[1]['title'])[:60],
                    actions=[
                        PostbackTemplateAction(
                            label='♡',
                            # data='2'
                            data='https://www.youtube.com/' + results[1]['url_suffix']
                        ),
                        URITemplateAction(
                            label='download',
                            uri=send('https://www.youtube.com/' + results[1]['url_suffix'])
                        ),
                        URITemplateAction(
                            label='Website',
                            uri='https://www.youtube.com/' + results[1]['url_suffix']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=results[2]['thumbnails'][0],
                    title='Time：' + results[2]['duration'] + '／' + results[2]['views'],
                    text=(results[2]['title'])[:60],
                    actions=[
                        PostbackTemplateAction(
                            label='♡',
                            # data='3'
                            data='https://www.youtube.com/' + results[2]['url_suffix']
                        ),
                        URITemplateAction(
                            label='download',
                            uri=send('https://www.youtube.com/' + results[2]['url_suffix'])
                        ),
                        URITemplateAction(
                            label='Website',
                            uri='https://www.youtube.com/' + results[2]['url_suffix']
                        )
                    ]
                )
            ]
        )
    )
    return message

@app.route("/file/<name>", methods=['GET'])
def sendFile(name):
    return send_from_directory('/tmp/', f'{name}.mp3')


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if data not in SongsList:
        SongsList.append(str(data))
    return SongsList
    
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):  
    inputs = event.message.text
    if (inputs == 'select'):
        line_bot_api.reply_message(event.reply_token, Confirm_Template())
    if ((inputs)[:4] == 'http'):
        music_url = inputs
        name = download(str(music_url))
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(f'https://cloversfamily.herokuapp.com/file/{name}'), Sticker()])
    if (inputs == 'show list'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\n".join(show_list())))
    if (inputs == 'remove all'):
        SongsList.clear()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='removed'))
    if (inputs == 'remove one'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Which one would you remove?(0~...)'))
    if inputs.isnumeric():
        SongsList.pop(int(inputs))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\n".join(show_list())))
    elif(inputs != 'select' and inputs != 'URL：' and inputs != 'Name：' and inputs != 'show list' and inputs != 'remove all' and inputs != 'remove one'):
        SongsName = inputs
        results = YoutubeSearch(SongsName, max_results=10).to_dict()
        line_bot_api.reply_message(event.reply_token, Carousel_Template(results))

#網址類似https://linebotName.herokuapp.com/test?name=1
@app.route('/test')
def test_page():
    global name
    name=request.values.get('name')
    message = ImageSendMessage(
        original_content_url='https://firebasestorage.googleapis.com/v0/b/project-6435563441602913509.appspot.com/o/image%2F'+name+'.jpg?alt=media&token=none',
        preview_image_url='https://firebasestorage.googleapis.com/v0/b/project-6435563441602913509.appspot.com/o/image%2F'+name+'.jpg?alt=media&token=none'
    )
    line_bot_api.push_message('Uf7ccf8963b879004383a8786b910e5b7', message)
    return name

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
