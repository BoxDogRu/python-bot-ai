GPT_IAM_TOKEN = ''
FOLDER_ID = ''
GPT_MODEL = 'yandexgpt-lite'

# TODO. Напиши системный промт, который объяснит нейросети, как правильно писать сценарий вместе с пользователем
SYSTEM_PROMPT = ("Ты пишешь историю вместе с человеком. "
    "Историю вы пишете по очереди. Начинает человек, а ты продолжаешь. "
    "Если это уместно, ты можешь добавлять в историю диалог между персонажами. "
    "Диалоги пиши с новой строки и отделяй тире. "
    "Не пиши никакого пояснительного текста в начале, а просто логично продолжай историю."
)

# Дополнительная версия.
# Ты бот сценарист, отвечай кратко и не разделяй текст на сцены.
# Ты пишешь историю вместе с человеком, историю вы пишете по очереди.
# Не добавляй никакого пояснительного текста, а просто логически продолжай историю.

CONTINUE_STORY = 'Продолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = 'Напиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'