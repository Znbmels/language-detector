#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пример использования библиотеки MyLangDetect.

Этот файл демонстрирует различные способы использования библиотеки
для определения языка текста.
"""

import sys
import os

# Добавляем текущую директорию в путь для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from detector import TfidfLangID

def example_simple_usage():
    """Простой пример использования."""
    print("🔍 ПРОСТОЙ ПРИМЕР ИСПОЛЬЗОВАНИЯ")
    print("=" * 40)
    
    # Загружаем модель
    detector = TfidfLangID.load_from_package()
    
    # Тестовые тексты
    texts = [
        "Hello, how are you today?",
        "Привет, как дела?",
        "Сәлем, қалайсың?",
        "Hola, ¿cómo estás?",
        "Bonjour, comment allez-vous?",
        "Hallo, wie geht es dir?",
        "Ciao, come stai?",
        "Olá, como você está?",
        "Здравствуйте, как поживаете?",
        "مرحبا، كيف حالك؟"
    ]
    
    print("📝 Определение языка для различных текстов:")
    print()
    
    for text in texts:
        result = detector.predict_one(text)
        language = result['language']
        confidence = result['confidence']
        
        print(f"Текст: {text}")
        print(f"Язык: {language.upper()} (уверенность: {confidence:.1%})")
        print("-" * 50)

def example_detailed_analysis():
    """Пример детального анализа."""
    print("\n🔬 ДЕТАЛЬНЫЙ АНАЛИЗ")
    print("=" * 40)
    
    detector = TfidfLangID.load_from_package()
    
    # Анализируем текст с получением топ-5 результатов
    text = "This is a sample text for language detection analysis."
    result = detector.predict_one(text, top_k=5)
    
    print(f"Анализируемый текст: {text}")
    print(f"Определенный язык: {result['language'].upper()}")
    print(f"Уверенность: {result['confidence']:.2%}")
    print()
    print("Топ-5 наиболее вероятных языков:")
    
    for i, (lang, conf) in enumerate(result['top_k'], 1):
        print(f"  {i}. {lang.upper()}: {conf:.2%}")

def example_batch_processing():
    """Пример пакетной обработки."""
    print("\n📦 ПАКЕТНАЯ ОБРАБОТКА")
    print("=" * 40)
    
    detector = TfidfLangID.load_from_package()
    
    # Список текстов для обработки
    texts = [
        "Good morning!",
        "Доброе утро!",
        "Қайырлы таң!",
        "Buenos días!",
        "Bonjour!",
        "Guten Morgen!",
        "Buongiorno!",
        "Bom dia!",
        "Доброго ранку!",
        "صباح الخير!"
    ]
    
    # Обрабатываем все тексты сразу
    results = detector.predict(texts)
    
    print("Результаты пакетной обработки:")
    print()
    
    for text, result in zip(texts, results):
        print(f"'{text}' -> {result['language'].upper()} ({result['confidence']:.1%})")

def example_supported_languages():
    """Пример получения списка поддерживаемых языков."""
    print("\n🌍 ПОДДЕРЖИВАЕМЫЕ ЯЗЫКИ")
    print("=" * 40)
    
    detector = TfidfLangID.load_from_package()
    
    if detector.le is not None:
        languages = sorted(detector.le.classes_.tolist())
        print(f"Всего поддерживается языков: {len(languages)}")
        print()
        print("Список языков:")
        
        # Выводим по 10 языков в строке
        for i in range(0, len(languages), 10):
            chunk = languages[i:i+10]
            print("  " + " ".join(f"{lang.upper():>3}" for lang in chunk))

def example_confidence_analysis():
    """Пример анализа уверенности модели."""
    print("\n📊 АНАЛИЗ УВЕРЕННОСТИ МОДЕЛИ")
    print("=" * 40)
    
    detector = TfidfLangID.load_from_package()
    
    # Тестируем на текстах разной длины
    test_cases = [
        ("Hi", "Очень короткий текст"),
        ("Hello world", "Короткий текст"),
        ("This is a longer text that should provide more context for language detection.", "Средний текст"),
        ("This is a much longer text that contains multiple sentences and should provide excellent context for accurate language detection. The model should be very confident about this prediction.", "Длинный текст")
    ]
    
    print("Анализ уверенности в зависимости от длины текста:")
    print()
    
    for text, description in test_cases:
        result = detector.predict_one(text, top_k=3)
        confidence = result['confidence']
        
        print(f"{description}:")
        print(f"  Текст: '{text}'")
        print(f"  Язык: {result['language'].upper()}")
        print(f"  Уверенность: {confidence:.2%}")
        
        # Показываем топ-3
        print("  Топ-3:")
        for i, (lang, conf) in enumerate(result['top_k'], 1):
            print(f"    {i}. {lang.upper()}: {conf:.2%}")
        print()

def main():
    """Основная функция с примерами."""
    print("🚀 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ MYLANGDETECT")
    print("=" * 50)
    
    try:
        example_simple_usage()
        example_detailed_analysis()
        example_batch_processing()
        example_supported_languages()
        example_confidence_analysis()
        
        print("\n" + "=" * 50)
        print("✅ Все примеры выполнены успешно!")
        print("📚 Библиотека готова к использованию в ваших проектах")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении примеров: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
