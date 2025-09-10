#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для интеграции определения языка в систему обработки Reels
Поддерживает определение казахского и русского языков
"""

import sys
import os
import json
import logging
from typing import Dict, List, Tuple, Optional

# Добавляем путь к модулю langdetect
sys.path.append('langdetect')

import langdetect as ld

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReelsLanguageDetector:
    """Класс для определения языка в системе обработки Reels"""
    
    def __init__(self):
        """Инициализация детектора языка"""
        self.profiles = None
        self.supported_languages = {
            'kk': 'Kazakh',
            'ru': 'Russian', 
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'ar': 'Arabic'
        }
        self._load_profiles()
    
    def _load_profiles(self):
        """Загрузка языковых профилей"""
        try:
            logger.info("Загрузка языковых профилей...")
            self.profiles = ld.create_languages_profiles()
            logger.info(f"Загружено профилей: {len(self.profiles)}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке профилей: {e}")
            raise
    
    def detect_language(self, text: str, min_confidence: float = 0.5) -> Dict:
        """
        Определение языка текста
        
        Args:
            text (str): Текст для анализа
            min_confidence (float): Минимальная уверенность для принятия результата
            
        Returns:
            Dict: Результат определения языка
        """
        if not text or not text.strip():
            return {
                'language': None,
                'language_name': None,
                'confidence': 0.0,
                'all_results': [],
                'status': 'empty_text'
            }
        
        # Очистка текста
        cleaned_text = self._clean_text(text)
        
        if len(cleaned_text) < 10:
            return {
                'language': None,
                'language_name': None,
                'confidence': 0.0,
                'all_results': [],
                'status': 'text_too_short'
            }
        
        try:
            # Определение языка
            result = ld.detect_language(cleaned_text, self.profiles)
            result_list = list(result)
            
            if not result_list:
                return {
                    'language': None,
                    'language_name': None,
                    'confidence': 0.0,
                    'all_results': [],
                    'status': 'no_detection'
                }
            
            # Получаем лучший результат
            best_lang, best_confidence = result_list[0]
            
            # Проверяем минимальную уверенность
            if best_confidence < min_confidence:
                status = 'low_confidence'
            else:
                status = 'success'
            
            return {
                'language': best_lang,
                'language_name': self.supported_languages.get(best_lang, best_lang),
                'confidence': best_confidence,
                'all_results': result_list[:3],  # Топ-3 результата
                'status': status
            }
            
        except Exception as e:
            logger.error(f"Ошибка при определении языка: {e}")
            return {
                'language': None,
                'language_name': None,
                'confidence': 0.0,
                'all_results': [],
                'status': 'error',
                'error': str(e)
            }
    
    def _clean_text(self, text: str) -> str:
        """Очистка текста от лишних символов"""
        import re
        
        # Удаляем URL
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Удаляем упоминания (@username)
        text = re.sub(r'@\w+', '', text)
        
        # Удаляем хештеги (#hashtag)
        text = re.sub(r'#\w+', '', text)
        
        # Удаляем лишние пробелы
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def process_reel(self, reel_data: Dict) -> Dict:
        """
        Обработка одного Reel
        
        Args:
            reel_data (Dict): Данные Reel с полями caption и/или transcript
            
        Returns:
            Dict: Обновленные данные Reel с информацией о языке
        """
        # Получаем текст для анализа
        text_sources = []
        
        if 'caption' in reel_data and reel_data['caption']:
            text_sources.append(('caption', reel_data['caption']))
        
        if 'transcript' in reel_data and reel_data['transcript']:
            text_sources.append(('transcript', reel_data['transcript']))
        
        if not text_sources:
            reel_data['language_detection'] = {
                'language': None,
                'language_name': None,
                'confidence': 0.0,
                'status': 'no_text'
            }
            return reel_data
        
        # Объединяем все тексты
        combined_text = ' '.join([text for _, text in text_sources])
        
        # Определяем язык
        detection_result = self.detect_language(combined_text)
        
        # Добавляем результат в данные Reel
        reel_data['language_detection'] = detection_result
        
        # Для совместимости добавляем отдельные поля
        reel_data['language'] = detection_result['language']
        reel_data['language_confidence'] = detection_result['confidence']
        
        return reel_data
    
    def process_batch(self, reels_data: List[Dict]) -> List[Dict]:
        """
        Обработка пакета Reels
        
        Args:
            reels_data (List[Dict]): Список данных Reels
            
        Returns:
            List[Dict]: Обработанные данные Reels
        """
        processed_reels = []
        
        for i, reel_data in enumerate(reels_data):
            try:
                processed_reel = self.process_reel(reel_data)
                processed_reels.append(processed_reel)
                
                if (i + 1) % 100 == 0:
                    logger.info(f"Обработано {i + 1} Reels")
                    
            except Exception as e:
                logger.error(f"Ошибка при обработке Reel {i}: {e}")
                # Добавляем Reel с ошибкой
                reel_data['language_detection'] = {
                    'language': None,
                    'language_name': None,
                    'confidence': 0.0,
                    'status': 'processing_error',
                    'error': str(e)
                }
                processed_reels.append(reel_data)
        
        return processed_reels

def main():
    """Пример использования"""
    
    # Создаем детектор
    detector = ReelsLanguageDetector()
    
    # Примеры данных Reels
    sample_reels = [
        {
            'id': 1,
            'caption': 'Қазақстан - менің Отаным! 🇰🇿 #Kazakhstan #Қазақстан',
            'transcript': 'Бүгін біз Алматыда жаңа жоба туралы айтамыз'
        },
        {
            'id': 2,
            'caption': 'Красивые виды Казахстана 🏔️ #природа #путешествия',
            'transcript': 'Сегодня мы покажем вам самые красивые места нашей страны'
        },
        {
            'id': 3,
            'caption': 'Amazing Kazakhstan! Beautiful nature and culture 🌟',
            'transcript': 'Welcome to Kazakhstan, the heart of Central Asia'
        },
        {
            'id': 4,
            'caption': '',  # Пустая подпись
            'transcript': ''  # Пустой транскрипт
        }
    ]
    
    print("=== Пример обработки Reels ===\n")
    
    # Обрабатываем каждый Reel
    for reel in sample_reels:
        print(f"Reel ID: {reel['id']}")
        print(f"Caption: {reel['caption']}")
        print(f"Transcript: {reel['transcript']}")
        
        processed_reel = detector.process_reel(reel.copy())
        detection = processed_reel['language_detection']
        
        print(f"Определенный язык: {detection['language']} ({detection['language_name']})")
        print(f"Уверенность: {detection['confidence']:.3f}")
        print(f"Статус: {detection['status']}")
        
        if detection.get('all_results'):
            print(f"Все результаты: {detection['all_results']}")
        
        print("-" * 50)
    
    # Пример пакетной обработки
    print("\n=== Пакетная обработка ===")
    processed_batch = detector.process_batch(sample_reels)
    
    # Статистика
    languages_count = {}
    for reel in processed_batch:
        lang = reel['language_detection']['language']
        if lang:
            languages_count[lang] = languages_count.get(lang, 0) + 1
    
    print(f"Статистика языков: {languages_count}")

if __name__ == "__main__":
    main()
