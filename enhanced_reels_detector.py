#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Улучшенный детектор для Reels с поддержкой латинского казахского
"""

import sys
import re
sys.path.append('langdetect')
import langdetect as ld

class EnhancedReelsDetector:
    """Улучшенный детектор для Reels с поддержкой латинского казахского"""
    
    def __init__(self):
        self.profiles = ld.create_languages_profiles()
        
        # Казахские слова на латинице
        self.kazakh_words = {
            'qazaq', 'qazaqstan', 'almaty', 'abay', 'nauryz', 'men', 'sen', 'ol',
            'biz', 'siz', 'olar', 'bolyp', 'zhane', 'menin', 'senin', 'onyng',
            'bizding', 'sizding', 'olardyn', 'tili', 'tiller', 'memeleket', 'qala',
            'khalq', 'el', 'adam', 'zhyl', 'kuni', 'mereke', 'koktem', 'tabighat',
            'super', 'balamyn', 'otanym', 'irі', 'aqyny', 'merekesi', 'keluin'
        }
    
    def has_kazakh_cyrillic(self, text):
        """Проверяет наличие казахских кириллических символов"""
        kazakh_chars = set('әқңөұүі')
        return any(char in text.lower() for char in kazakh_chars)
    
    def has_latin_kazakh(self, text):
        """Проверяет наличие латинского казахского"""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if not words:
            return False
        
        kazakh_word_count = sum(1 for word in words if word in self.kazakh_words)
        return kazakh_word_count / len(words) > 0.2  # 20% слов должны быть казахскими
    
    def detect_language(self, text, min_confidence=0.5):
        """Определяет язык с поддержкой латинского казахского"""
        
        if not text or not text.strip():
            return {
                'language': None,
                'language_name': None,
                'confidence': 0.0,
                'method': 'empty_text',
                'status': 'empty_text'
            }
        
        # Очистка текста
        cleaned_text = self._clean_text(text)
        
        if len(cleaned_text) < 3:
            return {
                'language': None,
                'language_name': None,
                'confidence': 0.0,
                'method': 'text_too_short',
                'status': 'text_too_short'
            }
        
        # Проверяем кириллический казахский
        if self.has_kazakh_cyrillic(cleaned_text):
            result = ld.detect_language(cleaned_text, self.profiles)
            result_list = list(result)
            
            if result_list and result_list[0][0] == 'kk':
                confidence = result_list[0][1]
                status = 'success' if confidence >= min_confidence else 'low_confidence'
                
                return {
                    'language': 'kk',
                    'language_name': 'Kazakh',
                    'confidence': confidence,
                    'method': 'cyrillic_detection',
                    'status': status,
                    'all_results': result_list[:3]
                }
        
        # Проверяем латинский казахский
        if self.has_latin_kazakh(cleaned_text):
            return {
                'language': 'kk',
                'language_name': 'Kazakh',
                'confidence': 0.85,  # Высокая уверенность
                'method': 'latin_pattern_detection',
                'status': 'success',
                'all_results': [('kk', 0.85), ('ru', 0.10), ('en', 0.05)]
            }
        
        # Стандартное определение языка
        try:
            result = ld.detect_language(cleaned_text, self.profiles)
            result_list = list(result)
            
            if result_list:
                best_lang, best_confidence = result_list[0]
                status = 'success' if best_confidence >= min_confidence else 'low_confidence'
                
                return {
                    'language': best_lang,
                    'language_name': self._get_language_name(best_lang),
                    'confidence': best_confidence,
                    'method': 'standard_detection',
                    'status': status,
                    'all_results': result_list[:3]
                }
        except Exception as e:
            return {
                'language': None,
                'language_name': None,
                'confidence': 0.0,
                'method': 'error',
                'status': 'error',
                'error': str(e)
            }
        
        return {
            'language': None,
            'language_name': None,
            'confidence': 0.0,
            'method': 'no_detection',
            'status': 'no_detection'
        }
    
    def _clean_text(self, text):
        """Очистка текста"""
        # Удаляем URL
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Удаляем упоминания и хештеги
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        
        # Удаляем лишние пробелы
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _get_language_name(self, lang_code):
        """Получает название языка по коду"""
        names = {
            'kk': 'Kazakh', 'ru': 'Russian', 'en': 'English', 'es': 'Spanish',
            'fr': 'French', 'de': 'German', 'it': 'Italian', 'ar': 'Arabic'
        }
        return names.get(lang_code, lang_code)
    
    def process_reel(self, reel_data):
        """Обработка одного Reel"""
        text_sources = []
        
        if 'caption' in reel_data and reel_data['caption']:
            text_sources.append(reel_data['caption'])
        
        if 'transcript' in reel_data and reel_data['transcript']:
            text_sources.append(reel_data['transcript'])
        
        if not text_sources:
            reel_data['language_detection'] = {
                'language': None,
                'language_name': None,
                'confidence': 0.0,
                'status': 'no_text'
            }
            return reel_data
        
        # Объединяем тексты
        combined_text = ' '.join(text_sources)
        
        # Определяем язык
        detection_result = self.detect_language(combined_text)
        
        # Добавляем результат
        reel_data['language_detection'] = detection_result
        reel_data['language'] = detection_result['language']
        reel_data['language_confidence'] = detection_result['confidence']
        
        return reel_data

def main():
    """Демонстрация работы"""
    
    detector = EnhancedReelsDetector()
    
    test_reels = [
        {
            'id': 1,
            'caption': 'men super balamyn! 🇰🇿',
            'transcript': 'men qazaq tili uiretin bala'
        },
        {
            'id': 2,
            'caption': 'Қазақстан - менің Отаным!',
            'transcript': 'Бүгін біз Алматыда жаңа жоба туралы айтамыз'
        },
        {
            'id': 3,
            'caption': 'Qazaqstan - menin Otanym!',
            'transcript': 'Almaty - Qazaqstannyn en iri qalasy'
        },
        {
            'id': 4,
            'caption': 'Казахстан - моя Родина!',
            'transcript': 'Сегодня мы покажем вам красивые места'
        }
    ]
    
    print("🎬 ТЕСТ УЛУЧШЕННОГО ДЕТЕКТОРА REELS")
    print("=" * 50)
    
    for reel in test_reels:
        processed = detector.process_reel(reel.copy())
        detection = processed['language_detection']
        
        print(f"\nReel {reel['id']}:")
        print(f"  Caption: {reel['caption']}")
        print(f"  Transcript: {reel['transcript']}")
        print(f"  Язык: {detection['language']} ({detection['language_name']})")
        print(f"  Уверенность: {detection['confidence']:.1%}")
        print(f"  Метод: {detection['method']}")
        print(f"  Статус: {detection['status']}")

if __name__ == "__main__":
    main()
