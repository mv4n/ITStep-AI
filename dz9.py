import os
import dotenv
from langchain_google_genai import GoogleGenerativeAI

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = GoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=api_key,
    temperature=0.7
)

with open(r"data\lesson9\return_policy.txt", "r", encoding="utf-8") as file:
    policy_text = file.read()

history = f"""Instruction:
Ти чат-бот служби підтримки.
Відповідай ТІЛЬКИ використовуючи правила повернення товару нижче.
Якщо питання не стосується повернення — скажи, що не можеш відповісти.

Правила повернення:
{policy_text}
"""

print("Чат-бот з питань повернення товару")
print("Для завершення — порожній рядок\n")

while True:
    user_input = input("Human: ").strip()

    if user_input == "":
        break

    history += f"\nHuman: {user_input}\nAI:"

    response = llm.invoke(history)
    history += f" {response}"

    print("AI:", response)

print("\nПовний діалог\n")
print(history)
