# Разработка ботов на базе нейросетей
## Python в ИИ от Яндекса, группа 21

## 1. Материалы к вебинарам

В папках - код, разбираемый на вебинарах. База: [Python+PyCharm - инструкция по установке](https://praktikum.notion.site/44fdf3dccf074a62a916c44d5568acdb).

requirements.txt - используемые библиотеки.

## 2. Библиотечка AI-инструментов

### AI - текстовые
* [GPT от OpenAI](https://chat.openai.com/).
* [Chatpdf - суммаризатор pdf](https://www.chatpdf.com/).
* [Perplexity.ai - ответы на вопросы](https://www.perplexity.ai/).
* [Explainlikeimfive.io - ответы на вопросы](https://explainlikeimfive.io/).

### AI - генераторы изображений
* [Midjourney](https://www.midjourney.com/home/)
* [DALL·E 2 от OpenAI](https://labs.openai.com/)
* [Кандинский от Сбера](https://fusionbrain.ai/editor/)
* [Шедеврум от YandexGPT](https://shedevrum.ai/)
* [Stable diffusion](https://www.stablediffusionai.ai/ru)
* [Krea.ai](https://www.krea.ai/)
* [Roomgpt.io](https://www.roomgpt.io/dream) - redesign your room
* [Picfinder.ai](https://picfinder.ai/)
* [lumalabs.ai](https://lumalabs.ai/genie) - генератор 3D моделей

Промпт-инжиниринг:
* [Promt Engineering Template](https://docs.google.com/spreadsheets/d/1TWYoCaPVPllyoZyjOhnPeojfzgTbppMDhpK_r87-duM/edit#gid=0). Плюс [Visual Prompt Builder](https://tools.saxifrage.xyz/prompt) от автора этого же шаблона Майка Тейлора, мотивированного маркетолога-практика. Больше подробностей - [в публикации автора](https://www.saxifrage.xyz/post/prompt-engineering).
* [Руководство по промпт-инжинирингу](https://www.promptingguide.ai/ru).

Дополнительно:
* [DALL·E 3 vs Midjourney](https://atachkina.com/dalle3) - сравнительный анализ.
* [Ai molodca 🤖](https://t.me/strangedalle) - канал в телеге, где какой-то чувак показывает картинки, которые делает компьютер.

### AI - генерация музыки, работа с голосом
* [Soundraw.io](https://soundraw.io/)
* [Elevenlabs.io](https://elevenlabs.io/)


## 3. Библиотечка AI для разработчика
* [Каталог плагинов для ChatGPT](https://www.phind.com/) от чувака с Реддита.
* [Phind.com - AI для кодера](https://www.phind.com/).
* [Face_recognition](https://github.com/ageitgey/face_recognition) - библиотека для распознавания лиц. Пример colab'а для вебинара 11: [Pillow + Face Recognition](https://colab.research.google.com/drive/17rS98rePRDSS8Tqlg76hutivlCyOBLsI?usp=sharing#scrollTo=y8_9hiruUsx2).
* [Wunjo](https://github.com/wladradchenko/wunjo.wladradchenko.ru) - приложение и нейросетка для распознавания речи и создания дипфейков.



## 4. Полезные материалы по направлениям в Python

### Бэкенд
* [Python - это для всего](https://github.com/vinta/awesome-python).
  * Например, библиотечка [Pillow](https://pythonexamples.org/python-pillow/) - для обработки изображений.
* [Видеолекции Тимофея Хирьянова на YouTube](https://www.youtube.com/@tkhirianov/playlists).
* [Разработка на Python - видеокурс Яндекса](https://habr.com/ru/companies/yandex/articles/498856/) (школа бэкенд-разработки).
* [Краткий справочник для собеседований на бэкендера](https://backendinterview.ru/).

### Git
* [Как установить Git на компьютер](https://likeable-efraasia-4a7.notion.site/Git-8d014c3a992e4481b32accd911294356)
* [Регистрация на GitHub и как создать репозиторий](https://likeable-efraasia-4a7.notion.site/GitHub-1b1e1ae006914c83959d4e2cac2148e9)
* [Онлайн-тренажер по Git](https://learngitbranching.js.org/?locale=ru_RU)
* [Книга Pro Git, pdf](https://losst.pro/wp-content/uploads/2016/08/progit-ru.1027.pdf)

### Разработка ботов в Telegram
* [Первый совместный бот - Цветастик](https://t.me/my_experimental_bot).
  * Можете запросить доступ Collaborator'a к репозиторию [python-bot-ai-fotofilters](https://github.com/BoxDogRu/python-bot-ai-fotofilters/) для тестирования совместной работы в Git.
* Примеры ботов: [список 1](https://praktikum.notion.site/4dee5c4d21e94016b6c601789eafeefb), [список 2](https://praktikum.notion.site/c6c4a87b7be54eb5984fa99ad37027a3).
* [Telegram Bot API](https://core.telegram.org/bots/api). Библиотека [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/). Получить токен для бота: [BotFather](https://t.me/BotFather). 
* [Общедоступные API](https://github.com/public-apis/public-apis) - для расширения функционала ботов.

### Веб-разработка (Django)
* [Обзорный мануал по Django](https://developer.mozilla.org/ru/docs/Learn/Server-side/Django) и [документация](https://django.fun/ru/).
* [Django Packages - маркетплейс под любые задачи](https://djangopackages.org/). Рекомендую попробовать установку Django с [Cookiecutter](https://github.com/cookiecutter/cookiecutter-django).
* Неклассический Django. [Hypergen](https://github.com/runekaagaard/django-hypergen/) - отдохните от JavaScript. Фронтэнд на чистом Python. 

### Десктопная и мобильная разработка
* [PyWebIO](https://pypi.org/project/pywebio/) - создание приложений на основе браузера. Доступна интеграция с веб-сервисами (Flask, Django, FastAPI и др.). Интересная рекомендация от Егора.
* [Kivy](https://github.com/kivy/kivy) - кроссплатформенная среда для разработки приложений.

### Аналитика, data science
* [Хабр Карьера - карьерная карта аналитиков](https://track.habr.com/).
* [Open Data Science - сообщество](https://ods.ai/).
* [Jupyter Notebook Users Manual](https://jupyter.brynmawr.edu/services/public/dblank/Jupyter%20Notebook%20Users%20Manual.ipynb).

### IoT - интернет-вещей
* [EMQ](https://www.emqx.com/en) - The #1 MQTT Platform for IoT.

### Разработка игр (Ren'py)
* [Ren'py - Visual Novel Design](https://www.youtube.com/@vimi/videos). Отличный канал чувака на YouTube.
* [Live2d](https://www.live2d.com/en/) - программа для создания 2D-анимации.


## 5. Разное

* Полезные инструменты:
    * Расширение "Xi" для VSCode. Markdown-like language designed for a personal knowledge base.
    * [JSON Editor Online](https://jsoneditoronline.org/). Кстати, можно заметить определенное сходство словарей python c JSON-объектами. И тут пары «ключ:значение». JSON - текстовый формат обмена данными, используется в REST API.
    * Научится десятипальцевому методу набора на клавиатуре - пригодится на всю жизнь. Самая известная программа - [СОЛО на клавиатуре](https://solo.nabiraem.ru/).
* [Гений Джорджа Буля (2016)](https://vk.com/video-19478017_456239792) - документальный фильм, загугленная ссылка на фильм во ВК.
* [Архетипический маркетинг по М.Марк и К.Пирсон](https://brainmod.ru/magazine/business/archetypal-marketing/) - универсальный метод управления знаниями.

### Телеграм-боты от соавтора данной подборки материалов.
Сделаны на основе [этого решения](https://github.com/ohld/django-telegram-bot). 
Модели расширены через [django-polymorphic-tree](https://github.com/django-polymorphic/django-polymorphic-tree). Некоторые дополнительные расширения указаны ниже. 
Иллюстрации - Midjourney.

* [Психолог-практик.рф](https://t.me/TestotekaBot)
  * matplotlib - для отрисовки графиков.
  * reportlab - для генерации pdf-файлов.
* [Мастерская BoxDogRu](https://t.me/BoxDogRu_bot)
  * [Распознование пород собак по фото](https://boxdog.ru/blog/ai.php) - эксперимент с машинным обучением.
  * Fuzzywuzzy ([статейка о модуле на хабре](https://habr.com/ru/articles/491448/)) - для пользовательского ввода породы собаки (сервис расчета размера будки).
* [Шахматная демо-игра](https://t.me/BlackDragonGameBot)
  * django-translated-fields - поддержка мультиязычности.
  * python-chess - для парсинга шахматных задач из txt-задачников с генерацией соответствующих картинок.
