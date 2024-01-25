# from __future__ import unicode_literals
# import youtube_dl

# # 
# # ydl_opts = {
# #     'format': 'bestaudio/best',
# #     'postprocessors': [{
# #         'key': 'FFmpegExtractAudio',
# #         'preferredcodec': 'mp3',
# #         'preferredquality': '192',
# #     }],
# # }
# # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# #     ydl.download(['https://www.youtube.com/watch?v=ioNng23DkIM'])

# def download(music_url):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl' : '/tmp/1.webm'
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([music_url])
# def test(url):
#     music_url = 'https://www.youtube.com/watch?v=dyRsYk0LyA8'
#     download(music_url)
# test(2)

# from youtube_search import YoutubeSearch
# results = YoutubeSearch('千年以後', max_results=10).to_dict()
# # print('片長：' + results[1]['duration'] + '\t' + results[1]['views'])
# print('https://www.youtube.com/' + results[1]['url_suffix'])
inputs = '2'
if inputs.isnumeric():
    print('y')
else:
    print('n')