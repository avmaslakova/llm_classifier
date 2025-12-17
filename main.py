import json
import time
import random
from typing import Literal

from pydantic import BaseModel

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class ClassificationResult(BaseModel):
  category: Literal["Support", "Bug", "Feedback"]
  sentiment: Literal["positive", "neutral", "negative"]


INPUT_PATH = "input.json"
OUTPUT_PATH = "output.json"


def build_chain():
  llm = ChatOllama(model="llama3", temperature=0)

  parser = PydanticOutputParser(pydantic_object=ClassificationResult)

  prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Ты — строгий классификатор пользовательских обращений сервиса доставки еды. Если сомневаешься - выбирай наиболее вероятный класс"
            ),
            (
                "human",
                """
                Определи класс и тональность обращения.

                Классы:
                - Support — вопросы, доставка, возвраты, аккаунт
                - Bug — технические проблемы, ошибки приложения, сбои приложение не работает
                - Feedback — отзывы, жалобы, благодарности

                Определи тональность обращения: positive / neutral / negative

                Пример:
                Текст: "Приложение не открывается"
                Ответ: "id":"1", "text":"Приложение не открывается", "category":"Bug","sentiment":"negative"

                Текст: "Спасибо, курьер был вежлив"
                Ответ: "id":"2", "text":"Спасибо, курьер был вежлив", "category":"Feedback","sentiment":"positive"

                Формат ответа: {format_instructions}

                Текст обращения:
                {text}
                """
            )
        ]
    )


  chain = (prompt | llm | parser)

  return chain


def safe_invoke(chain, text, retries=3):
    for attempt in range(retries):
        try:
            return chain.invoke(
                {
                    "text": text,
                    "format_instructions": chain.steps[-1].get_format_instructions(),
                }
            )
        except Exception as e:
            print(f"Попытка {attempt + 1}: ошибка модели или парсинга: {e}")
            time.sleep(2 ** attempt + random.random())
    raise RuntimeError("LLM is not available")


def main():
  with open(INPUT_PATH, "r") as f:
    data = json.load(f)

  chain = build_chain()
  results = []

  for item in data:
    try:
      response = safe_invoke(chain, item["text"])

      result = {
        "id": item["id"],
        "text": item["text"],
        "category": response.category,
        "sentiment": response.sentiment
      }

    except Exception as e:
      result = {
        "id": item["id"],
        "text": item["text"],
        "category": "Support",
        "sentiment": "neutral",
        "error": str(e)
      }

    results.append(result)
    time.sleep(0.3)

  with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
  main()

