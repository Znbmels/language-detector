# MyLangDetect

Быстрая библиотека для определения языка текста на базе TF‑IDF (символьные n‑граммы). В комплекте — готовая модель и CLI.

## Установка

```bash
pip install .
```

Требуется Python 3.7+. Зависимости (`scikit-learn`, `numpy`, `joblib`) подтянутся автоматически.

## Использование (Python)

```python
from mylangdetect import detect_language, detect_language_detailed

print(detect_language("Hello, world!"))              # 'EN'
print(detect_language("Привет, мир!"))               # 'RU'
print(detect_language_detailed("Сәлем дүние"))      # {'language': 'KK', 'confidence': ...}
```

## CLI

```bash
# Одна строка
mylang-detect "Hello, world!"

# Топ-3 предсказания в JSON
mylang-detect -k 3 -j "Привет, как дела?"

# Из файла
mylang-detect -f path/to/text.txt

# Список поддерживаемых языков
mylang-detect --list-langs
```

Если модель не вложена в пакет (см. размер >100MB), укажите путь к файлу модели через переменную окружения:

```bash
export MYLANGDETECT_MODEL_PATH=/absolute/path/to/tfidf_langid.joblib
```

## Что внутри
- Пакет: `mylangdetect/`
  - API: `__init__.py` — `detect_language`, `detect_language_detailed`, `TfidfLangID`
  - Модель: `mylangdetect/model/tfidf_langid.joblib`
  - CLI: `mylangdetect/cli.py` (команда `mylang-detect`)
- Пакетинг: `setup.py`, `MANIFEST.in`
- Если модель не в репозитории — см. `mylangdetect/model/README_MODEL.md`

## Быстрая проверка
```bash
python -c "from mylangdetect import detect_language as d; print(d('Bonjour'))"
# -> FR
```

## Лицензия
MIT (пример; при необходимости обновите файл лицензии).
