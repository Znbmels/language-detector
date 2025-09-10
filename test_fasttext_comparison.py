#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Сравнение FastText и нашей системы определения языка
"""

import sys
import os

# Добавляем путь к нашей системе
sys.path.append('langdetect')

def test_fasttext():
    """Тестирует FastText"""
    try:
        import fasttext
        
        # Загружаем модель
        print("Загрузка FastText модели...")
        model = fasttext.load_model('lid.176.bin')
        print("✅ FastText модель загружена")
        
        return model
    except Exception as e:
        print(f"❌ Ошибка загрузки FastText: {e}")
        return None

def test_our_system():
    """Тестирует нашу систему"""
    try:
        import langdetect as ld
        from enhanced_reels_detector import EnhancedReelsDetector
        
        print("Загрузка нашей системы...")
        detector = EnhancedReelsDetector()
        print("✅ Наша система загружена")
        
        return detector
    except Exception as e:
        print(f"❌ Ошибка загрузки нашей системы: {e}")
        return None

def compare_systems():
    """Сравнивает обе системы"""
    
    print("🔬 СРАВНЕНИЕ СИСТЕМ ОПРЕДЕЛЕНИЯ ЯЗЫКА")
    print("=" * 60)
    
    # Загружаем системы
    fasttext_model = test_fasttext()
    our_detector = test_our_system()
    
    if not fasttext_model or not our_detector:
        print("❌ Не удалось загрузить одну из систем")
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
        },
        {
            'text': 'Қазақстан Kazakhstan Казахстан',
            'description': 'Смешанный текст',
            'expected': 'kk'
        }
    ]
    
    print(f"\n🧪 ТЕСТИРОВАНИЕ {len(test_cases)} ТЕКСТОВ:")
    print("-" * 60)
    
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
        fasttext_lang = None
        fasttext_conf = 0
        try:
            fasttext_predictions = fasttext_model.predict(text, k=3)
            fasttext_lang = fasttext_predictions[0][0].replace('__label__', '')
            fasttext_conf = fasttext_predictions[1][0]
            
            fasttext_correct += 1 if fasttext_lang == expected else 0
            
            print(f"   🚀 FastText: {fasttext_lang} ({fasttext_conf:.1%})")
            
            # Показываем топ-3
            top3 = []
            for j in range(min(3, len(fasttext_predictions[0]))):
                lang = fasttext_predictions[0][j].replace('__label__', '')
                conf = fasttext_predictions[1][j]
                top3.append(f"{lang}({conf:.1%})")
            print(f"      Топ-3: {', '.join(top3)}")
            
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
            
            # Показываем топ-3
            if 'all_results' in our_result and our_result['all_results']:
                top3 = [f"{lang}({conf:.1%})" for lang, conf in our_result['all_results'][:3]]
                print(f"      Топ-3: {', '.join(top3)}")
            
        except Exception as e:
            print(f"   🏠 Наша система: Ошибка - {e}")
        
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
    print("-" * 60)
    print(f"FastText: {fasttext_correct}/{len(test_cases)} правильных ({fasttext_correct/len(test_cases)*100:.1f}%)")
    print(f"Наша система: {our_system_correct}/{len(test_cases)} правильных ({our_system_correct/len(test_cases)*100:.1f}%)")
    
    # Анализ по типам текстов
    print(f"\n🔍 АНАЛИЗ ПО ТИПАМ ТЕКСТОВ:")
    print("-" * 60)
    
    latin_kazakh_tests = [t for t in test_cases if 'Латинский казахский' in t['description']]
    cyrillic_kazakh_tests = [t for t in test_cases if 'Кириллический казахский' in t['description']]
    
    print(f"Латинский казахский ({len(latin_kazakh_tests)} тестов):")
    print(f"  FastText: {'✅ Поддерживает' if any('kk' in str(fasttext_model.predict(t['text'], k=1)[0][0]) for t in latin_kazakh_tests) else '❌ Не поддерживает'}")
    print(f"  Наша система: {'✅ Поддерживает' if any(our_detector.detect_language(t['text'])['language'] == 'kk' for t in latin_kazakh_tests) else '❌ Не поддерживает'}")
    
    print(f"Кириллический казахский ({len(cyrillic_kazakh_tests)} тестов):")
    print(f"  FastText: {'✅ Поддерживает' if any('kk' in str(fasttext_model.predict(t['text'], k=1)[0][0]) for t in cyrillic_kazakh_tests) else '❌ Не поддерживает'}")
    print(f"  Наша система: {'✅ Поддерживает' if any(our_detector.detect_language(t['text'])['language'] == 'kk' for t in cyrillic_kazakh_tests) else '❌ Не поддерживает'}")

if __name__ == "__main__":
    compare_systems()
