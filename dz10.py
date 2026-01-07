from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
import dotenv

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = GoogleGenerativeAI(
    model='gemini-2.5-flash-lite',
    api_key=api_key,
)

prompt_zero_shot = PromptTemplate.from_template("""
Ти – викладач та методист. Твоя задача – створити детальний план навчального курсу
для певної цільової аудиторії. План має включати:

1. Кількість уроків/модулів
2. Назви уроків
3. Короткий опис кожного уроку
4. Рівень складності та підходи до навчання, враховуючи цільову аудиторію

Тема курсу: {topic}
Цільова аудиторія: {audience}
""")

chain_zero_shot = prompt_zero_shot | llm

topic = input("Тема курсу: ")
audience = input("Цільова аудиторія: ")

response_zero_shot = chain_zero_shot.invoke({
    "topic": topic,
    "audience": audience
})



print("Zero-Shot")
print(response_zero_shot)


# Few-Shot
prompt_few_shot = PromptTemplate.from_template("""
Ти – викладач та методист. Твоя задача – створити детальний план навчального курсу
для певної цільової аудиторії. План має включати:

1. Кількість уроків/модулів
2. Назви уроків
3. Короткий опис кожного уроку
4. Рівень складності та підходи до навчання, враховуючи цільову аудиторію

### ПРИКЛАД
Тема курсу: Основи Python
Цільова аудиторія: Початківці
План курсу:
1. Вступ до програмування
   - Короткий опис: Що таке програмування, установка Python, перша програма "Hello, World!"
   - Рівень: Початковий
2. Змінні та типи даних
   - Короткий опис: Основні типи даних, операції над ними
   - Рівень: Початковий
3. Умовні конструкції
   - Короткий опис: if, else, elif, приклади застосування
   - Рівень: Початковий
4. Цикли
   - Короткий опис: for, while, break/continue
   - Рівень: Початковий
5. Функції
   - Короткий опис: Створення та виклик функцій, параметри та return
   - Рівень: Початковий

### ВАШЕ ЗАВДАННЯ
Тема курсу: {topic}
Цільова аудиторія: {audience}
План курсу:
""")

chain_few_shot = prompt_few_shot | llm

topic = input("Тема курсу: ")
audience = input("Цільова аудиторія: ")

response_few_shot = chain_few_shot.invoke({
    "topic": topic,
    "audience": audience
})

print("=== Few-Shot План курсу ===")
print(response_few_shot)
