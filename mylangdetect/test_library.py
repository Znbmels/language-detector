#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для проверки работы библиотеки MyLangDetect.
"""

import sys
import os

# Добавляем текущую директорию в путь для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Импортируем модули напрямую
from detector import TfidfLangID

def test_simple_api():
    """Тест простого API."""
    print("🧪 Тестирование простого API...")
    
    try:
        # Создаем простые функции для тестирования
        detector = TfidfLangID.load_from_package()
        
        def detect_language(text, top_k=1):
            result = detector.predict_one(text, top_k=top_k)
            return result['language']
        
        def detect_language_detailed(text, top_k=3):
            return detector.predict_one(text, top_k=top_k)
        
        def get_supported_languages():
            if detector.le is None:
                raise RuntimeError("Model not loaded properly")
            return sorted(detector.le.classes_.tolist())
        
        # Тест простой детекции
        test_texts = [
            ("Hello world", "EN"),
            ("Привет мир", "RU"), 
            ("Сәлем дүние", "KK"),
            ("Hola mundo", "ES"),
            ("Bonjour le monde", "FR"),
            ("Hallo Welt", "DE")
        ]
        
        print("📝 Тестирование detect_language():")
        for text, expected in test_texts:
            result = detect_language(text)
            status = "✅" if result == expected else "❌"
            print(f"  {status} '{text}' -> {result} (ожидалось: {expected})")
        
        # Тест детальной детекции
        print("\n📊 Тестирование detect_language_detailed():")
        result = detect_language_detailed("Hello world", top_k=3)
        print(f"  Результат: {result}")
        
        # Тест списка языков
        print("\n🌍 Поддерживаемые языки:")
        languages = get_supported_languages()
        print(f"  Всего языков: {len(languages)}")
        print(f"  Первые 10: {languages[:10]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в простом API: {e}")
        return False

def test_advanced_api():
    """Тест продвинутого API."""
    print("\n🔧 Тестирование продвинутого API...")
    
    try:
        # TfidfLangID уже импортирован в начале файла
        
        # Загрузка модели
        detector = TfidfLangID.load_from_package()
        print("✅ Модель загружена")
        
        # Тест предсказания для одного текста
        result = detector.predict_one("Hello world", top_k=5)
        print(f"📝 Результат для 'Hello world':")
        print(f"  Язык: {result['language']}")
        print(f"  Уверенность: {result['confidence']:.2%}")
        print("  Топ-5:")
        for i, (lang, conf) in enumerate(result['top_k'], 1):
            print(f"    {i}. {lang}: {conf:.2%}")
        
        # Тест предсказания для списка
        texts = ["Hello", "Привет", "Сәлем", "Hola", "Bonjour"]
        results = detector.predict(texts)
        print(f"\n📋 Результаты для списка текстов:")
        for text, result in zip(texts, results):
            print(f"  '{text}' -> {result['language']} ({result['confidence']:.1%})")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в продвинутом API: {e}")
        return False

def main():
    """Основная функция тестирования."""
    print("🚀 Запуск тестов библиотеки MyLangDetect")
    print("=" * 50)
    
    success = True
    
    # Тест простого API
    if not test_simple_api():
        success = False
    
    # Тест продвинутого API
    if not test_advanced_api():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Все тесты прошли успешно!")
        print("📦 Библиотека готова к использованию")
    else:
        print("❌ Некоторые тесты не прошли")
        sys.exit(1)

if __name__ == "__main__":
    main()
