# Инструкция по установке MyLangDetect

## Вариант 1: Установка через pip (рекомендуется)

```bash
# Перейдите в папку с библиотекой
cd mylangdetect

# Установите в режиме разработки
pip install -e .

# Или установите обычным способом
pip install .
```

## Вариант 2: Прямое использование

Если у вас нет возможности установить через pip, можете использовать библиотеку напрямую:

```bash
# Скопируйте папку mylangdetect в ваш проект
cp -r mylangdetect /path/to/your/project/

# В вашем коде импортируйте напрямую
from mylangdetect.detector import TfidfLangID
```

## Требования

Убедитесь, что у вас установлены зависимости:

```bash
pip install scikit-learn numpy joblib
```

## Проверка установки

```python
from mylangdetect import detect_language

# Простой тест
result = detect_language("Hello world")
print(result)  # Должно вывести "EN"
```

## Использование в проекте

```python
# Простое использование
from mylangdetect import detect_language, detect_language_detailed

# Определить язык
language = detect_language("Привет мир")
print(language)  # "RU"

# С детальной информацией
result = detect_language_detailed("Hello world")
print(result)
# {
#     "language": "EN",
#     "confidence": 0.95,
#     "top_k": [("EN", 0.95), ("FR", 0.03), ...]
# }
```

## Структура библиотеки

```
mylangdetect/
├── __init__.py          # Основной API
├── detector.py          # Класс TfidfLangID
├── model/               # Предобученная модель
│   └── tfidf_langid.joblib
├── setup.py            # Для установки через pip
├── requirements.txt    # Зависимости
├── README.md          # Документация
├── example_usage.py   # Примеры использования
└── test_library.py    # Тесты
```

## Поддержка

Если у вас возникли проблемы с установкой или использованием, проверьте:

1. Версию Python (требуется 3.7+)
2. Установлены ли все зависимости
3. Правильно ли указан путь к библиотеке

Для получения помощи создайте issue в репозитории проекта.
