import os
import dotenv
from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser


dotenv.load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=API_KEY,
    temperature=0
)



class ExerciseResponse(BaseModel):
    exercises: List[str] = Field(description="список вправ для досягнення мети")


parser1 = PydanticOutputParser(pydantic_object=ExerciseResponse)
instructions1 = parser1.get_format_instructions()

prompt1 = PromptTemplate.from_template(
    """
Ти — професійний фітнес-тренер.
На основі мети тренування згенеруй список вправ.

### МЕТА
{goal}

### ФОРМАТ ВІДПОВІДІ
{instructions}
""",
    partial_variables={"instructions": instructions1}
)

chain_exercises = prompt1 | llm | parser1


class WorkoutPlan(BaseModel):
    plan: List[str] = Field(description="детальний план тренувань на тиждень")


parser2 = PydanticOutputParser(pydantic_object=WorkoutPlan)
instructions2 = parser2.get_format_instructions()

prompt2 = PromptTemplate.from_template(
    """
Ти — персональний тренер.
Створи персональний тижневий план тренувань.

### СПИСОК ВПРАВ
{exercises}

### РІВЕНЬ ПІДГОТОВКИ
{level}

### ЧАС НА ТИЖДЕНЬ (в годинах)
{hours}

Розбий план по днях (Понеділок – Неділя).

### ФОРМАТ ВІДПОВІДІ
{instructions}
""",
    partial_variables={"instructions": instructions2}
)

chain_plan = prompt2 | llm | parser2




print("\nPERSONAL FITNESS AI\n")

goal = input("Введіть мету (схуднення / набір м’язів / витривалість тощо): ")
level = input("Введіть рівень (низький / середній / професіонал): ")
hours = input("Скільки годин на тиждень ви можете тренуватись?: ")

print("\n🔹 Генеруємо вправи...")

exercise_result = chain_exercises.invoke({
    "goal": goal
})

print("\nСписок вправ:")
for ex in exercise_result.exercises:
    print("•", ex)

print("\nГенеруємо персональний план...")

plan_result = chain_plan.invoke({
    "exercises": exercise_result.exercises,
    "level": level,
    "hours": hours
})

print("\n Ваш тижневий план:")
for day in plan_result.plan:
    print(day)
