from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Задача 1. Запустить в локальной среде
# Задача 2. Подобрать интересную модель https://huggingface.co/ai-forever/
# Задача 3. Поиграться с гиперпараметрами

# загружаем модели
# sberbank-ai/rugpt3small_based_on_gpt2
# sberbank-ai/rugpt3large_based_on_gpt2

model = GPT2LMHeadModel.from_pretrained("sberbank-ai/rugpt3large_based_on_gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("sberbank-ai/rugpt3large_based_on_gpt2")


def ask_GPT(promt):
    input_ids = tokenizer.encode(promt, return_tensors="pt")
    output = model.generate(input_ids,
                            max_length=70,
                            num_return_sequences=1,
                            repetition_penalty=2.0,
                            do_sample=True,
                            #top_k=50,
                            #top_p=0.95,
                            temperature=0.1)[0]
    rezult = tokenizer.decode(output)

    return rezult


print(ask_GPT('Математика - это'))

