#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# Добавляем путь к модулю langdetect
sys.path.append('langdetect')

import langdetect as ld

def test_language_detection():
    print("=== Тестирование определения языка ===\n")
    
    # Создаем профили
    print("Создание языковых профилей...")
    profiles = ld.create_languages_profiles()
    print(f"Создано профилей: {len(profiles)}\n")
    
    # Тестовые тексты
    test_cases = [
        {
            'expected': 'kk',
            'text': "Қазақстан Республикасы Орталық Азияда орналасқан мемлекет.",
            'description': "Короткий казахский текст"
        },
        {
            'expected': 'kk', 
            'text': "Абай Құнанбайұлы қазақтың ұлы ақыны, ағартушысы, композиторы, философы және аудармашысы болып табылады.",
            'description': "Средний казахский текст"
        },
        {
            'expected': 'kk',
            'text': "Наурыз қазақтардың ұлттық мерекесі болып табылады және жаңа жыл мерекесі ретінде тойланады. Наурыз 22 наурызда тойланады және бұл мереке көктемнің келуін, табиғаттың жаңаруын білдіреді.",
            'description': "Длинный казахский текст"
        },
        {
            'expected': 'ru',
            'text': "Казахстан - государство, расположенное в Центральной Азии.",
            'description': "Короткий русский текст"
        },
        {
            'expected': 'ru',
            'text': "Абай Кунанбаев - великий казахский поэт, просветитель, композитор, философ и переводчик.",
            'description': "Средний русский текст"
        },
        {
            'expected': 'ru',
            'text': "Наурыз является национальным праздником казахов и отмечается как праздник нового года. Наурыз отмечается 22 марта и этот праздник символизирует приход весны, обновление природы.",
            'description': "Длинный русский текст"
        },
        {
            'expected': 'en',
            'text': "Kazakhstan is a country located in Central Asia.",
            'description': "Английский текст"
        }
    ]
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        expected = test_case['expected']
        text = test_case['text']
        description = test_case['description']
        
        print(f"Тест {i}: {description}")
        print(f"Текст: {text[:60]}{'...' if len(text) > 60 else ''}")
        print(f"Ожидаемый язык: {expected}")
        
        try:
            result = ld.detect_language(text, profiles)
            result_list = list(result)
            
            if result_list:
                detected_lang = result_list[0][0]
                confidence = result_list[0][1]
                
                print(f"Определенный язык: {detected_lang} (уверенность: {confidence:.3f})")
                
                if detected_lang == expected:
                    print("✓ ПРАВИЛЬНО")
                    correct_predictions += 1
                else:
                    print("✗ НЕПРАВИЛЬНО")
                
                print(f"Все результаты: {result_list[:3]}")
            else:
                print("✗ НЕ УДАЛОСЬ ОПРЕДЕЛИТЬ ЯЗЫК")
                
        except Exception as e:
            print(f"✗ ОШИБКА: {e}")
        
        print("-" * 60)
    
    print(f"\n=== ИТОГИ ===")
    print(f"Правильных предсказаний: {correct_predictions}/{total_tests}")
    print(f"Точность: {correct_predictions/total_tests*100:.1f}%")
    
    # Тест на смешанные тексты
    print(f"\n=== Тест на смешанные тексты ===")
    mixed_texts = [
        "Қазақстан Kazakhstan Казахстан",
        "Hello Сәлем Привет",
        "Абай Abay Абай"
    ]
    
    for text in mixed_texts:
        print(f"\nСмешанный текст: {text}")
        try:
            result = ld.detect_language(text, profiles)
            result_list = list(result)
            print(f"Результат: {result_list[:3]}")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    test_language_detection()
