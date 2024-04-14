init_methods = {
    'text_generating': 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
    'text_generating_async': 'https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync',
    'tokenize': 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize',
    'tokenize_completion': 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion',
    'embed_url': 'https://llm.api.cloud.yandex.net/foundationModels/v1/textEmbedding'
}

init_models = {
    'yandexgpt': 'Yandex GPT',
    'yandexgpt-lite': 'Yandex GPT Lite',
    'summarization': 'Суммаризация',
    'edu_test': 'Yandex DataSphere',
}

# текст в речь
# https://yandex.cloud/ru/docs/speechkit/tts/
# разметка речи https://yandex.cloud/ru/docs/speechkit/tts/markup/tts-markup
# https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize

# речь в текст
# https://yandex.cloud/ru/docs/speechkit/stt/api/request-api
# https://stt.api.cloud.yandex.net/speech/v1/stt:recognize