# LLM Классификатор обращений пользователей

## Описание

Этот проект - пайплайн обработки пользовательских обращений с использованием LLM.

Скрипт проходит по списку пользовательских обращений, для каждого обращения обращается к языковой модели и:

* классифицирует обращение по категориям: Support, Sales, Bug;
* определяет эмоциональную окраску текста: positive / neutral / negative;
* сохраняет результат в формате JSON.

В проекте используется локальная LLM через Ollama (`llama3`).

---

## Установка и запуск

### 1. Установка Ollama

Скачать и установить Ollama:
[https://ollama.com](https://ollama.com)

Загрузить модель:

```bash
ollama pull llama3
```
### 2. Клонирование репозитория

```bash
git clone https://github.com/avmaslakova/llm_classifier.git
cd llm_classifier
```

### 3. Создание виртуального окружения

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# MacOS/Linux
source venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Запуск

```bash

python main.py
```

---

## Возможные улучшения

* few-shot примеры в prompt
* batch / async обработка
* метрики качества (accuracy, F1)
* rule-based fallback

---
