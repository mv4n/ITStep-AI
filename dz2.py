import os
import dotenv
from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage
)
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser



dotenv.load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=API_KEY,
    temperature=0
)


class SummarySchema(BaseModel):
    summary: str = Field(description="детальний підсумок всієї розмови в кількох реченнях")

summary_parser = PydanticOutputParser(pydantic_object=SummarySchema)
summary_instructions = summary_parser.get_format_instructions()

summary_prompt = PromptTemplate.from_template(
"""
Ти — модель для стискання історії чату.
Твоя задача — підсумувати розмову в декілька речень,
зберігаючи ЯКОМОГА БІЛЬШЕ деталей:
імена, факти, питання, відповіді, наміри користувача.

### ПОВІДОМЛЕННЯ
{chat_history}

### ФОРМАТ
{instructions}
""",
partial_variables={"instructions": summary_instructions}
)

summary_chain = summary_prompt | llm | summary_parser


def summarize_messages(messages: List[BaseMessage]) -> List[BaseMessage]:
    """
    Якщо повідомлень більше 4 — стискаємо історію в summary
    SystemMessage не чіпаємо і не передаємо в summary
    """

    if len(messages) <= 4:
        return messages

    system_message = messages[0]

    history = messages[1:]

    history_text = ""
    for m in history:
        role = "User" if isinstance(m, HumanMessage) else "AI"
        history_text += f"{role}: {m.content}\n"

    summary = summary_chain.invoke({"chat_history": history_text})

    new_messages = [
        system_message,
        AIMessage(f"SUMMARY OF PREVIOUS CONVERSATION: {summary.summary}")
    ]

    return new_messages



messages: List[BaseMessage] = [
    SystemMessage("""
    Ти — ввічливий розумний чат-бот.
    Відповідай чітко, по суті і враховуй всю історію діалогу.
    """)
]

print("\nSmart Chat with LLM Memory\n")

while True:
    user_input = input("Ви: ")

    if user_input == "":
        break

    messages.append(HumanMessage(user_input))

    messages = summarize_messages(messages)

    response = llm.invoke(messages)
    messages.append(response)

    print(f"\nAI: {response.content}")

    print("\n--- CURRENT MEMORY ---")
    for m in messages:
        print(repr(m))
    print("---------------------\n")
