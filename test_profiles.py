#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# Добавляем путь к модулю langdetect
sys.path.append('langdetect')

try:
    import langdetect as ld
    
    print("Создание языковых профилей...")
    print("Доступные языки:", list(ld.LANGUAGES.keys()))
    
    # Создаем профили для всех языков
    profiles = ld.create_languages_profiles()
    
    print(f"Создано профилей: {len(profiles)}")
    
    # Проверяем, что казахский профиль создан
    if 'kk' in profiles:
        print("✓ Казахский профиль успешно создан")
        kk_profile = profiles['kk']
        print(f"  Количество n-грамм в казахском профиле: {len(kk_profile)}")
        
        # Показываем несколько примеров n-грамм
        sample_ngrams = list(kk_profile.keys())[:10]
        print(f"  Примеры n-грамм: {sample_ngrams}")
    else:
        print("✗ Казахский профиль не создан")
    
    print("\nТестирование определения языка...")
    
    # Тестовые тексты
    test_texts = {
        'kk': "Қазақстан Республикасы Орталық Азияда орналасқан мемлекет.",
        'ru': "Казахстан - государство, расположенное в Центральной Азии.",
        'en': "Kazakhstan is a country located in Central Asia."
    }
    
    for lang_code, text in test_texts.items():
        try:
            result = ld.detect_language(text, profiles)
            result_list = list(result)
            print(f"Текст ({lang_code}): {text[:50]}...")
            print(f"  Результат: {result_list[:3]}")
        except Exception as e:
            print(f"Ошибка при определении языка для {lang_code}: {e}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()
