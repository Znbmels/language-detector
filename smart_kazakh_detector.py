#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Умный детектор казахского языка с поддержкой латиницы
"""

import sys
import re
sys.path.append('langdetect')
import langdetect as ld

class SmartKazakhDetector:
    """Умный детектор казахского языка"""
    
    def __init__(self):
        self.profiles = ld.create_languages_profiles()
        
        # Паттерны латинского казахского
        self.latin_kazakh_patterns = [
            r'\bqazaq\b',  # qazaq
            r'\bqazaqstan\b',  # qazaqstan
            r'\balmaty\b',  # almaty
            r'\babay\b',  # abay
            r'\bnauryz\b',  # nauryz
            r'\bmen\b',  # men (я)
            r'\bsen\b',  # sen (ты)
            r'\bol\b',  # ol (он)
            r'\bbiz\b',  # biz (мы)
            r'\bsiz\b',  # siz (вы)
            r'\bolar\b',  # olar (они)
            r'\bbolyp\b',  # bolyp (будучи)
            r'\bzhane\b',  # zhane (и)
            r'\bmenin\b',  # menin (мой)
            r'\bsenin\b',  # senin (твой)
            r'\bonyng\b',  # onyng (его)
            r'\bbizding\b',  # bizding (наш)
            r'\bsizding\b',  # sizding (ваш)
            r'\bolardyn\b',  # olardyn (их)
        ]
        
        # Казахские слова на латинице
        self.kazakh_words = {
            'qazaq', 'qazaqstan', 'almaty', 'abay', 'nauryz', 'men', 'sen', 'ol',
            'biz', 'siz', 'olar', 'bolyp', 'zhane', 'menin', 'senin', 'onyng',
            'bizding', 'sizding', 'olardyn', 'tili', 'tiller', 'memeleket', 'qala',
            'khalq', 'el', 'adam', 'zhyl', 'kuni', 'mereke', 'koktem', 'tabighat'
        }
    
    def has_kazakh_cyrillic(self, text):
        """Проверяет наличие казахских кириллических символов"""
        kazakh_chars = set('әқңөұүі')
        return any(char in text.lower() for char in kazakh_chars)
    
    def has_latin_kazakh_patterns(self, text):
        """Проверяет наличие латинских казахских паттернов"""
        text_lower = text.lower()
        
        # Проверяем паттерны
        for pattern in self.latin_kazakh_patterns:
            if re.search(pattern, text_lower):
                return True
        
        # Проверяем слова
        words = re.findall(r'\b\w+\b', text_lower)
        kazakh_word_count = sum(1 for word in words if word in self.kazakh_words)
        
        # Если больше 30% слов - казахские, считаем казахским
        if len(words) > 0 and kazakh_word_count / len(words) > 0.3:
            return True
        
        return False
    
    def detect_language(self, text):
        """Определяет язык с учетом латинского казахского"""
        
        if not text or not text.strip():
            return {
                'language': None,
                'confidence': 0.0,
                'method': 'empty_text'
            }
        
        # Проверяем кириллический казахский
        if self.has_kazakh_cyrillic(text):
            result = ld.detect_language(text, self.profiles)
            result_list = list(result)
            
            if result_list and result_list[0][0] == 'kk':
                return {
                    'language': 'kk',
                    'confidence': result_list[0][1],
                    'method': 'cyrillic_detection'
                }
        
        # Проверяем латинский казахский
        if self.has_latin_kazakh_patterns(text):
            return {
                'language': 'kk',
                'confidence': 0.8,  # Высокая уверенность для латинского
                'method': 'latin_pattern_detection'
            }
        
        # Обычное определение языка
        result = ld.detect_language(text, self.profiles)
        result_list = list(result)
        
        if result_list:
            return {
                'language': result_list[0][0],
                'confidence': result_list[0][1],
                'method': 'standard_detection'
            }
        
        return {
            'language': None,
            'confidence': 0.0,
            'method': 'no_detection'
        }

def test_smart_detector():
    """Тестирует умный детектор"""
    
    print("🧠 ТЕСТ УМНОГО ДЕТЕКТОРА КАЗАХСКОГО")
    print("=" * 50)
    
    detector = SmartKazakhDetector()
    
    test_cases = [
        # Кириллический казахский
        ("Қазақстан - менің Отаным!", "Кириллический казахский"),
        ("Абай Құнанбайұлы қазақтың ұлы ақыны", "Кириллический казахский"),
        
        # Латинский казахский
        ("men super balamyn", "Латинский казахский"),
        ("Qazaqstan - menin Otanym!", "Латинский казахский"),
        ("Almaty - Qazaqstannyn en iri qalasy", "Латинский казахский"),
        ("Abay Qunanbaiuly qazaqtyn uly aqyny", "Латинский казахский"),
        
        # Другие языки
        ("Казахстан - моя Родина!", "Русский"),
        ("Kazakhstan is my homeland!", "Английский"),
        ("Kazakhstan - mein Heimatland!", "Немецкий"),
        
        # Смешанные тексты
        ("Қазақстан Kazakhstan Казахстан", "Смешанный"),
        ("Hello Сәлем men super balamyn", "Смешанный")
    ]
    
    for text, description in test_cases:
        result = detector.detect_language(text)
        
        print(f"\n📝 {description}")
        print(f"   Текст: {text}")
        print(f"   Результат: {result['language']} (уверенность: {result['confidence']:.1%})")
        print(f"   Метод: {result['method']}")
        
        # Анализируем результат
        if 'казахский' in description.lower():
            if result['language'] == 'kk':
                print("   ✅ ПРАВИЛЬНО!")
            else:
                print("   ❌ НЕПРАВИЛЬНО!")
        else:
            print("   ℹ️  Другой язык")

if __name__ == "__main__":
    test_smart_detector()
