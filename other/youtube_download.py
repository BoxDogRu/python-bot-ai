from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=xNe3mp7ross') #ссылка на видео.
# yt.stream показывает какое видео ты можешь скачать
# (mp4(720) + audio или только mp4(1080) без звука).
# Сейчас стоит фильтр по mp4.
print(yt.streams.filter(file_extension='mp4'))
stream = yt.streams.get_by_itag(22) #выбираем по тегу, в каком формате будем скачивать.
stream.download() #загружаем видео.