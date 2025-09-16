# MyLangDetect

Простая библиотека для определения языка текста с использованием предобученной TF-IDF модели и символьных n-грамм.

## Особенности

- 🚀 **Быстрая детекция** - использует оптимизированную TF-IDF модель
- 🌍 **55 языков** - поддерживает широкий спектр языков включая казахский
- 📦 **Простой API** - одна функция для детекции языка
- 🎯 **Высокая точность** - 99.1% точность на тестовых данных
- ⚡ **Готовая модель** - предобученная модель включена в пакет

## Поддерживаемые языки

Библиотека поддерживает 55 языков, включая:
- **EN** - Английский
- **RU** - Русский  
- **KK** - Казахский
- **DE** - Немецкий
- **FR** - Французский
- **ES** - Испанский
- **IT** - Итальянский
- **PT** - Португальский
- **AR** - Арабский
- **ZH** - Китайский
- **JA** - Японский
- **KO** - Корейский
- И многие другие...

## Установка

### Через pip (рекомендуется)

```bash
pip install .
```

### Прямое использование

```bash
# Скопируйте папку mylangdetect в ваш проект
cp -r mylangdetect /path/to/your/project/
```

## Быстрый старт

### Простое использование

```python
from mylangdetect import detect_language

# Определить язык
result = detect_language("Hello world")
print(result)  # "EN"

result = detect_language("Привет мир")
print(result)  # "RU"

result = detect_language("Сәлем дүние")
print(result)  # "KK"
```

### CLI-утилита

После установки доступна команда `mylang-detect`:

```bash
# Определить язык одной строки
mylang-detect "Hello, world!"

# Топ-3 предсказания в JSON
mylang-detect -k 3 -j "Привет, как дела?"

# Определение из файла
mylang-detect -f path/to/text.txt

# Список поддерживаемых языков
mylang-detect --list-langs

# Интерактивный режим
mylang-detect
```

### Детальная информация

```python
from mylangdetect import detect_language_detailed

result = detect_language_detailed("Hello world")
print(result)
# {
#     "language": "EN",
#     "confidence": 0.95,
#     "top_k": [("EN", 0.95), ("FR", 0.03), ("DE", 0.02)]
# }
```

### Продвинутое использование

```python
from mylangdetect import TfidfLangID

# Загрузить модель
detector = TfidfLangID.load_from_package()

# Предсказание для одного текста
result = detector.predict_one("Hello world", top_k=5)
print(f"Язык: {result['language']}")
print(f"Уверенность: {result['confidence']:.2%}")
print("Топ-5 результатов:")
for lang, conf in result['top_k']:
    print(f"  {lang}: {conf:.2%}")

# Предсказание для списка текстов
texts = ["Hello", "Привет", "Сәлем"]
results = detector.predict(texts)
for text, result in zip(texts, results):
    print(f"{text} -> {result['language']}")
```

### Получение списка поддерживаемых языков

```python
from mylangdetect import get_supported_languages

languages = get_supported_languages()
print(f"Поддерживается {len(languages)} языков:")
print(languages[:10])  # Первые 10 языков
```

## API Reference

### `detect_language(text, top_k=1)`

Определяет язык текста и возвращает код языка.

**Параметры:**
- `text` (str): Текст для анализа
- `top_k` (int): Количество топ-предсказаний (по умолчанию: 1)

**Возвращает:**
- `str`: Код языка (например, "EN", "RU", "KK")

### `detect_language_detailed(text, top_k=3)`

Определяет язык текста с детальной информацией.

**Параметры:**
- `text` (str): Текст для анализа  
- `top_k` (int): Количество топ-предсказаний (по умолчанию: 3)

**Возвращает:**
- `dict`: Словарь с ключами:
  - `language`: Код наиболее вероятного языка
  - `confidence`: Уровень уверенности (0.0 до 1.0)
  - `top_k`: Список кортежей (язык, уверенность)

### `TfidfLangID`

Основной класс для работы с моделью.

**Методы:**
- `load_from_package(model_name="tfidf_langid.joblib)`: Загрузить модель из пакета
- `predict_one(text, top_k=3)`: Предсказание для одного текста
- `predict(texts, top_k=3)`: Предсказание для списка текстов

### `get_supported_languages()`

Возвращает список поддерживаемых языков.

**Возвращает:**
- `list`: Список кодов языков

## Примеры использования

### Веб-приложение

```python
from flask import Flask, request, jsonify
from mylangdetect import detect_language_detailed

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = detect_language_detailed(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
```

### Обработка файлов

```python
from mylangdetect import detect_language
import os

def process_text_files(directory):
    results = {}
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                language = detect_language(text)
                results[filename] = language
    
    return results

# Использование
results = process_text_files('./documents')
for filename, language in results.items():
    print(f"{filename}: {language}")
```

## Технические детали

- **Модель**: TF-IDF с символьными n-граммами (1-5 символов)
- **Классификатор**: SVM с калибровкой вероятностей
- **Точность**: 99.1% на тестовых данных
- **Размер модели**: ~50MB
- **Время предсказания**: ~1-5ms на текст

## Требования

- Python 3.7+
- scikit-learn >= 1.0.0
- numpy >= 1.20.0
- joblib >= 1.0.0

## Лицензия

MIT License

## Поддержка

Если у вас есть вопросы или проблемы, создайте issue в репозитории проекта.
