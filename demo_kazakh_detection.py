#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Демонстрация работы определения казахского языка
"""

import sys
sys.path.append('langdetect')
import langdetect as ld

def main():
    print("🇰🇿 ДЕМОНСТРАЦИЯ ОПРЕДЕЛЕНИЯ КАЗАХСКОГО ЯЗЫКА 🇰🇿")
    print("=" * 60)
    
    # Создаем профили
    print("Загрузка языковых профилей...")
    profiles = ld.create_languages_profiles()
    print(f"✅ Загружено {len(profiles)} языковых профилей")
    print(f"✅ Казахский язык {'поддерживается' if 'kk' in profiles else 'НЕ поддерживается'}")
    print()
    
    # Тестовые тексты
    test_texts = [
        {
            'lang': 'kk',
            'name': 'Казахский',
            'texts': [
                "Қазақстан - менің Отаным!",
                "Абай Құнанбайұлы қазақтың ұлы ақыны.",
                "Наурыз мерекесі көктемнің келуін білдіреді.",
                "Алматы - Қазақстанның ең ірі қаласы.",
                "Домбыра - қазақтардың ұлттық аспабы."
            ]
        },
        {
            'lang': 'ru', 
            'name': 'Русский',
            'texts': [
                "Казахстан - моя Родина!",
                "Абай Кунанбаев - великий казахский поэт.",
                "Праздник Наурыз символизирует приход весны.",
                "Алматы - крупнейший город Казахстана.",
                "Домбра - национальный инструмент казахов."
            ]
        },
        {
            'lang': 'en',
            'name': 'Английский', 
            'texts': [
                "Kazakhstan is my homeland!",
                "Abay Kunanbayev is a great Kazakh poet.",
                "Nauryz holiday symbolizes the arrival of spring.",
                "Almaty is the largest city in Kazakhstan.",
                "Dombra is the national instrument of Kazakhs."
            ]
        }
    ]
    
    # Тестируем каждый язык
    for lang_group in test_texts:
        lang_code = lang_group['lang']
        lang_name = lang_group['name']
        texts = lang_group['texts']
        
        print(f"🔍 ТЕСТИРОВАНИЕ: {lang_name.upper()} ({lang_code})")
        print("-" * 40)
        
        correct = 0
        total = len(texts)
        
        for i, text in enumerate(texts, 1):
            result = ld.detect_language(text, profiles)
            result_list = list(result)
            
            if result_list:
                detected_lang = result_list[0][0]
                confidence = result_list[0][1]
                
                is_correct = detected_lang == lang_code
                if is_correct:
                    correct += 1
                
                status = "✅" if is_correct else "❌"
                print(f"{status} Текст {i}: {text}")
                print(f"   Определено: {detected_lang} (уверенность: {confidence:.1%})")
                
                if len(result_list) > 1:
                    other_results = [(lang, conf) for lang, conf in result_list[1:3]]
                    print(f"   Альтернативы: {other_results}")
            else:
                print(f"❌ Текст {i}: {text}")
                print("   Не удалось определить язык")
            
            print()
        
        accuracy = correct / total * 100
        print(f"📊 РЕЗУЛЬТАТ: {correct}/{total} правильных ({accuracy:.1f}%)")
        print()
    
    # Тест на смешанные тексты
    print("🔀 ТЕСТ НА СМЕШАННЫЕ ТЕКСТЫ")
    print("-" * 40)
    
    mixed_texts = [
        "Қазақстан Kazakhstan Казахстан",
        "Hello Сәлем Привет", 
        "Абай Abay Абай",
        "🇰🇿 #Kazakhstan #Қазақстан #Казахстан",
        "Алматы Almaty Алматы - beautiful city!"
    ]
    
    for text in mixed_texts:
        result = ld.detect_language(text, profiles)
        result_list = list(result)
        
        print(f"📝 Текст: {text}")
        if result_list:
            top_3 = result_list[:3]
            print(f"   Результат: {top_3}")
        else:
            print("   Не удалось определить язык")
        print()
    
    print("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print("=" * 60)
    print("Казахский язык успешно интегрирован в систему определения языков!")

if __name__ == "__main__":
    main()
