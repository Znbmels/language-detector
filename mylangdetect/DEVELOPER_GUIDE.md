# Руководство для разработчика

## Быстрый старт

### 1. Установка

```bash
# Установите зависимости
pip install scikit-learn numpy joblib

# Установите библиотеку
pip install -e .
```

### 2. Базовое использование

```python
from mylangdetect import detect_language

# Простое определение языка
language = detect_language("Hello world")
print(language)  # "EN"
```

### 3. Продвинутое использование

```python
from mylangdetect import TfidfLangID

# Загрузить модель
detector = TfidfLangID.load_from_package()

# Детальный анализ
result = detector.predict_one("Hello world", top_k=5)
print(f"Язык: {result['language']}")
print(f"Уверенность: {result['confidence']:.2%}")

# Пакетная обработка
texts = ["Hello", "Привет", "Сәлем"]
results = detector.predict(texts)
for text, result in zip(texts, results):
    print(f"{text} -> {result['language']}")
```

## API Reference

### Основные функции

- `detect_language(text)` - возвращает код языка
- `detect_language_detailed(text)` - возвращает детальную информацию
- `get_supported_languages()` - список поддерживаемых языков

### Класс TfidfLangID

- `load_from_package()` - загрузить модель из пакета
- `predict_one(text, top_k=3)` - предсказание для одного текста
- `predict(texts, top_k=3)` - предсказание для списка текстов

## Поддерживаемые языки

Библиотека поддерживает 55 языков:
- EN, RU, KK, DE, FR, ES, IT, PT, AR, ZH, JA, KO и другие

## Особенности модели

- **Точность**: 99.1% на тестовых данных
- **Метод**: TF-IDF с символьными n-граммами (1-5 символов)
- **Классификатор**: SVM с калибровкой вероятностей
- **Время предсказания**: ~1-5ms на текст

## Рекомендации

1. **Длина текста**: Для лучшей точности используйте тексты длиннее 20 символов
2. **Уверенность**: Проверяйте confidence score для критичных применений
3. **Пакетная обработка**: Используйте `predict()` для обработки множества текстов

## Примеры интеграции

### Flask API

```python
from flask import Flask, request, jsonify
from mylangdetect import detect_language_detailed

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    text = data.get('text', '')
    result = detect_language_detailed(text)
    return jsonify(result)
```

### Обработка файлов

```python
import os
from mylangdetect import detect_language

def process_directory(directory):
    results = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as f:
                text = f.read()
                results[filename] = detect_language(text)
    return results
```

## Тестирование

```bash
# Запустить тесты
python test_library.py

# Запустить примеры
python example_usage.py
```
