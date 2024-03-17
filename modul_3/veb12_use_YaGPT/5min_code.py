# Базовые операции со строками

string1 = "hello"
string2 = "world1"
# TODO сложить длины двух строк
result = len(string1) + len(string2)
print(result)


string = "python"
# TODO из строки получить "yth" c помощью среза
result = string[1:4]
print(result)


word1 = "apple"
word2 = "banana"
# TODO сравнить длины двух слов и написать какое длиннее
if len(word1) > len(word2):
    print("apple is longer than banana")
else:
    print("banana is longer than apple")


string = "hello world"
# TODO разбить слова на список
result = string.split()
print(result)


word = "Python"
# TODO привести текст к нижнему регистру
result = word.lower()
print(result)


# TODO сделать валидацию ввода пользователя
MAX_LETTERS = 23
user_text = input('Введите текст для запроса в нейросеть')

if len(user_text) > MAX_LETTERS:
    print('Текст слишком длинный, введите текст короче')
else:
    print('Вопрос передан нейросети')
