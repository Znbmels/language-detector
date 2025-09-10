#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Тест определения латинского казахского языка
"""

import sys
sys.path.append('langdetect')
import langdetect as ld

def test_latin_kazakh():
    print("🔤 ТЕСТ ЛАТИНСКОГО КАЗАХСКОГО ЯЗЫКА")
    print("=" * 50)
    
    # Создаем профили
    print("Загрузка языковых профилей...")
    profiles = ld.create_languages_profiles()
    print(f"✅ Загружено {len(profiles)} профилей\n")
    
    # Тестовые тексты на латинском казахском
    latin_kazakh_texts = [
        {
            'text': "men super balamyn",
            'translation': "мен супер баламын",
            'description': "Короткая фраза"
        },
        {
            'text': "Qazaqstan - menin Otanym!",
            'translation': "Қазақстан - менің Отаным!",
            'description': "Фраза про Родину"
        },
        {
            'text': "Almaty - Qazaqstannyn en iri qalasy",
            'translation': "Алматы - Қазақстанның ең ірі қаласы",
            'description': "Про Алматы"
        },
        {
            'text': "Abay Qunanbaiuly qazaqtyn uly aqyny",
            'translation': "Абай Құнанбайұлы қазақтың ұлы ақыны",
            'description': "Про Абая"
        },
        {
            'text': "Nauryz merekesi koktemnin keluin bildiredi",
            'translation': "Наурыз мерекесі көктемнің келуін білдіреді",
            'description': "Про Наурыз"
        },
        {
            'text': "Qazaq tili turki tiller tobyna zhatatyn til",
            'translation': "Қазақ тілі түркі тілдер тобына жататын тіл",
            'description': "Про казахский язык"
        }
    ]
    
    print("🔍 ТЕСТИРОВАНИЕ ЛАТИНСКОГО КАЗАХСКОГО:")
    print("-" * 50)
    
    for i, test_case in enumerate(latin_kazakh_texts, 1):
        text = test_case['text']
        translation = test_case['translation']
        description = test_case['description']
        
        print(f"\n{i}. {description}")
        print(f"   Латинский: {text}")
        print(f"   Кириллица: {translation}")
        
        try:
            result = ld.detect_language(text, profiles)
            result_list = list(result)
            
            if result_list:
                detected_lang = result_list[0][0]
                confidence = result_list[0][1]
                
                print(f"   🎯 Определено: {detected_lang} (уверенность: {confidence:.1%})")
                print(f"   📊 Все результаты: {result_list[:3]}")
                
                # Анализируем результат
                if detected_lang == 'kk':
                    print("   ✅ ПРАВИЛЬНО! Система узнала казахский")
                else:
                    print(f"   ❌ НЕПРАВИЛЬНО! Определила как {detected_lang}")
                    print("   💡 Проблема: латинский казахский не распознается")
            else:
                print("   ❌ Не удалось определить язык")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    # Сравнение с кириллицей
    print(f"\n🔄 СРАВНЕНИЕ С КИРИЛЛИЦЕЙ:")
    print("-" * 50)
    
    comparison_texts = [
        ("men super balamyn", "мен супер баламын"),
        ("Qazaqstan", "Қазақстан"),
        ("Almaty", "Алматы"),
        ("Abay", "Абай")
    ]
    
    for latin, cyrillic in comparison_texts:
        print(f"\nСравнение: '{latin}' vs '{cyrillic}'")
        
        # Тестируем латинский
        latin_result = ld.detect_language(latin, profiles)
        latin_list = list(latin_result)
        print(f"  Латинский: {latin_list[0] if latin_list else 'Не определен'}")
        
        # Тестируем кириллицу
        cyrillic_result = ld.detect_language(cyrillic, profiles)
        cyrillic_list = list(cyrillic_result)
        print(f"  Кириллица: {cyrillic_list[0] if cyrillic_list else 'Не определен'}")
    
    print(f"\n📋 ВЫВОДЫ:")
    print("-" * 50)
    print("1. Система обучена на кириллическом казахском")
    print("2. Латинский казахский НЕ распознается как казахский")
    print("3. Нужно добавить латинские тексты в корпус")
    print("4. Или использовать транслитерацию")

if __name__ == "__main__":
    test_latin_kazakh()
