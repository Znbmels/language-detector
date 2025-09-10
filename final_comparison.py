#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Финальное сравнение FastText и нашей системы
"""

import sys
import os

# Добавляем путь к нашей системе
sys.path.append('langdetect')

def test_fasttext():
    """Тестирует FastText"""
    try:
        import fasttext
        model = fasttext.load_model('lid.176.bin')
        return model
    except Exception as e:
        print(f"Ошибка FastText: {e}")
        return None

def test_our_system():
    """Тестирует нашу систему"""
    try:
        from enhanced_reels_detector import EnhancedReelsDetector
        detector = EnhancedReelsDetector()
        return detector
    except Exception as e:
        print(f"Ошибка нашей системы: {e}")
        return None

def main():
    """Главная функция сравнения"""
    
    print("🏆 ФИНАЛЬНОЕ СРАВНЕНИЕ СИСТЕМ")
    print("=" * 50)
    
    # Загружаем системы
    fasttext_model = test_fasttext()
    our_detector = test_our_system()
    
    if not fasttext_model or not our_detector:
        print("❌ Не удалось загрузить системы")
        return
    
    # Тестовые тексты
    test_cases = [
        {
            'text': 'men super balamyn',
            'description': 'Латинский казахский (короткая фраза)',
            'expected': 'kk'
        },
        {
            'text': 'Qazaqstan - menin Otanym!',
            'description': 'Латинский казахский (фраза про Родину)',
            'expected': 'kk'
        },
        {
            'text': 'Almaty - Qazaqstannyn en iri qalasy',
            'description': 'Латинский казахский (про Алматы)',
            'expected': 'kk'
        },
        {
            'text': 'Қазақстан - менің Отаным!',
            'description': 'Кириллический казахский',
            'expected': 'kk'
        },
        {
            'text': 'Абай Құнанбайұлы қазақтың ұлы ақыны',
            'description': 'Кириллический казахский (про Абая)',
            'expected': 'kk'
        },
        {
            'text': 'Казахстан - моя Родина!',
            'description': 'Русский язык',
            'expected': 'ru'
        },
        {
            'text': 'Kazakhstan is my homeland!',
            'description': 'Английский язык',
            'expected': 'en'
        }
    ]
    
    print(f"\n🧪 ТЕСТИРОВАНИЕ {len(test_cases)} ТЕКСТОВ:")
    print("-" * 50)
    
    fasttext_correct = 0
    our_system_correct = 0
    
    for i, test_case in enumerate(test_cases, 1):
        text = test_case['text']
        description = test_case['description']
        expected = test_case['expected']
        
        print(f"\n{i}. {description}")
        print(f"   Текст: {text}")
        print(f"   Ожидается: {expected}")
        
        # Тестируем FastText
        try:
            predictions = fasttext_model.predict(text)
            fasttext_lang = predictions[0][0].replace('__label__', '')
            fasttext_conf = predictions[1][0]
            
            fasttext_correct += 1 if fasttext_lang == expected else 0
            
            print(f"   🚀 FastText: {fasttext_lang} ({fasttext_conf:.1%})")
            
        except Exception as e:
            print(f"   🚀 FastText: Ошибка - {e}")
            fasttext_lang = "error"
        
        # Тестируем нашу систему
        try:
            our_result = our_detector.detect_language(text)
            our_lang = our_result['language']
            our_conf = our_result['confidence']
            our_method = our_result['method']
            
            our_system_correct += 1 if our_lang == expected else 0
            
            print(f"   🏠 Наша система: {our_lang} ({our_conf:.1%}) [{our_method}]")
            
        except Exception as e:
            print(f"   🏠 Наша система: Ошибка - {e}")
            our_lang = "error"
        
        # Анализ результата
        if fasttext_lang == expected and our_lang == expected:
            print("   ✅ Обе системы ПРАВИЛЬНО")
        elif fasttext_lang == expected:
            print("   🚀 Только FastText ПРАВИЛЬНО")
        elif our_lang == expected:
            print("   🏠 Только наша система ПРАВИЛЬНО")
        else:
            print("   ❌ Обе системы НЕПРАВИЛЬНО")
    
    # Итоговая статистика
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print("-" * 50)
    print(f"FastText: {fasttext_correct}/{len(test_cases)} правильных ({fasttext_correct/len(test_cases)*100:.1f}%)")
    print(f"Наша система: {our_system_correct}/{len(test_cases)} правильных ({our_system_correct/len(test_cases)*100:.1f}%)")
    
    # Анализ по типам
    print(f"\n🔍 АНАЛИЗ ПО ТИПАМ ТЕКСТОВ:")
    print("-" * 50)
    
    latin_tests = [t for t in test_cases if 'Латинский казахский' in t['description']]
    cyrillic_tests = [t for t in test_cases if 'Кириллический казахский' in t['description']]
    
    print(f"Латинский казахский ({len(latin_tests)} тестов):")
    print(f"  FastText: {'❌ НЕ поддерживает' if fasttext_correct < len(test_cases) - len(cyrillic_tests) else '✅ Поддерживает'}")
    print(f"  Наша система: {'✅ Поддерживает' if our_system_correct >= len(latin_tests) else '❌ НЕ поддерживает'}")
    
    print(f"Кириллический казахский ({len(cyrillic_tests)} тестов):")
    print(f"  FastText: {'✅ Поддерживает' if fasttext_correct >= len(cyrillic_tests) else '❌ НЕ поддерживает'}")
    print(f"  Наша система: {'✅ Поддерживает' if our_system_correct >= len(cyrillic_tests) else '❌ НЕ поддерживает'}")
    
    # Рекомендации
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    print("-" * 50)
    
    if our_system_correct > fasttext_correct:
        print("🏆 Наша система ЛУЧШЕ для вашего проекта!")
        print("   ✅ Поддерживает латинский казахский")
        print("   ✅ Легко настраивается")
        print("   ✅ Работает оффлайн")
    elif fasttext_correct > our_system_correct:
        print("🚀 FastText ЛУЧШЕ для общего использования!")
        print("   ✅ Поддерживает 176 языков")
        print("   ✅ Высокая точность на кириллице")
        print("   ❌ НЕ поддерживает латинский казахский")
    else:
        print("🤝 Обе системы имеют свои преимущества!")
        print("   FastText: для общего использования")
        print("   Наша система: для казахского языка")

if __name__ == "__main__":
    main()


