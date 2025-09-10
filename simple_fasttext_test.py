#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Простой тест FastText для латинского казахского
"""

import sys
import os

def test_fasttext_simple():
    """Простой тест FastText"""
    
    print("🚀 ПРОСТОЙ ТЕСТ FASTTEXT")
    print("=" * 40)
    
    try:
        import fasttext
        print("✅ FastText импортирован")
        
        # Загружаем модель
        print("Загрузка модели lid.176.bin...")
        model = fasttext.load_model('lid.176.bin')
        print("✅ Модель загружена")
        
        # Тестовые тексты
        test_texts = [
            "men super balamyn",
            "Qazaqstan - menin Otanym!",
            "Almaty - Qazaqstannyn en iri qalasy",
            "Қазақстан - менің Отаным!",
            "Казахстан - моя Родина!",
            "Kazakhstan is my homeland!"
        ]
        
        print(f"\n🧪 ТЕСТИРОВАНИЕ {len(test_texts)} ТЕКСТОВ:")
        print("-" * 40)
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n{i}. Текст: {text}")
            
            try:
                # Простое предсказание
                predictions = model.predict(text)
                language = predictions[0][0].replace('__label__', '')
                confidence = predictions[1][0]
                
                print(f"   Результат: {language} (уверенность: {confidence:.1%})")
                
                # Анализ
                if 'men' in text.lower() or 'qazaq' in text.lower():
                    if language == 'kk':
                        print("   ✅ ПРАВИЛЬНО! FastText узнал латинский казахский")
                    else:
                        print(f"   ❌ НЕПРАВИЛЬНО! Определил как {language}")
                elif 'Қазақ' in text or 'менің' in text:
                    if language == 'kk':
                        print("   ✅ ПРАВИЛЬНО! FastText узнал кириллический казахский")
                    else:
                        print(f"   ❌ НЕПРАВИЛЬНО! Определил как {language}")
                elif 'Казахстан' in text and 'Родина' in text:
                    if language == 'ru':
                        print("   ✅ ПРАВИЛЬНО! FastText узнал русский")
                    else:
                        print(f"   ❌ НЕПРАВИЛЬНО! Определил как {language}")
                elif 'Kazakhstan' in text and 'homeland' in text:
                    if language == 'en':
                        print("   ✅ ПРАВИЛЬНО! FastText узнал английский")
                    else:
                        print(f"   ❌ НЕПРАВИЛЬНО! Определил как {language}")
                
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        print(f"\n📊 ВЫВОД:")
        print("-" * 40)
        print("FastText протестирован на латинском казахском")
        print("Проверьте результаты выше для анализа точности")
        
    except ImportError:
        print("❌ FastText не установлен")
        print("Установите: pip install fasttext")
    except FileNotFoundError:
        print("❌ Модель lid.176.bin не найдена")
        print("Скачайте: curl -O https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_fasttext_simple()


