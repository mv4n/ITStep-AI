# LLM

# завантаження api key як змінну середовища
# import os
# import dotenv
#
#
# # завантаження данних з файлу .env
# dotenv.load_dotenv()
#
# # caм api key
# api_key = os.getenv('GEMINI_API_KEY')
#
# # сама модель LMM
# import langchain
# from langchain_google_genai import GoogleGenerativeAI
#
# # root /
# #    - langchain.py
# #    - lang...
#
#
# #
# # # запуск моделі
# # response = llm.invoke('Привіт, що таке LLM?')
# # print(response)
#
# # параметри креативності
#
# # створення моделі
# llm = GoogleGenerativeAI(
#     model='gemini-2.5-flash-lite', # назва моделі
#     api_key=api_key,
#     top_k=10, # вибрати випадково наступне слово з 10 з найбільшою ймовірністю
#     top_p=0.8, # залишити ті слова, сума ймовірностей яких не менше 80%, та вибрати серед них
#     temperature=1.5 # вища температура -- відсотки стають більш однаковими
# )

# temperature
# 0 - 0.3   -- низька креативність(відповіді як по методичці)
# 0.7 - 1.2 -- середня креативність(відповідає як людина)
# 1.5 - 1.7 -- висока креативність(вигадає щось цікаво або збреше)
# >2        -- випадкові слова



# Практична робота
# import os
# import dotenv
# from langchain_google_genai import GoogleGenerativeAI
# dotenv.load_dotenv()
#
# api_key = os.getenv('GEMINI_API_KEY')
#
#
#
# llm = GoogleGenerativeAI(
#     model='gemini-2.5-flash-lite',
#     api_key=api_key,
#     temperature=1
# )
#
# user_input = input('Питання: ')
# comand = 'дай відповідь один словом '
#
# response = llm.invoke(f"{user_input}, {comand}")
# print(response)




# import os
# import dotenv
# from langchain_google_genai import GoogleGenerativeAI
# dotenv.load_dotenv()
#
# api_key = os.getenv('GEMINI_API_KEY')
#
#
#
# llm = GoogleGenerativeAI(
#     model='gemini-2.5-flash-lite',
#     api_key=api_key,
#     temperature=1
# )
#
# with open('data/lesson9/rules.txt', 'r', encoding='utf-8') as file:
#     rules = file.read()
#
# user_question = input("enter question: ")
#
# response = llm.invoke(f'{rules} Вопрос - {user_question} Дай відповідь тільки по правилам')
#
# print(response)





import os
import dotenv
from langchain_google_genai import GoogleGenerativeAI
dotenv.load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')



llm = GoogleGenerativeAI(
    model='gemini-2.5-flash-lite',
    api_key=api_key,
    temperature=1
)


history = 'Відповідай як Джекі Чан'

while True:
    user_input = input('Ваше питання - ')
    history += f'\n Human: {user_input}'


    response = llm.invoke(history)
    history += f'\n AI: {response}'
    print(response)




# Створіть найпростіший чат бот. Напишіть моделі якого персонажа вона повинна вдавати(відомий актор, персонаж кіно\книги, тощо).
# Реалізуйте двома способами:
# 1. Модель отримує інструкцію в якому стилі відповідати та нове повідомлення.
# 2. Модель отримує інструкцію та історію попередніх повідомлень як від користувача, так і її власні відповіді у форматі
# Instruction: ….
# Human: massage1
# AI: message2
# Human: massage3
# AI: message4
# Human: massage5
# AI:


