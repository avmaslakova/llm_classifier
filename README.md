# LLM классификатор обращений пользователей

Простой пайплайн для классификации пользовательских обращений с использованием LLM через LangChain.  

---

## Возможности

- Классификация на 3 категории: `Support`, `Bug`, `Feedback`  
- Определение эмоциональной окраски: `positive`, `neutral`, `negative`  
- Обработка ошибок модели и повторные попытки  
- Результат сохраняется в `data/output.json`

---

## Установка

1. Создать виртуальное окружение и активировать его:

```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
2. Установить зависимости:
```
pip install -r requirements.txt
```
---

## Запуск
```
python src/main.py
```
