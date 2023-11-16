# https://github.com/pytube/pytube
# в терминале: pip install pytube

from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=dQw4w9WgXcQ')     # ссылка на видео

# yt.stream показывает какое видео ты можешь скачать
streams = yt.streams.filter(file_extension='mp4')   # фильтр по mp4
for kind in streams:
    print(kind)

stream = streams.get_by_itag(18)    # выбираем по тегу в каком формате будем скачивать (+acodec)
stream.download()   # загружаем видео
